"""Validate Checkpoint 19 source fidelity, events, earnings, reserves and scheduling."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
BASELINE = '4982fd6ff43faaf1bf0e5fdd289d0831951e1ef4'


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "validation"))
from validate_clock_promotion import current_clock_baseline, validated_replacements


def audit(root):
    errors = []
    def require(ok, message):
        if not ok: errors.append(message)
    def js(path): return json.loads((root/path).read_text(encoding='utf-8-sig'))
    def rows(path):
        with (root/path).open(encoding='utf-8-sig', newline='') as stream:
            return list(csv.DictReader(stream))
    def old(path):
        return subprocess.check_output(['git','-c',f'safe.directory={root.as_posix()}',
                                       'show',f'{BASELINE}:{path}'],cwd=root)
    archive = 'provenance/checkpoint-19-package/'
    manifest = js(archive+'FINAL_MANIFEST.json')
    expected_sources = set(manifest['files']) | {'FINAL_MANIFEST.json'}
    require({p.name for p in (root/archive).iterdir()} == expected_sources, 'Source archive file set mismatch')
    source_rows = js(archive+'ARC3_ORANGE_CALENDAR.json')
    calendar = rows('world-clock/ARC3_ORANGE_CALENDAR.csv')
    for row in calendar:
        for field in ('week','day','illi_credit','kira_credit'): row[field] = int(row[field])
    require(calendar == js('world-clock/ARC3_ORANGE_CALENDAR.json') == source_rows, 'Calendar mirrors/source differ')
    for suffix in ('csv','json'):
        name = 'ARC3_ORANGE_CALENDAR.'+suffix
        require((root/'world-clock'/name).read_bytes() == (root/archive/name).read_bytes(), name+' source bytes changed')
    coordinates = [('Orange',2,d) for d in range(4,8)] + [('Orange',w,d) for w in range(3,8) for d in range(1,8)]
    require([(r['season'],r['week'],r['day']) for r in calendar] == coordinates, '39-day coverage/order mismatch')
    counts = Counter(r['kind'] for r in calendar)
    require(counts == Counter({'Duo Trial':9,'Kira Solo':6,'Dungeon':7,'Raid':1,'Hard Raid':1,
                              'Tournament':2,'domai':2,'Recovery / Tournament':1,'OPEN':10}), 'Event count mismatch')
    trials = {r['wave']:r['cumulative'] for r in js('trial-rewards/TRIAL_WAVE_CREDITS.json')}
    rewards = js('combat-rewards/COMBAT_REWARD_TABLES.json')
    totals = {'illi':0,'kira':0}
    by_kind = defaultdict(lambda: {'illi':0,'kira':0})
    waves = {'Duo Trial':[],'Kira Solo':[]}
    orange_clears, yellow_attempts = 0, 0
    daily=[]
    for row in calendar:
        kind, event = row['kind'],row['event']
        expected_i = expected_k = 0
        if kind in waves:
            match = re.search(r'W(\d+)$',event)
            require(bool(match), 'Missing Trial wave')
            wave = int(match[1]); waves[kind].append(wave)
            require(13 <= wave <= 17 and row['status'] == 'CLEAR', 'Trial is not a Green clear')
            expected_k = trials[wave]
            expected_i = expected_k if kind == 'Duo Trial' else 0
        elif kind == 'Dungeon':
            if event.startswith('Orange Dungeon'):
                number = 2 if event.endswith('×2') else 1
                require(row['status'] == ('2 CLEARS' if number == 2 else 'CLEAR'), 'Orange completion status mismatch')
                orange_clears += number
                expected_i = expected_k = number * rewards['dungeons']['normal']['Orange']
            else:
                require(event == 'Yellow Dungeon attempt' and row['status'] == 'FAIL', 'Unexpected Dungeon or Yellow completion')
                yellow_attempts += 1
        elif kind == 'Raid':
            require((row['week'],row['day']) == (4,2) and row['status'] == 'BOTH CLEAR', 'Normal Raid schedule/outcome mismatch')
            expected_i = expected_k = sum(rewards['raids']['normal'][c] for c in ('Red','Orange'))
        elif kind == 'Hard Raid':
            require((row['week'],row['day']) == (6,5) and row['status'] == 'RED CLEAR / ORANGE FAIL', 'Hard Raid schedule/outcome mismatch')
            expected_i = expected_k = rewards['raids']['hard']['Red']
        else:
            require(kind in ('OPEN','Tournament','domai','Recovery / Tournament'), 'Unexpected event kind')
        require((row['illi_credit'],row['kira_credit']) == (expected_i,expected_k), f"O{row['week']}D{row['day']}: incorrect credits")
        for who, value in [('illi',row['illi_credit']),('kira',row['kira_credit'])]:
            require(value >= 0, 'Negative gross income')
            totals[who] += value; by_kind[kind][who] += value
        daily.append({'week':row['week'],'day':row['day'],'cumulative_illi_gross':totals['illi'],'cumulative_kira_gross':totals['kira']})
    require(waves['Duo Trial'] == [13,14,14,15,15,16,16,17,17], 'Duo progression mismatch')
    require(waves['Kira Solo'] == [13,14,14,15,15,16], 'Solo progression mismatch')
    require(orange_clears == 7 and yellow_attempts == 2, 'Dungeon count mismatch')
    require(totals == {'illi':58885,'kira':83915}, 'Deterministic gross mismatch')
    require(by_kind['Kira Solo'] == {'illi':0,'kira':25030}, 'Kira-only income attribution mismatch')
    require(totals['kira']-totals['illi'] == 25030, 'Shared income topology mismatch')
    price = js('economy/KIRA_BLACK_ACQUISITION_PRICES.json')
    require(price['post_armor_acquisition_prices'] == dict.fromkeys(('CSR','Genesis Orbs','Halo','Domain'),61017), 'Black tier mismatch')
    require(price['ordinary_binding_class_matrix_applies'] is False, 'Black class-pricing firewall lost')
    require('1000' in price['armor_of_the_abyss'] and 'unchanged' in price['armor_of_the_abyss'], 'Armor repriced')
    orbs = price['post_armor_acquisition_prices']['Genesis Orbs']
    require(totals['kira']-orbs == 22898 == manifest['kira_pre_domai_discretionary_headroom'], 'Orbs reserve/headroom mismatch')
    require(manifest['locked_kira_orbs_price'] == orbs and manifest['domai_payout'] == 'OPEN', 'Final manifest lock mismatch')
    ledger = js('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json')
    beam = [r for r in ledger if r['purchase_or_upgrade'] == 'Genesis Beam → Red']
    require(len(beam) == 1 and (beam[0]['season'],beam[0]['week'],beam[0]['day'],beam[0]['cost']) == ('Yellow',1,2,6050), 'Beam cost/date moved')
    require(totals['illi'] >= 6050, 'Insufficient illi terminal reserve')
    for path in ('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv','world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json',
                 'world-clock/ILLI_PROGRESSION_SKELETON.csv','world-clock/ILLI_PROGRESSION_SKELETON.json',
                 'combat-rewards/COMBAT_REWARD_TABLES.json','combat-rewards/DOMAI_PARTICIPATION_RULES.json',
                 'trial-rewards/TRIAL_WAVE_CREDITS.csv','trial-rewards/TRIAL_WAVE_CREDITS.json',
                 'world-clock/PRISM_TEAM_TRACKER.csv'):
        if path not in {'trial-rewards/README.md', 'combat-rewards/COMBAT_REWARD_TABLES.json', 'combat-rewards/DOMAI_PARTICIPATION_RULES.json', 'combat-rewards/validate_rewards.py', 'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json', 'world-clock/WORLD_CLOCK_TEMPLATE.csv', 'world-clock/ILLI_PROGRESSION_SKELETON.csv', 'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv', 'world-clock/ILLI_PROGRESSION_SKELETON.json'}:
            require((root/path).read_bytes() == old(path), 'Protected baseline changed: '+path)
    prior_calendar = json.loads(old('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json'))
    current_calendar = js('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json')
    expected_red = ('Red',5,4)
    modified=[]
    for before,after in zip(prior_calendar,current_calendar):
        coord = (after['season'],after['week'],after['day'])
        if before != after:
            modified.append(coord)
            require(coord == expected_red and set(before) == set(after), 'Unapproved prior calendar change')
            require(all(before[k] == after[k] for k in before if k not in ('kira_combat','illi_combat','author_notes')), 'Prior combat/money changed')
    require(len(current_calendar) == len(prior_calendar) == 59 and modified == [expected_red], 'Red appointment update missing/extra')
    red = next(r for r in current_calendar if (r['season'],r['week'],r['day']) == expected_red)
    require(red['combat_event'] == 'NO REQUIRED COMBAT' and red['duration_block'] == ''
            and all('eliminated' in red[k] for k in ('kira_combat','illi_combat')), 'Red tournament conflicts with combat')
    combined=[(r['season'],r['week'],r['day']) for r in current_calendar]+coordinates
    require(combined == [(season,w,d) for season in ('Red','Orange') for w in range(1,8) for d in range(1,8)], 'Combined 98-day gap/overlap')
    lookup={(r['week'],r['day']):r for r in calendar}
    for date, status in [((5,1),'PARTICIPATE'),((5,6),'PARTICIPATE / ELIMINATED'),((7,5),'RECOVERY')]:
        row=lookup[date]
        require('Tournament' in row['kind'] and row['status'] == status
                and row['illi_credit'] == row['kira_credit'] == 0, 'Tournament/recovery conflict')
    require(lookup[(7,3)]['kind'] == lookup[(7,4)]['kind'] == 'domai'
            and lookup[(7,4)]['status'] == 'EXIT' and lookup[(7,5)]['duration'] == 'full day', 'domai recovery sequence mismatch')
    require('OPEN' in lookup[(7,3)]['notes'] and 'elapsed' in lookup[(7,6)]['notes'], 'domai payout/recovery assumption lost')
    weekly=rows('world-clock/WORLD_CLOCK_TEMPLATE.csv')
    previous_weekly=list(csv.DictReader(old('world-clock/WORLD_CLOCK_TEMPLATE.csv').decode('utf-8-sig').splitlines()))
    try:
        previous_weekly = current_clock_baseline(root, previous_weekly)
    except (OSError, ValueError, KeyError) as exc:
        require(False, 'Highlights promotion: ' + str(exc))
    changed_weeks=[]
    for before,after in zip(previous_weekly,weekly):
        require(all(before[k] == after[k] for k in before if k not in ('kira_clock','illi_clock')), 'Standing social/world track changed')
        if before != after: changed_weeks.append((after['season'],int(after['week'])))
    require(len(weekly) == len(previous_weekly) == 49 and changed_weeks == [('Red',5)]+[('Orange',w) for w in range(2,8)]+[('Green',6),('Green',7),('Blue',1),('Blue',2),('Blue',5),('Blue',6),('Blue',7)]+[('Violet',w) for w in range(1,8)]+[('White',w) for w in range(1,8)], 'Weekly update scope mismatch')
    result='FAIL' if errors else 'PASS'
    inputs=['world-clock/ARC3_ORANGE_CALENDAR.csv','world-clock/ARC3_ORANGE_CALENDAR.json',
            'world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.csv','world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json',
            'world-clock/WORLD_CLOCK_TEMPLATE.csv','economy/KIRA_BLACK_ACQUISITION_PRICES.json',
            'world-clock/validate_arc3.py']
    return {'checkpoint':19,'result':result,'errors':errors,'baseline_commit':BASELINE,
            'calendar_rows':len(calendar),'combined_consecutive_days':len(combined),'csv_json_source_bytes':'PASS' if not errors else 'CHECK ERRORS',
            'event_rows_by_kind':dict(counts),'duo_waves':waves['Duo Trial'],'kira_solo_waves':waves['Kira Solo'],
            'orange_dungeon_clears':orange_clears,'yellow_attempts':yellow_attempts,'yellow_completions':0,'red_dungeons':0,
            'income_by_kind':dict(by_kind),'deterministic_gross':totals,'kira_solo_income':25030,
            'kira_orbs_reserve':orbs,'kira_deterministic_headroom':totals['kira']-orbs,
            'illi_beam_reserve':6050,'illi_beam_date':'Yellow W1 D2','illi_arc_income_minus_reserve':totals['illi']-6050,
            'gross_is_not_ending_balance':True,'domai_payout':'OPEN; excluded, not canonically zero',
            'protected_open_days':counts['OPEN'],'tournament_dates':['R5D4 participation/eliminated','O5D1 qualification','O5D6 eliminated','O7D5 recovery/optional viewing'],
            'scheduling_scope':'Day-level conflicts checked; intraday timings/qualitative durations remain OPEN',
            'raid_eligibility_constraint':'O4D2 Normal Red must be distinct from paid O1D6 boss; exact identities OPEN',
            'weekly_character_rows_updated':len(changed_weeks),'standing_social_tracks_preserved_except_authorized_highlights':True,
            'arc3_beam_cost_date_preserved':True,'post_G6D2_ledger_authority':'CP24','daily_cumulative_gross':daily,
            'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in inputs}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write-audit',action='store_true')
    args=parser.parse_args()
    try: report=audit(args.repository.resolve())
    except (KeyError,ValueError,TypeError,IndexError,OSError,subprocess.CalledProcessError) as error:
        report={'result':'FAIL','errors':[str(error)]}
    if args.write_audit and report['result']=='PASS':
        (args.repository/'world-clock/ARC3_ECONOMY_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('daily_cumulative_gross','sha256','income_by_kind')},indent=2,ensure_ascii=False))
    return 0 if report['result']=='PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
