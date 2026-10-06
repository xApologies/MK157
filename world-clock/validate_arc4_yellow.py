"""Audit Checkpoint 21 source fidelity, daily rewards, event scope and preservation."""
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re


def audit(root):
    errors=[]
    def require(ok,message):
        if not ok: errors.append(message)
    def text(p): return (root/p).read_text(encoding='utf-8-sig')
    def js(p): return json.loads(text(p))
    def rows(p):
        with (root/p).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
    def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
    archive='provenance/checkpoint-21-package/'
    before=js('provenance/CHECKPOINT_21_BEFORE_REVIEW.json')
    manifest=js(archive+'MANIFEST.json')
    expected_sources=set(manifest['files'])|{'MANIFEST.json'}
    actual_sources={p.relative_to(root/archive).as_posix() for p in (root/archive).rglob('*') if p.is_file()}
    require(actual_sources==expected_sources and len(actual_sources)==10,'Source file set differs from package manifest')
    for p,expected in before['package_source_sha256'].items():
        require(sha(archive+p)==expected,'Archived source differs from uploaded ZIP: '+p)
    for ext in ('csv','json'):
        p='ARC4_YELLOW_COMBAT_CALENDAR.'+ext
        require((root/'world-clock'/p).read_bytes()==(root/archive/p).read_bytes(),'Active calendar source bytes differ: '+p)
    calendar=rows('world-clock/ARC4_YELLOW_COMBAT_CALENDAR.csv')
    for row in calendar:
        for field in ('week','day','kira_deterministic_credits','illi_deterministic_credits'): row[field]=int(row[field])
    require(calendar==js('world-clock/ARC4_YELLOW_COMBAT_CALENDAR.json'),'CSV/JSON calendar mismatch')
    dates=[('Yellow',1,d) for d in range(3,8)]+[('Yellow',w,d) for w in range(2,6) for d in range(1,8)]+[('Yellow',6,d) for d in range(1,4)]
    require([(r['season'],r['week'],r['day']) for r in calendar]==dates and len(calendar)==36,'36 consecutive Y1D3–Y6D3 rows required')
    require(all(r['status']=='LOCKED SCAFFOLD' for r in calendar),'Calendar status changed')
    lookup={(r['week'],r['day']):r for r in calendar}
    trial={r['wave']:r['cumulative'] for r in js('trial-rewards/TRIAL_WAVE_CREDITS.json')}
    rewards=js('combat-rewards/COMBAT_REWARD_TABLES.json')
    counts=Counter()
    totals={'kira':0,'illi':0}
    by_kind=defaultdict(lambda:{'kira':0,'illi':0})
    paid=set(); raid_bookings=[]; daily=[]
    raid_results={(3,1):('normal',[],['Red']), (3,6):('normal',['Red'],['Orange']),
                  (4,6):('normal',['Red','Orange'],[]),(6,1):('hard',['Red'],['Orange'])}
    no_combat={'Recovery / open','Recovery / social beat','Open','illi progression purchase','raeon tournament','raeon tournament window','Arc Four endpoint'}
    for index,row in enumerate(calendar):
        kind=row['event']; date=(row['week'],row['day']); k=i=0
        if kind in ('Shared Duo Trial','Kira Solo Trial'):
            shared=kind=='Shared Duo Trial'
            counts['shared_duo_W18' if shared else 'kira_solo_W18']+=1
            require('W18' in row['result'] and 'W19' in row['result'] and 'fail' in row['result'].lower(),'Trial depth/result mismatch')
            require('full day' in row['duration_author_target'] and '21–38' in row['duration_author_target'],'Trial full-day runtime missing')
            following=calendar[index+1]
            require(following['result']=='No required combat' and following['kira_deterministic_credits']==following['illi_deterministic_credits']==0,'Trial following day has required combat')
            k=trial[18]; i=k if shared else 0
        elif kind=='Orange Dungeon session':
            m=re.fullmatch(r'(\d+) clears',row['result']); require(m is not None,'Orange clear count missing')
            n=int(m.group(1)); counts['orange_dungeon_clears']+=n; counts['orange_farm_sessions']+=1
            k=i=n*rewards['dungeons']['normal']['Orange']
        elif kind=='Yellow Dungeon push':
            counts['yellow_dungeon_attempts']+=1; counts['yellow_failures']+=1
            require(row['result']=='FAIL' and 'OPEN' in row['notes'],'Failed Dungeon partial boundary lost')
        elif kind=='Yellow Dungeon — Kira independent':
            counts['yellow_dungeon_attempts']+=1; counts['yellow_dungeon_clears_kira']+=1
            require(date==(4,2) and row['result']=='CLEAR' and 'royal' in row['illi_activity'].lower(),'Independent first Yellow clear changed')
            k=rewards['dungeons']['normal']['Yellow']
        elif kind=='Progression-cohort Yellow farm':
            m=re.fullmatch(r'(\d+) clears',row['result']); require(m is not None,'Yellow farm clear count missing')
            n=int(m.group(1)); counts['yellow_dungeon_attempts']+=n
            counts['yellow_dungeon_clears_kira']+=n; counts['yellow_dungeon_clears_illi']+=n
            require(date==(5,3),'Shared Yellow farm moved')
            k=i=n*rewards['dungeons']['normal']['Yellow']
        elif kind in ('Normal Raid attempt','Hard Raid attempt'):
            mode,cleared,failed=raid_results[date]
            require(mode==('normal' if kind=='Normal Raid attempt' else 'hard'),'Raid mode mismatch')
            counts[mode+'_raid_attempts']+=1
            payouts=[]
            for boss in cleared:
                key=('Yellow',mode,boss)
                value=0 if key in paid else rewards['raids'][mode][boss]
                paid.add(key); k+=value; payouts.append({'boss':boss,'credits_each':value})
            i=k
            raid_bookings.append({'date':f'Y{date[0]}D{date[1]}','mode':mode,'cleared':payouts,'failed':failed})
        elif kind in no_combat:
            counts['noncombat_rows']+=1
        else:
            require(False,'Unexpected scheduled event: '+kind)
        require((row['kira_deterministic_credits'],row['illi_deterministic_credits'])==(k,i),'Reward mismatch at '+str(date))
        for who,value in (('kira',k),('illi',i)):
            totals[who]+=value; by_kind[kind][who]+=value
        daily.append({'date':f'Y{date[0]}D{date[1]}','event':kind,'kira':k,'illi':i,'cumulative_gross':totals.copy()})
    expected={'shared_duo_W18':5,'kira_solo_W18':1,'orange_dungeon_clears':17,'orange_farm_sessions':5,
              'yellow_dungeon_attempts':4,'yellow_failures':1,'yellow_dungeon_clears_kira':3,
              'yellow_dungeon_clears_illi':2,'normal_raid_attempts':3,'hard_raid_attempts':1,'noncombat_rows':18}
    require(dict(counts)==expected,'Activity counts mismatch')
    require(totals=={'illi':64725,'kira':73585},'Deterministic gross mismatch')
    require(paid=={('Yellow','normal','Red'),('Yellow','normal','Orange'),('Yellow','hard','Red')},'Unexpected Raid major reward')
    require(raid_bookings[2]['cleared'][0]['credits_each']==0,'Duplicate Normal Red payout')
    require(not any('Green Dungeon' in r['kira_activity']+r['illi_activity'] or 'domai' in r['event'].lower() for r in calendar),'Invented Green Dungeon/domai run')
    require(lookup[(5,1)]['event']=='raeon tournament' and lookup[(5,6)]['event']=='raeon tournament window','Tournament protected dates changed')
    require('OPEN' in lookup[(5,6)]['notes'] and 'No required combat'==lookup[(5,6)]['result'],'Personal elimination invented')
    require(all(lookup[d]['event']=='illi progression purchase' for d in ((2,4),(3,5),(5,2))),'Combat collides with progression purchase')
    require(lookup[(6,3)]['event']=='Arc Four endpoint' and 'exact day remains' in lookup[(6,3)]['notes'],'Endpoint/Orb-window boundary lost')
    scale={r['dungeon_rank']:r['target_runtime'] for r in rows('builder/encounters/NORMAL_DUNGEON_AUTHOR_SCALE.csv')}
    require(scale['Orange']=='3–5 hr' and scale['Yellow']=='5–10 hr','Dungeon runtime scale changed')
    minimum=3*Fraction(20,60)+4*Fraction(45,60)+5*1+6*2
    maximum=3*Fraction(40,60)+4*Fraction(75,60)+5*2+6*Fraction(7,2)
    require((minimum,maximum,(minimum+maximum)/2)==(21,38,Fraction(59,2)),'W18 band aggregation mismatch')
    ledger=js('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json')
    require(len(ledger)==17 and sum(r['cost'] for r in ledger)==250884,'17-event ledger total changed')
    yellow=[r for r in ledger if r['season']=='Yellow' and (r['week'],r['day'])!=(1,2)]
    require([r['cost'] for r in yellow]==[9680,17424,36590,9350] and sum(r['cost'] for r in yellow)==73044,'Arc Four spend changed')
    future=[(r['season'],r['week'],r['day'],r['cost']) for r in ledger if r['season'] in ('Green','Violet')]
    require(future==[('Green',6,2,9350),('Green',6,4,14960),('Green',7,2,26928),('Violet',1,3,56549),('Violet',2,2,9350)],'Future milestone dates/costs changed')
    handoff=js('world-clock/ARC4_HANDOFF.json')
    require(handoff['kira_black_scaffold']=={'Armor of the Abyss':'Entry/Red','CSR':'Early Orange','Genesis Orbs':'Late Yellow','Halo':'Early Blue','Domain':'Late Violet'},'Seasonal scaffold changed')
    require(handoff['kira_orbs']['date'] is None and handoff['kira_orbs']['price']==61017 and handoff['kira_card']['price']==86000,'Orb day invented or prices changed')
    require(handoff['yellow_deterministic_gross']==totals and handoff['yellow_personal_elimination_day'] is None,'Handoff gross/bracket mismatch')
    require('move' in handoff['hard_raid_date_policy'] and 'preserving' in handoff['hard_raid_date_policy'],'Future tournament conflict rule missing')
    # Preserve all earlier archived evidence, checkpoint masters, priced registries and dated data.
    protected=[]
    for p,expected_hash in before['sha256'].items():
        should_preserve=(p.startswith(('provenance/','prior-checkpoint-source/','bindings/','summons/','combat-rewards/','trial-rewards/'))
            or bool(re.fullmatch(r'live-model/\d+_CHECKPOINT_.*\.md',p))
            or (p.startswith('builder/encounters/eldris/') and not p.endswith(('/README.md','/AUDIT.json')))
            or p=='builder/encounters/NORMAL_DUNGEON_AUTHOR_SCALE.csv'
            or p in ['world-clock/'+n for n in ('WORLD_CLOCK_TEMPLATE.csv','PRISM_TEAM_TRACKER.csv','ILLI_PROGRESSION_SKELETON.csv','ILLI_PROGRESSION_SKELETON.json','ILLI_AUTHOR_PROGRESSION_LEDGER.csv','ILLI_AUTHOR_PROGRESSION_LEDGER.json','RED_TO_ORANGE_COMBAT_CALENDAR.csv','RED_TO_ORANGE_COMBAT_CALENDAR.json','ARC3_ORANGE_CALENDAR.csv','ARC3_ORANGE_CALENDAR.json')])
        if should_preserve:
            require(sha(p)==expected_hash,'Protected baseline bytes changed: '+p); protected.append(p)
    source=text(archive+'CHECKPOINT21_LIVE_MODEL_DELTA.md')
    require(text('live-model/28_CHECKPOINT_21_ARC4_YELLOW.md').endswith(source),'Full author delta not retained')
    content={
      'live-model/ELDRIS_REFERENCE.md':['stabilized','bounded by closure','black','energy intrusion','energy-mass projection','juggernaut','secondary effects','A: R/O/Y; B: G/B; C: V','not universal color→domain','209','no White eldris','Absorption refresh','W19'],
      'live-model/COMBAT_ECOLOGY.md':['17–45','youth track','three-person peer nucleus','NOT a fixed guild/vaelum','private inventory','item-level','does NOT clear Green Solo','military/guard/vaelum/noble','pseudo-Guardian','No Yellow Raid boss clear'],
      'live-model/COMBAT_THRESHOLDS.md':['21–38','29.5','31-hour','spillover','W19','Blue competence'],
      'live-model/ECONOMY_PURCHASE_SCHEDULE.md':['8,319','12,568','NOT a canonical deficit','Affordability never auto-advances','clothing and social presentation','ordinary savings','future luxury goals'],
      'live-model/OPEN.md':['exact Late Yellow Orb purchase day','personal Yellow raeon elimination','cohort headcount','carry-in','failed-Dungeon partial','G6D2','V2D2'],
      'live-model/SOCIAL_LIFE_AND_FOUNDATIONS.md':['Tea Parties','Yellow Gala','Builder parties','deck nights','Genesis-card gatherings','abecca routines','royal-family scenes','Champion Table','home/recovery'],
    }
    for p,phrases in content.items():
        value=text(p).lower()
        for phrase in phrases: require(phrase.lower() in value,'Missing content: '+p+': '+phrase)
    inputs=['world-clock/ARC4_YELLOW_COMBAT_CALENDAR.csv','world-clock/ARC4_YELLOW_COMBAT_CALENDAR.json',
            'world-clock/ARC4_HANDOFF.json','world-clock/validate_arc4_yellow.py',*content]
    return {'checkpoint':21,'result':'FAIL' if errors else 'PASS','errors':errors,'baseline_commit':before['baseline_commit'],
      'calendar_rows':len(calendar),'counts':dict(counts),'deterministic_gross':totals,'income_by_event':dict(by_kind),
      'daily_gross':daily,'raid_bookings':raid_bookings,'no_green_dungeon_or_yellow_raid_clear':not errors,
      'scheduled_domai':0,'failed_dungeon_partial_progress':'OPEN and excluded',
      'runtime_hours':{'W18_min':float(minimum),'W18_max':float(maximum),'W18_central':float((minimum+maximum)/2),'day':31,'Orange':[3,5],'Yellow':[5,10]},
      'illi_arc4_spend':sum(r['cost'] for r in yellow),'zero_carry_in_illustrations_only':{'illi_gap':73044-totals['illi'],'kira_before_cards_after_orbs':totals['kira']-61017},
      'gross_is_not_balance':True,'illi_future_milestones':future,'all_17_illi_milestones_preserved':not errors,
      'kira_black_scaffold':handoff['kira_black_scaffold'],'exact_orb_day':'OPEN; Y6D3 labels the window only',
      'personal_yellow_elimination':'OPEN; reschedule Hard Raid only if a later actual bracket date conflicts',
      'source_files':sorted(actual_sources),'source_pdf_sha256':sha(archive+'source/MK147_MASTER_ELDRIS_LRS.pdf'),
      'preserved_baseline_files':protected,'sha256':{p:sha(p) for p in inputs}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write-audit',action='store_true')
    args=parser.parse_args()
    try: report=audit(args.repository.resolve())
    except (OSError,KeyError,ValueError,TypeError,IndexError,AttributeError) as exc:
        report={'result':'FAIL','errors':[str(exc)]}
    if args.write_audit and report['result']=='PASS':
        (args.repository/'world-clock/ARC4_YELLOW_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('daily_gross','sha256','preserved_baseline_files','source_files','income_by_event')},indent=2,ensure_ascii=False))
    return 0 if report['result']=='PASS' else 1


if __name__=='__main__': raise SystemExit(main())
