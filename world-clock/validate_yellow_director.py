"""Validate the current CP22 Yellow director calendar, Arc Five and preserved canon."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


def audit(root):
    errors=[]
    def require(ok,msg):
        if not ok: errors.append(msg)
    def text(p): return (root/p).read_text(encoding='utf-8-sig')
    def js(p): return json.loads(text(p))
    def rows(p):
        with (root/p).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
    def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
    before=js('provenance/CHECKPOINT_22_BEFORE_REVIEW.json')
    archive='provenance/checkpoint-22-package/'
    sources=set(js(archive+'MANIFEST.json')['files'])
    require(sources=={p.name for p in (root/archive).iterdir() if p.is_file()} and len(sources)==16,'Package manifest/source membership mismatch')
    for p,h in before['package_source_sha256'].items(): require(sha(archive+p)==h,'Uploaded source bytes changed: '+p)
    inventory=js(archive+'FILE_INVENTORY.json')
    mismatches=[r['path'] for r in inventory if sha(archive+r['path'])!=r['sha256'] or (root/archive/r['path']).stat().st_size!=r['bytes']]
    require(mismatches==['MANIFEST.json'],'Unexpected supplied inventory discrepancy')
    review=js('provenance/CHECKPOINT_22_SOURCE_REVIEW.json')
    require(review['inventory_mismatches'][0]['path']=='MANIFEST.json' and 'Preserve' in review['resolution'],'Stale inventory exception not documented')
    for ext in ('csv','json'):
        p='YELLOW_DIRECTOR_CALENDAR.'+ext
        require((root/'world-clock'/p).read_bytes()==(root/archive/p).read_bytes(),'Calendar source bytes differ: '+p)
    raw=rows('world-clock/YELLOW_DIRECTOR_CALENDAR.csv')
    require(raw==js('world-clock/YELLOW_DIRECTOR_CALENDAR.json'),'Source CSV/JSON differ (numeric strings are intentional)')
    calendar=[dict(r) for r in raw]
    for r in calendar:
        for k in ('week','day','kira_deterministic_credits','illi_deterministic_credits'): r[k]=int(r[k])
    require([(r['season'],r['week'],r['day']) for r in calendar]==[('Yellow',w,d) for w in range(1,8) for d in range(1,8)],'49 consecutive Yellow dates required')
    lookup={(r['week'],r['day']):r for r in calendar}
    trials={r['wave']:r['cumulative'] for r in js('trial-rewards/TRIAL_WAVE_CREDITS.json')}
    rewards=js('combat-rewards/COMBAT_REWARD_TABLES.json')
    counts=Counter(); totals={'illi':0,'kira':0}; arc4={'illi':0,'kira':0}
    by_kind=defaultdict(lambda:{'illi':0,'kira':0}); daily=[]; raid_bookings=[]; paid=set(); duo_dates=[]
    raids={(3,1):('normal',[],['Red']),(3,6):('normal',['Red'],['Orange']),
           (4,6):('normal',['Red','Orange'],[]),(6,1):('hard',['Red'],['Orange'])}
    noncombat={'Season transition','Arc Three close / Arc Four boundary','Recovery / open','Open','illi progression purchase',
       'Recovery / social beat','raeon tournament','First Builder party','raeon tournament window',
       'Kira Black acquisition — Genesis Orbs','Arc Four endpoint','Arc Five opening','Recovery',
       'Yellow seasonal Auction Day 1','Yellow seasonal Auction Day 2','Yellow seasonal Auction Day 3'}
    for row in calendar:
        kind=row['event']; date=(row['week'],row['day']); i=k=0
        if kind in ('Shared Duo Trial','Kira Solo Trial'):
            shared=kind=='Shared Duo Trial'
            counts['shared_W18_duo' if shared else 'kira_W18_solo']+=1
            require('W18' in row['result'] and 'W19' in row['result'] and 'fail' in row['result'].lower(),'Trial depth/result mismatch')
            require('full day' in row['duration_author_target'] and '21–38' in row['duration_author_target'],'Trial runtime shortened')
            k=trials[18];i=k if shared else 0
            if shared: duo_dates.append(f'Y{date[0]}D{date[1]}')
        elif kind=='Orange Dungeon session':
            m=re.fullmatch(r'(\d+) clears',row['result']);require(m is not None,'Orange count missing')
            n=int(m.group(1)); counts['orange_clears']+=n;counts['orange_sessions']+=1
            i=k=n*rewards['dungeons']['normal']['Orange']
        elif kind=='Yellow Dungeon push':
            counts['yellow_attempts']+=1;counts['yellow_failures']+=1
            require(row['result']=='FAIL' and 'OPEN' in row['notes'],'Yellow failed/partial boundary lost')
        elif kind=='Yellow Dungeon — Kira independent':
            counts['yellow_attempts']+=1;counts['kira_yellow_clears']+=1
            require(date==(4,2) and row['result']=='CLEAR','Independent first Yellow clear changed')
            k=rewards['dungeons']['normal']['Yellow']
        elif kind=='Progression-cohort Yellow farm':
            m=re.fullmatch(r'(\d+) clears',row['result']);n=int(m.group(1))
            counts['yellow_attempts']+=n;counts['kira_yellow_clears']+=n;counts['illi_yellow_clears']+=n
            i=k=n*rewards['dungeons']['normal']['Yellow']
            require(date==(5,3) and 'unnamed female peer' in row['notes'] and 'Y5D5' in row['notes'],'First Builder invitation missing')
        elif kind in ('Normal Raid attempt','Hard Raid attempt'):
            mode,cleared,failed=raids[date];counts[mode+'_raid_outings']+=1;entries=[]
            for boss in cleared:
                key=('Yellow',mode,boss);value=0 if key in paid else rewards['raids'][mode][boss]
                paid.add(key);k+=value;entries.append({'boss':boss,'credits_each':value})
            i=k;raid_bookings.append({'date':f'Y{date[0]}D{date[1]}','mode':mode,'cleared':entries,'failed':failed})
        elif kind=='domai excursion':
            counts['successful_domai_events']+=1
            require(date==(7,4) and row['result']=='Successful contribution; contextual group award'
                    and 'OPEN BY DESIGN' in row['notes'] and 'excluded' in row['notes'],'domai outcome/scope mismatch')
        elif kind in noncombat: counts['noncombat_rows']+=1
        else: require(False,'Unsupplied event: '+kind)
        require((row['illi_deterministic_credits'],row['kira_deterministic_credits'])==(i,k),'Payout mismatch: '+str(date))
        for who,value in (('illi',i),('kira',k)):
            totals[who]+=value;by_kind[kind][who]+=value
            if (1,3)<=date<=(6,3): arc4[who]+=value
        daily.append({'date':f'Y{date[0]}D{date[1]}','event':kind,'illi':i,'kira':k,'cumulative_fixed_gross':totals.copy()})
    expected={'shared_W18_duo':6,'kira_W18_solo':1,'orange_clears':17,'orange_sessions':5,'yellow_attempts':4,
              'yellow_failures':1,'kira_yellow_clears':3,'illi_yellow_clears':2,'normal_raid_outings':3,
              'hard_raid_outings':1,'successful_domai_events':1,'noncombat_rows':29}
    require(dict(counts)==expected,'Calendar counts mismatch')
    require(duo_dates==['Y1D3','Y2D2','Y3D3','Y4D4','Y6D5','Y6D6'],'Shared Trial dates mismatch')
    require(totals=={'illi':71280,'kira':80140} and arc4=={'illi':58170,'kira':67030},'Current fixed gross mismatch')
    require(paid=={('Yellow','normal','Red'),('Yellow','normal','Orange'),('Yellow','hard','Red')}
            and raid_bookings[2]['cleared'][0]['credits_each']==0,'Raid duplicate/higher boss award invented')
    require(lookup[(5,5)]['event']=='First Builder party' and lookup[(5,5)]['illi_deterministic_credits']==lookup[(5,5)]['kira_deterministic_credits']==0,'Y5D5 Trial not removed')
    require(lookup[(6,2)]['event']=='Kira Black acquisition — Genesis Orbs' and '61,017' in lookup[(6,2)]['notes'],'Exact Orb acquisition missing')
    require(lookup[(6,3)]['event']=='Arc Four endpoint' and lookup[(6,4)]['event']=='Arc Five opening','Arc boundary mismatch')
    require(lookup[(6,7)]['event']=='Recovery' and 'consecutive' in lookup[(6,7)]['notes'],'Recovery after consecutive Duos missing')
    for d in (1,2,3): require(lookup[(7,d)]['event']=='raeon tournament' and 'run ends by Y7D3' in lookup[(7,d)]['result'],'Personal tournament block changed')
    for d in (5,6,7): require(lookup[(7,d)]['event']==f'Yellow seasonal Auction Day {d-4}' and 'exact intraday time OPEN' in lookup[(7,d)]['duration_author_target'],'Auction infrastructure changed')
    require(lookup[(5,1)]['event']=='raeon tournament' and lookup[(5,6)]['event']=='raeon tournament window','Earlier qualification/availability lost')
    # Reconcile every older row. Only four dates receive source-author changes.
    old_calendar=js('world-clock/ARC4_YELLOW_COMBAT_CALENDAR.json'); changed=[]
    for old in old_calendar:
        date=(old['week'],old['day'])
        if old!=lookup[date]: changed.append(date)
    require(changed==[(5,3),(5,5),(6,2),(6,3)],'Unexpected change to CP21 overlapping dates')
    require(all('Green Dungeon' not in r['kira_activity']+r['illi_activity'] for r in calendar),'Invented dated Green Dungeon')
    handoff=js('world-clock/ARC4_HANDOFF.json'); arc5=js('world-clock/ARC5_HANDOFF.json')
    require(handoff['kira_orbs']['date']=='Y6D2' and handoff['kira_orbs']['price']==61017,'Orb date/price mismatch')
    require(handoff['arc4_deterministic_gross']==arc4 and handoff['yellow_deterministic_gross']==totals,'Handoff income mismatch')
    require(arc5['start']=='Y6D4' and arc5['close']=={'date':'G6D2','purchase':'Coherence Prime Elemental Red','cost':9350},'Arc Five boundary/cost mismatch')
    require(arc5['illi_opening']=={'Persistent Coherence':'Blue','Absorption Shield':'Red','Genesis Beam':'Green','Genesis Prime Elemental':'Red'},'illi opening ranks changed')
    require(arc5['genesis_prime_rank_dates'] is None and arc5['new_persistent_coherence_purchase_required'] is False,'Invented rank/purchase requirement')
    require(arc5['kira_solo']['cleared_wave']==19 and arc5['kira_solo']['reached_wave']==20
            and arc5['kira_solo']['first_blue_clear_date'] is None and arc5['kira_solo']['w20_failure_depth'] is None,'Blue Solo direction/date boundary lost')
    require(arc5['duo']=={'cleared_wave':18,'failed_wave':19} and arc5['meaningful_trio_push'] is False and arc5['trio_partner'] is None,'Duo/Trio scope changed')
    require(arc5['green_dungeon']['first_attempt_date'] is None and arc5['green_dungeon']['first_clear_date'] is None,'Invented Green Dungeon date')
    require(arc5['mastery']=={'ordinary_paid_rank_ladder':False,'defined_mastery_ceiling':None,'intrinsic_orb_range_cutoff':None,'late_integrated_system_unlocked_in_arc5':False},'Black mastery boundary lost')
    require(arc5['one_orb_stage']['orbs']==1 and arc5['one_orb_stage']['working_radius_feet']==11
            and arc5['one_orb_stage']['radius_status'].startswith('WORKING'),'One-Orb stage changed')
    ledger=js('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json')
    require(len(ledger)==17 and sum(r['cost'] for r in ledger)==250884,'17-event ledger changed')
    prime=next(r for r in ledger if r['purchase_or_upgrade']=='Coherence Prime → Red')
    require((prime['season'],prime['week'],prime['day'],prime['cost'])==('Green',6,2,9350),'Coherence Prime moved/repriced')
    group=js('combat-rewards/DOMAI_GROUP_ECONOMY.json'); participant=js('combat-rewards/DOMAI_PARTICIPATION_RULES.json')
    require(group['base_member_share']=='group_award / eligible_members' and group['individual_share_after_deaths']=='base_member_share * 0.8^deaths','Group/death allocation changed')
    require(group['small_group_size_bonus'] is False and group['optional_individual_bonus'] is None
            and group['rounding_and_bonus_interaction']=='OPEN','Bonus/scoring invented')
    require(group['yellow_event']['date']=='Y7D4' and group['yellow_event']['aggregate_award'] is None
            and group['yellow_event']['base_split_each']==0.5,'Y7D4 payout invented')
    require(participant['eligibility_days']==7 and participant['eligibility_starts']=='first validated eldris kill'
            and participant['recovery_full_days']==1 and participant['recovery_scope']=='same domai'
            and participant['death_multiplier_per_death']==0.8,'Existing participation rules changed')
    registry_counts={'bindings':len(js('bindings/BINDINGS.json')),'summons':len(js('summons/SUMMONED_ENTITIES.json')),'builder_paths':len(js('builder/paths/PATHS.json'))}
    require(registry_counts=={'bindings':1016,'summons':229,'builder_paths':200},'Registry counts changed')
    families=Counter(r['role_family'] for r in js('builder/paths/PATHS.json'))
    require(families=={'Combat Medic':30,'Augmenter':45,'Maege':65,'Summoner':60},'Builder paths reclassified')
    protected=[]
    for p,h in before['sha256'].items():
        keep=(p.startswith(('provenance/','prior-checkpoint-source/','bindings/','summons/','trial-rewards/','builder/encounters/'))
              or (p.startswith('builder/paths/') and not p.endswith('/README.md'))
              or (p.startswith('combat-rewards/') and p.endswith(('.json','.csv')))
              or bool(re.fullmatch(r'live-model/\d+_CHECKPOINT_.*\.md',p))
              or p=='live-model/ELDRIS_REFERENCE.md'
              or p in ['world-clock/'+n for n in ('WORLD_CLOCK_TEMPLATE.csv','PRISM_TEAM_TRACKER.csv','ILLI_PROGRESSION_SKELETON.csv','ILLI_PROGRESSION_SKELETON.json','ILLI_AUTHOR_PROGRESSION_LEDGER.csv','ILLI_AUTHOR_PROGRESSION_LEDGER.json','RED_TO_ORANGE_COMBAT_CALENDAR.csv','RED_TO_ORANGE_COMBAT_CALENDAR.json','ARC3_ORANGE_CALENDAR.csv','ARC3_ORANGE_CALENDAR.json','ARC4_YELLOW_COMBAT_CALENDAR.csv','ARC4_YELLOW_COMBAT_CALENDAR.json')])
        if keep:
            require(sha(p)==h,'Protected baseline bytes changed: '+p);protected.append(p)
    # The exact late-cycle carry section must survive, not merely its title.
    old_partner=subprocess.check_output(['git','-c',f'safe.directory={root.as_posix()}','show',before['baseline_commit']+':live-model/PARTNERSHIP_AND_CARRY.md'],cwd=root).decode('utf-8')
    def carry_section(s): return re.search(r'(?ms)^## Project Princess Carry — LOCK\n.*?(?=^## )',s).group(0)
    require(carry_section(old_partner)==carry_section(text('live-model/PARTNERSHIP_AND_CARRY.md')),'Project Princess Carry section altered')
    promotions={'TRAINING_YARD.md':'live-model/TRAINING_YARD.md','BUILDER_COMMUNITY.md':'builder/COMMUNITY.md',
      'KIRA_BLACK_SYSTEMS_ARC5.md':'live-model/BLACK_SYSTEMS_MASTERY.md','ARC5_HANDOFF_ROADMAP.md':'world-clock/ARC5_HANDOFF.md',
      'DOMAI_GROUP_ECONOMY.md':'combat-rewards/DOMAI_GROUP_ECONOMY.md','CHECKPOINT22_LIVE_MODEL_DELTA.md':'live-model/29_CHECKPOINT_22_ARC5_SOCIAL_MASTERY.md'}
    for source,target in promotions.items(): require(text(target).endswith(text(archive+source)),'Incomplete promoted author source: '+source)
    content={
      'live-model/TRAINING_YARD.md':['inter-wave break','no voluntary mid-combat exit','already completed/unlocked','do **not** award Trial credits','official standing/unlocking','start at W1'],
      'builder/COMMUNITY.md':['200','create a hypothetical build','save multiple builds','publish/share','like/dislike','Trending','Valnak Recommended','No mandatory','Elara publishes','Y5D3','Y5D5','female peer'],
      'live-model/BLACK_SYSTEMS_MASTERY.md':['No defined mastery ceiling','no defined intrinsic range cutoff','slow, drift, hover','11-foot radius','NOT a force-field Binding','W19 Blue clear','W20 reached','W18 clear / W19 Blue fail','3–4 groups','hundreds of yards/meters','Do not back-port'],
      'world-clock/ARC5_HANDOFF.md':['Y6D2','9,350','distributed damage','not automatically','second autonomous helkir','Tiara Fund','20–40','17–45','50s/60s','Exact biology','first third','burnout'],
      'live-model/DOMAI_PARTICIPATION.md':['group_award / eligible_members','AUTHOR ONLY','Y7D4','0.8^deaths','OPEN'],
      'live-model/SOCIAL_LIFE_AND_FOUNDATIONS.md':['female peer','Y5D5','23,000 each, two per girl','WORKING','booking remain OPEN'],
      'live-model/OPEN.md':['W19 Blue Solo','first Green Dungeon attempt/clear','official-standing/unlocking','Tiara Fund','Exact Halo day','Y6D2'],
    }
    for p,phrases in content.items():
        s=text(p).lower()
        for phrase in phrases: require(phrase.lower() in s,'Content missing: '+p+': '+phrase)
    inputs=['world-clock/YELLOW_DIRECTOR_CALENDAR.csv','world-clock/YELLOW_DIRECTOR_CALENDAR.json','world-clock/ARC4_HANDOFF.json',
      'world-clock/ARC5_HANDOFF.json','combat-rewards/DOMAI_GROUP_ECONOMY.json','world-clock/validate_yellow_director.py',*content]
    return {'checkpoint':22,'scope':'Current full Yellow director calendar and Arc Five direction','result':'FAIL' if errors else 'PASS','errors':errors,
      'baseline_commit':before['baseline_commit'],'calendar_rows':len(calendar),'counts':dict(counts),'shared_duo_dates':duo_dates,
      'fixed_full_yellow_income_excluding_domai':totals,'revised_arc4_income_through_Y6D3':arc4,'daily_fixed_gross':daily,'income_by_event':dict(by_kind),
      'raid_bookings':raid_bookings,'changed_cp21_dates':[f'Y{w}D{d}' for w,d in changed],'gross_is_not_balance':True,
      'exact_orbs':'Y6D2','arc4_close':'Y6D3','arc5_open':'Y6D4','arc5_close':'G6D2 Coherence Prime Red, 9350',
      'personal_raeon_block':'Y7D1–D3; run ends by D3; exact matches/elimination OPEN','domai_award':'Y7D4 successful; exact group award OPEN and excluded',
      'registry_counts':registry_counts,'builder_role_counts':dict(families),'illi_events':len(ledger),'illi_total':250884,
      'project_princess_carry_section_byte_identical':True,'open_blue_solo_date':None,'open_green_dungeon_dates':None,
      'source_inventory_exception':'Supplied MANIFEST inventory entry is stale; all 16 actual ZIP members archived exactly',
      'protected_baseline_files':protected,'sha256':{p:sha(p) for p in inputs}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write-audit',action='store_true')
    args=parser.parse_args()
    try: report=audit(args.repository.resolve())
    except (OSError,KeyError,ValueError,TypeError,IndexError,AttributeError,StopIteration,subprocess.CalledProcessError) as exc:
        report={'result':'FAIL','errors':[str(exc)]}
    if args.write_audit and report['result']=='PASS':
        (args.repository/'world-clock/YELLOW_DIRECTOR_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('daily_fixed_gross','income_by_event','protected_baseline_files','sha256')},indent=2,ensure_ascii=False))
    return 0 if report['result']=='PASS' else 1


if __name__=='__main__': raise SystemExit(main())
