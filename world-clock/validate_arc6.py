"""Validate CP24 Arc Six calendar, reserve, current progression and preserved canon."""
import argparse
from collections import Counter, defaultdict
import csv
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "validation"))
from validate_clock_promotion import current_clock_baseline, validated_replacements


def audit(root):
    errors=[]
    def require(ok,msg):
        if not ok: errors.append(msg)
    def text(p): return (root/p).read_text(encoding='utf-8-sig')
    def js(p): return json.loads(text(p))
    def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
    def rows(p):
        with (root/p).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
    before=js('provenance/CHECKPOINT_24_BEFORE_REVIEW.json')
    def old(p): return subprocess.check_output(['git','-c',f'safe.directory={root.as_posix()}','show',before['baseline_commit']+':'+p],cwd=root)
    archive='provenance/checkpoint-24-package/'
    require(set(before['package_source_sha256'])=={p.name for p in (root/archive).iterdir()} and len(before['package_source_sha256'])==16,'Package membership mismatch')
    for p,h in before['package_source_sha256'].items(): require(sha(archive+p)==h,'Source bytes changed: '+p)
    for item in js(archive+'FILE_INVENTORY.json'): require(sha(archive+item['path'])==item['sha256'] and (root/archive/item['path']).stat().st_size==item['bytes'],'Inventory mismatch: '+item['path'])
    pairs={
        'ARC6_DIRECTOR_CALENDAR':('ARC6_DIRECTOR_CALENDAR',['week','day','kira_income','illi_income','illi_progression_spend','kira_progression_spend']),
        'ARC6_ILLI_CREDIT_LEDGER':('ARC6_ILLI_CREDIT_LEDGER',['income','progression_spend','running_progression_reserve']),
        'ILLI_AUTHOR_PROGRESSION_LEDGER':('ILLI_PROGRESSION_LEDGER_REPLACEMENT',['week','day','cost','cumulative_progression_spend'])}
    for target,(source,numeric) in pairs.items():
        for ext in ('csv','json'): require((root/f'world-clock/{target}.{ext}').read_bytes()==(root/f'{archive}{source}.{ext}').read_bytes(),'Promoted source differs: '+target+'.'+ext)
        converted=rows('world-clock/'+target+'.csv')
        for row in converted:
            for key in numeric: row[key]=int(row[key])
        require(converted==js('world-clock/'+target+'.json'),'CSV/JSON differs: '+target)
    calendar=js('world-clock/ARC6_DIRECTOR_CALENDAR.json')
    date=lambda r:f"{r['season'][0]}{r['week']}D{r['day']}"
    dates=[date(r) for r in calendar]
    expected_dates=[f'G6D{d}' for d in range(3,8)]+[f'G7D{d}' for d in range(1,8)]+[f'B{w}D{d}' for w in range(1,6) for d in range(1,8)]+['B6D1','B6D2','B6D3']
    require(dates==expected_dates and len(set(dates))==50,'50 consecutive Arc Six dates required')
    lookup=dict(zip(dates,calendar));rewards=js('combat-rewards/COMBAT_REWARD_TABLES.json')
    trials={r['wave']:r['cumulative'] for r in js('trial-rewards/TRIAL_WAVE_CREDITS.json')}
    purchases={'G6D4':('Genesis Prime → Orange',14960),'G7D2':('Genesis Prime → Yellow',26928),'B1D3':('Absorption Shield → Orange',14960),'B2D4':('Absorption Shield → Yellow',26928),'B5D6':('Absorption Shield → Green',56549),'B6D3':('Resonance Prime / Juggernaut → Red',9350)}
    solos={'G7D3':11,'G7D4':12,'B1D1':13};duos={'G6D7':18,'B2D2':19,'B6D2':20}
    green_dates=['G7D1','B1D2','B1D4','B1D6','B2D6','B3D1','B3D4','B4D2','B4D6']
    domai={'G6D3':('Orange',60000,30000),'B5D4':('Yellow',30000,15000)}
    raids={'B2D3':('normal',['Red A','Orange A','Yellow']), 'B3D2':('hard',['Red','Orange']), 'B4D3':('hard',['Red','Orange']), 'B5D3':('hard',['Red','Orange','Yellow'])}
    counts=Counter();totals={'kira':0,'illi':0};spend={'kira':0,'illi':0};category=defaultdict(lambda:{'kira':0,'illi':0});paid=set();raid_bookings=[];daily=[]
    noncombat={'illi progression purchase','Builder Night','Seasonal Auction','Kira Black acquisition','Veteran credibility beat','Recovery','Arc Six endpoint'}
    for day,row in zip(dates,calendar):
        k=i=0;kind='noncombat';event=row['event'];result=row['result']
        require(row['status'].startswith('LOCKED'),'Unlocked source row: '+day)
        if event=='Shared Duo Trial':
            kind='duo'
            if day in duos:
                wave=duos[day];k=i=trials[wave];counts['duo_outings']+=1
                require(f'W{wave}' in result and 'clear' in result.lower() and f'W{wave+1}' in result and 'fail' in result.lower(),'Duo outcome mismatch: '+day)
            else: require(day in ('B2D1','B6D1') and 'underway' in result,'Unplanned Trial/start row: '+day)
        elif event=='illi Solo Trial':
            require(day in solos,'Extra Solo');wave=solos[day];i=trials[wave];kind='illi_solo';counts['illi_solo']+=1
            require(f'W{wave}' in result and 'clear' in result.lower() and f'W{wave+1}' in result and 'fails' in result,'Solo wave mismatch')
        elif event=='Dungeon session':
            require(day=='G6D6' and result=='2 Yellow clears','Unexpected Yellow session');k=i=2*rewards['dungeons']['normal']['Yellow'];kind='yellow_dungeon';counts['yellow_clears']+=2
        elif event=='Green Dungeon':
            require(day in green_dates and result=='CLEAR','Unexpected Green clear');k=i=rewards['dungeons']['normal']['Green'];kind='green_dungeon';counts['green_clears']+=1
            require(row['runtime_author_target']=='12–21 h','Green runtime changed')
        elif event=='Blue Dungeon':
            require(day in ('B3D6','B3D7','B5D1','B5D2'),'Unexpected Blue day');kind='blue_dungeon'
            if day=='B3D6': counts['blue_attempts']+=1
            if day=='B3D7': require(result=='FAIL','Blue failure changed');counts['blue_failures']+=1
            if day=='B5D1': counts['blue_attempts']+=1
            if day=='B5D2': require(result=='FIRST BLUE DUNGEON CLEAR','First Blue clear changed');k=i=rewards['dungeons']['normal']['Blue'];counts['blue_clears']+=1
        elif event in ('Normal Raid outing','Hard Raid'):
            kind='raid'
            if day in raids:
                mode,bosses=raids[day];counts[mode+'_raid_outings']+=1;entries=[]
                for boss in bosses:
                    identity=('Blue',mode,boss);amount=0 if identity in paid else rewards['raids'][mode][boss.split()[0]]
                    paid.add(identity);k+=amount;entries.append({'boss':boss,'each':amount})
                i=k;raid_bookings.append({'date':day,'mode':mode,'bosses':entries,'each_total':k})
            else: require(day=='B4D4' and result=='Hard Yellow deep FAIL','Unplanned Raid completion')
            if day=='B2D3': require(result=='Normal Red A + Orange A + Yellow clear; Green fails','Normal Raid ceiling changed')
            if day=='B3D2': require(result=='Hard Red + Orange clear; Hard Yellow FAIL','Hard first attempt changed')
            if day=='B5D3': require(result=='Hard Yellow CLEAR; Hard R/O repeats','Hard Yellow milestone changed')
        elif event in ('Orange domai','Yellow domai'):
            rank,group,each=domai[day];require(event==rank+' domai' and result.startswith('SUCCESS') and group==each*2,'Specific domai mismatch');k=i=each;kind='specific_domai';counts['domai_successes']+=1
        elif event in noncombat:counts['noncombat_rows']+=1
        else:require(False,'Unexpected event '+event)
        expected_i_spend=purchases[day][1] if day in purchases else 0;expected_k_spend=61017 if day=='B1D5' else 0
        require((row['kira_income'],row['illi_income'],row['illi_progression_spend'],row['kira_progression_spend'])==(k,i,expected_i_spend,expected_k_spend),'Income/spend mismatch: '+day)
        for who,value in (('kira',k),('illi',i)):
            totals[who]+=value;category[kind][who]+=value;spend[who]+=row[who+'_progression_spend']
        daily.append({'date':day,'kira':k,'illi':i,'illi_spend':expected_i_spend,'illi_progression_reserve':totals['illi']-spend['illi']})
        require(daily[-1]['illi_progression_reserve']>=0,'Negative earmarked reserve: '+day)
    require(totals=={'kira':148600,'illi':157065} and spend=={'kira':61017,'illi':149675},'Arc Six totals mismatch')
    require({k:counts[k] for k in ('duo_outings','illi_solo','yellow_clears','green_clears','blue_attempts','blue_failures','blue_clears','normal_raid_outings','hard_raid_outings','domai_successes')}=={'duo_outings':3,'illi_solo':3,'yellow_clears':2,'green_clears':9,'blue_attempts':2,'blue_failures':1,'blue_clears':1,'normal_raid_outings':1,'hard_raid_outings':3,'domai_successes':2},'Combat counts mismatch')
    require([r['each_total'] for r in raid_bookings]==[11250,9375,0,7500],'Repeated Raid bosses double-paid')
    require(raid_bookings[-1]['bosses'][:2]==[{'boss':'Red','each':0},{'boss':'Orange','each':0}],'Hard repeats paid again')
    for start,end in [('B2D1','B2D2'),('B6D1','B6D2'),('B3D6','B3D7'),('B5D1','B5D2'),('B4D3','B4D4')]:
        require(dates.index(end)==dates.index(start)+1 and lookup[start]['kira_income']==lookup[start]['illi_income']==0,'Multi-day booking mismatch')
    reserve=js('world-clock/ARC6_ILLI_CREDIT_LEDGER.json');expected_transactions=[d for d in daily if d['illi'] or d['illi_spend']]
    require(len(reserve)==len(expected_transactions)==28,'Reserve transaction count mismatch')
    for transaction,d in zip(reserve,expected_transactions):
        require((transaction['date'],transaction['income'],transaction['progression_spend'],transaction['running_progression_reserve'])==(d['date'],d['illi'],d['illi_spend'],d['illi_progression_reserve']),'Reserve mismatch: '+d['date'])
        require(transaction['kind']==('purchase' if d['illi_spend'] else 'income'),'Reserve kind mismatch')
    require(reserve[-1]['running_progression_reserve']==7390,'Ending reserve mismatch')
    ledger=js('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json');old_ledger=json.loads(old('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json'))
    require(ledger[:13]==old_ledger[:13] and len(ledger)==19,'First 13 events changed or missing six-event tail')
    require([(date(r),r['purchase_or_upgrade'],r['cost']) for r in ledger[13:]]==[(d,p,c) for d,(p,c) in purchases.items()],'Replacement tail mismatch')
    bind={r['name']:r for r in js('bindings/BINDINGS.json')};prime={r['name']:r for r in js('summons/PRIME_ELEMENTAL_PRICING.json')}
    name_map={'Genesis Prime':'Genesis Prime Elemental','Coherence Prime':'Coherence Prime Elemental','Resonance Prime / Juggernaut':'Resonance Prime Elemental'}
    cumulative=0;accepted=False
    for r in ledger:
        if r['purchase_or_upgrade']=='Accept White Legacy':cost=0;accepted=True
        else:
            name,rank=r['purchase_or_upgrade'].split(' → ');value=(prime[name_map[name]] if name in name_map else bind[name])[rank]
            cost=int((Decimal(value)*(Decimal('0.55') if accepted else Decimal(1))).quantize(Decimal(1),rounding=ROUND_HALF_UP))
        cumulative+=cost;require((r['cost'],r['cumulative_progression_spend'])==(cost,cumulative),'Pricing/cumulative error: '+r['purchase_or_upgrade'])
    require(cumulative==292772 and sum(r['cost'] for r in ledger[13:])==149675,'Progression sum mismatch')
    skeleton=js('world-clock/ILLI_PROGRESSION_SKELETON.json');old_skeleton=json.loads(old('world-clock/ILLI_PROGRESSION_SKELETON.json'))
    require(skeleton[:13]==old_skeleton[:13] and len(skeleton)==19,'Skeleton prefix/count mismatch')
    skcsv=rows('world-clock/ILLI_PROGRESSION_SKELETON.csv')
    for row in skcsv:row['week']=int(row['week']);row['day']=int(row['day'])
    require(skcsv==skeleton,'Skeleton CSV/JSON differ')
    for row,sk in zip(ledger,skeleton):
        require((row['season'],row['week'],row['day'])==(sk['season'],sk['week'],sk['day']),'Skeleton date mismatch')
        if row['purchase_or_upgrade']=='Accept White Legacy': require(sk['event']=='Accept' and sk['binding']=='White Legacy','Legacy skeleton mismatch')
        else:
            name,rank=row['purchase_or_upgrade'].split(' → ')
            binding={'Genesis Prime':'Genesis Prime Elemental','Coherence Prime':'Coherence Prime Elemental','Resonance Prime / Juggernaut':'Resonance Prime Elemental / Juggernaut'}.get(name,name)
            require(sk['binding']==binding and sk['result']==rank and sk['event']==('Acquire' if rank=='Red' else 'Rank'),'Skeleton event mismatch')
    for name in ('ILLI_AUTHOR_PROGRESSION_LEDGER.csv','ILLI_AUTHOR_PROGRESSION_LEDGER.json','ILLI_PROGRESSION_SKELETON.csv','ILLI_PROGRESSION_SKELETON.json'):
        require((root/'provenance/checkpoint-24-baseline'/name).read_bytes()==old('world-clock/'+name),'Archived old progression changed')
    # Preserve standing clocks exactly; CP24 plus CP25 changes affect only authored character-overlay weeks.
    weekly=rows('world-clock/WORLD_CLOCK_TEMPLATE.csv');old_weekly=list(csv.DictReader(old('world-clock/WORLD_CLOCK_TEMPLATE.csv').decode().splitlines()));changed=[]
    promoted_prose = set()
    try:
        old_weekly = current_clock_baseline(root, old_weekly)
        promoted_prose = validated_replacements(root)
    except (OSError, ValueError, KeyError) as exc:
        require(False, 'R2/R3 promotion: ' + str(exc))
    require(len(weekly)==len(old_weekly)==49,'Weekly clock size changed')
    for a,b in zip(old_weekly,weekly):
        require(all(a[k]==b[k] for k in a if k not in ('kira_clock','illi_clock')),'Standing schedule changed')
        if a!=b:changed.append((b['season'],int(b['week'])))
    require(changed==[('Green',6),('Green',7),('Blue',1),('Blue',2),('Blue',5),('Blue',6),('Blue',7)]+[('Violet',w) for w in range(1,8)]+[('White',w) for w in range(1,8)],'Character overlay scope mismatch')
    for week in weekly:
        if week['season']=='Violet' and week['week'] in ('1','2'):require(week['illi_clock']=='','Stale Violet purchase overlay')
    scales={r['dungeon_rank']:r['target_runtime'] for r in rows('builder/encounters/NORMAL_DUNGEON_AUTHOR_SCALE.csv')}
    require([scales[k] for k in ('Yellow','Green','Blue')]==['5–10 hr','12–21 hr','25–42 hr'],'Dungeon runtime tables changed')
    require(lookup['G6D6']['runtime_author_target']=='10–20 h total' and all('25–42' in lookup[d]['runtime_author_target'] for d in ('B3D6','B5D1')),'Runtime blocks missing')
    require('3.5–6 hours' in text('live-model/COMBAT_THRESHOLDS.md'),'Blue-wave timing lost')
    state=js('world-clock/ARC6_HANDOFF.json')
    require(state['start']=='G6D3' and state['close']=={'date':'B6D3','purchase':'Resonance Prime Elemental Red','cost':9350} and state['arc7_open']=='B6D4','Arc boundaries mismatch')
    require(state['gross']==totals and state['illi_progression_reserve']=={'start':0,'income':157065,'spend':149675,'end':7390,'scope':'Earmarked progression only, not actual bank balance'},'Reserve scope mismatch')
    require(state['illi_graduation']=={'date':'B1D1','cleared_wave':13,'failed_wave':14,'failure_depth':None,'independent_solo':True},'Graduation mismatch')
    require(state['illi_solo']==[{'date':d,'clear':w,'fail':w+1} for d,w in solos.items()],'Solo handoff mismatch')
    require(state['duo']==[{'start':'G6D7','end':'G6D7','clear':18,'fail':19},{'start':'B2D1','end':'B2D2','clear':19,'fail':20},{'start':'B6D1','end':'B6D2','clear':20,'fail':21}],'Duo handoff mismatch')
    require(state['blue_dungeons']==[{'start':'B3D6','end':'B3D7','result':'FAIL','partial_reward':None},{'start':'B5D1','end':'B5D2','result':'FIRST CLEAR','each_completion_reward':7800}],'Blue handoff mismatch')
    require(state['halo']=={'date':'B1D5','cost':61017,'solvent_by_author':True,'zero_start_solvency_asserted':False,'mastery_not_implied':True},'Halo solvency/mastery boundary mismatch')
    require(state['domain']=={'window':'Late Violet','date':None} and state['arc7_later_calendar'] is None and state['raid_runtime'] is None,'Unresolved boundary filled')
    require(state['dungeon_runtime_hours']=={'Yellow':[5,10],'Green':[12,21],'Blue':[25,42]},'Handoff runtime mismatch')
    require(state['specific_domai_awards']==[{'date':d,'rank':rank,'group':group,'each':each} for d,(rank,group,each) in domai.items()],'Specific awards mismatch')
    require(state['illi_endpoint']=={'Persistent Coherence':'Blue','Absorption Shield':'Green','Genesis Beam':'Green','Genesis Prime':'Yellow','Coherence Prime':'Red','Resonance Prime':'Red'},'Endpoint architecture mismatch')
    require(not any(state[k] for k in ('trio','violet_dungeon_attempted','normal_green_raid_clear','hard_green_raid_clear')),'Content ceiling exceeded')
    nights=[d for d,row in lookup.items() if 'Builder Night' in row['kira_activity']]
    require(nights==state['builder_nights']==['G6D5','B1D5','B2D5','B3D5','B4D5','B5D5'],'Builder nights changed')
    require(all(lookup[f'G7D{d}']['event']=='Seasonal Auction' for d in (5,6,7)),'Green Auction displaced')
    price=js('economy/KIRA_BLACK_ACQUISITION_PRICES.json');old_price=json.loads(old('economy/KIRA_BLACK_ACQUISITION_PRICES.json'))
    require({k:v for k,v in price.items() if k!='acquisition_dates'}=={k:v for k,v in old_price.items() if k!='acquisition_dates'},'Black prices changed')
    require('B1D5' in price['acquisition_dates'] and 'Domain day OPEN' in price['acquisition_dates'],'Current price timing stale')
    protected=[]
    for p,digest in before['sha256'].items():
        keep=(p.startswith(('provenance/','prior-checkpoint-source/','trial-rewards/','builder/'))
              or (p.startswith(('bindings/','summons/')) and p!='bindings/PRICING_MODEL.md')
              or (p.startswith('combat-rewards/') and p!='combat-rewards/README.md')
              or re.match(r'live-model/\d+_CHECKPOINT_',p)
              or p in ('live-model/TRAINING_YARD.md','live-model/BLACK_SYSTEMS_MASTERY.md','world-clock/ARC5_HANDOFF.md','world-clock/ARC5_HANDOFF.json','world-clock/ARC5_DIRECTOR_CALENDAR.md','world-clock/ARC5_DIRECTOR_CALENDAR.csv','world-clock/ARC5_DIRECTOR_CALENDAR.json','world-clock/PRISM_TEAM_TRACKER.csv')
              or (p.startswith('world-clock/') and 'CALENDAR' in p and p.endswith(('.csv','.json')) and 'AUDIT' not in p))
        # CP25 checks unchanged reward numbers/participant fields and exact prior Black doctrine prefix.
        if keep and p not in promoted_prose and p not in {'trial-rewards/README.md', 'live-model/BLACK_SYSTEMS_MASTERY.md', 'combat-rewards/validate_rewards.py', 'combat-rewards/DOMAI_PARTICIPATION_RULES.json', 'combat-rewards/COMBAT_REWARD_TABLES.json'}:require(sha(p)==digest,'Protected baseline altered: '+p);protected.append(p)
    carry=re.compile(r'(?ms)^## Project Princess Carry — LOCK\n.*?(?=^## )')
    require(carry.search(old('live-model/PARTNERSHIP_AND_CARRY.md').decode()).group()==carry.search(text('live-model/PARTNERSHIP_AND_CARRY.md')).group(),'Project Princess Carry altered')
    require(text('live-model/31_CHECKPOINT_24_ARC6_GRADUATION.md').endswith(text(archive+'CHECKPOINT24_LIVE_MODEL_DELTA.md')),'Author delta incomplete')
    registry={'bindings':len(js('bindings/BINDINGS.json')),'summons':len(js('summons/SUMMONED_ENTITIES.json')),'builder_paths':len(js('builder/paths/PATHS.json'))}
    require(registry=={'bindings':1016,'summons':229,'builder_paths':200},'Registry counts changed')
    content={'live-model/ILLI_PROGRESSION.md':['19','292,772','B1D1','B5D6','B6D3','Genesis Prime Yellow','7,390'],
      'live-model/PRIME_ELEMENTALS.md':['B6D3','frontline','Genesis Prime','Coherence Prime','Resonance Prime'],
      'live-model/COMBAT_ECOLOGY.md':['Eligibility is not credibility','PUG','no item-level','Violet is not attempted','B3D6–D7','B5D1–D2'],
      'live-model/01_KIRA.md':['B1D5','61,017','two-Orb','Domain stays Late Violet'],
      'live-model/PARTNERSHIP_AND_CARRY.md':['B1D1','economic precursor','service/community','G6D5'],
      'live-model/DOMAI_PARTICIPATION.md':['60,000 collective / 30,000 each','30,000 collective / 15,000 each','7-day','one full day','0.8^deaths','AUTHOR ONLY'],
      'live-model/OPEN.md':['W14 failure depth','W21 depth','personal Blue-season raeon','later Arc Seven','Domain day in Late Violet','Halo mastery']}
    for p,phrases in content.items():
        for phrase in phrases:require(phrase.lower() in text(p).lower(),'Content missing: '+p+': '+phrase)
    inputs=['world-clock/ARC6_DIRECTOR_CALENDAR.json','world-clock/ARC6_ILLI_CREDIT_LEDGER.json','world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json','world-clock/ILLI_PROGRESSION_SKELETON.json','world-clock/WORLD_CLOCK_TEMPLATE.csv','world-clock/ARC6_HANDOFF.json','world-clock/validate_arc6.py','economy/KIRA_BLACK_ACQUISITION_PRICES.json',*content]
    return {'checkpoint':24,'result':'FAIL' if errors else 'PASS','errors':errors,'baseline_commit':before['baseline_commit'],'arc':'G6D3→B6D3','arc7_open':'B6D4','calendar_rows':len(calendar),'counts':dict(counts),'gross':totals,'progression_spend':spend,'income_by_category':dict(category),'daily_accounting':daily,'reserve_transactions':len(reserve),'illi_earmarked_start':0,'illi_earmarked_end':reserve[-1]['running_progression_reserve'],'minimum_post_purchase_reserve':min(r['running_progression_reserve'] for r in reserve if r['kind']=='purchase'),'illi_events':len(ledger),'illi_cumulative_spend':cumulative,'first_13_events_unchanged':True,'raid_bookings':raid_bookings,'domai_awards':state['specific_domai_awards'],'builder_nights':nights,'clock_changed_weeks':changed,'standing_clock_fields_unchanged_except_authorized_highlights':True,'runtime_hours':{'Yellow':[5,10],'Green':[12,21],'Blue':[25,42],'W18':[21,38],'each_Blue_wave':[3.5,6],'W19_before_failure':[24.5,44],'W20_before_failure':[28,50],'raid':None},'arc5_calendar_data_and_handoff_byte_identical':True,'project_princess_carry_section_byte_identical':True,'registries':registry,'protected_baseline_files':protected,'sha256':{p:sha(p) for p in sorted(set(inputs))}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write-audit',action='store_true')
    args=parser.parse_args()
    try:report=audit(args.repository.resolve())
    except (OSError,KeyError,ValueError,TypeError,IndexError,AttributeError,StopIteration,subprocess.CalledProcessError) as exc:report={'result':'FAIL','errors':[str(exc)]}
    if args.write_audit and report['result']=='PASS':(args.repository/'world-clock/ARC6_DIRECTOR_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('daily_accounting','protected_baseline_files','sha256')},indent=2,ensure_ascii=False))
    return 0 if report['result']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
