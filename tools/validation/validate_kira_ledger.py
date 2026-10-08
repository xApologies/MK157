"""Recompute Kira's R1D1-O2D3 ledger from her dated events and reward CSVs.

Read-only by default. Exact unknown spending is null, never a zero-cost claim.
Gross excludes the entry grant. Known balances exclude unquantified debits.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re

CALENDAR = 'world-clock/RED_TO_ORANGE_COMBAT_CALENDAR'
LEDGER = 'world-clock/KIRA_CREDIT_LEDGER'
PACKAGE = 'provenance/live-model-full-repair-2026-10-08/package/package/'
SOURCES = [CALENDAR+'.csv', CALENDAR+'.json', 'trial-rewards/TRIAL_WAVE_CREDITS.csv',
           'combat-rewards/DUNGEON_REWARDS.csv', 'combat-rewards/RAID_BOSS_REWARDS.csv',
           'economy/KIRA_BLACK_ACQUISITION_PRICES.json',
           'live-model/25_CHECKPOINT_18_MASTER_LIVE_MODEL.md',
           PACKAGE+'KIRA_LEDGER_SPEC.md', PACKAGE+'LIVE_MODEL_DELTA.md',
           'tools/validation/validate_kira_ledger.py']
NUMERIC = ('week', 'day', 'kira_credits_earned', 'kira_progression_spend',
           'kira_actual_surplus_earned', 'kira_minimum_running_gross',
           'kira_actual_running_gross', 'kira_noncombat_credits',
           'kira_known_running_balance')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def csv_rows(root, path):
    with (root/path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def reward_tables(root):
    trials = csv_rows(root, SOURCES[2])
    total = 0
    for wave, row in enumerate(trials, 1):
        total += int(row['credits'])
        require(int(row['wave']) == wave and int(row['cumulative']) == total,
                'Trial cumulative/order mismatch: '+str(wave))
    return ({int(r['wave']): int(r['cumulative']) for r in trials},
            {r['rank']: int(r['normal_completion_credits']) for r in csv_rows(root, SOURCES[3])},
            {r['boss_rank']: int(r['normal_boss_credits']) for r in csv_rows(root, SOURCES[4])})


def earned_for_event(row, tables):
    """No illi numeric field is accessed in this computation."""
    trial, dungeon, raid = tables
    event, kira = row['combat_event'], row['kira_combat']
    coordinate = (row['season'], int(row['week']), int(row['day']))
    if event.startswith('Duo Trial W'):
        wave = int(re.fullmatch(r'Duo Trial W(\d+)', event)[1])
        return trial[wave], 'Duo Trial', f'{SOURCES[2]}:wave={wave}'
    if kira.startswith('Solo Trial W'):
        wave = int(re.fullmatch(r'Solo Trial W(\d+)', kira)[1])
        return trial[wave], 'Kira Solo', f'{SOURCES[2]}:wave={wave}'
    match = re.fullmatch(r'(Red|Orange) Dungeon(?: ×(2))?', event)
    if match:
        return dungeon[match[1]] * int(match[2] or 1), 'Normal Dungeon', f'{SOURCES[3]}:rank={match[1]};count={match[2] or 1}'
    if kira == 'Normal Raid':
        required = {('Red',3,2): ('Fire Dragon Red-A CLEAR', 'Red'),
                    ('Red',6,6): ('Coherence Twins Orange-A CLEAR', 'Orange'),
                    ('Orange',1,6): ('Sixfold CLEAR; Triumvirate CLEAR; Black Orchard FAIL', 'Red')}
        require(coordinate in required, 'Unsourced Kira Raid: '+str(coordinate))
        marker, rank = required[coordinate]
        require(marker in row['result'], 'Raid identity/outcome mismatch: '+str(coordinate))
        return raid[rank], 'Normal Raid', f'{SOURCES[4]}:boss_rank={rank};normal'
    if event.startswith('illi Solo Trial'):
        return 0, 'illi-only Solo excluded', CALENDAR+'.csv:illi-only;no Kira reward'
    require(event in {'NO REQUIRED COMBAT', 'domai excursion — active day 1',
                     'domai excursion — active day 2', 'domai recovery lock'},
            'Unrecognized source event: '+event)
    return 0, 'No booked Kira reward', CALENDAR+'.csv:no sourced numeric Kira reward'


def coverage_report(gross, grant, known_prior_spend, csr):
    funds = gross + grant - known_prior_spend
    return {'result': 'PASS' if funds >= csr else 'FAIL',
            'scope': 'Sourced numeric transactions only; exact actual wallet remains OPEN',
            'authored_combat_gross_before_CSR': gross,
            'entry_grant': grant, 'locked_numeric_pre_CSR_spend': known_prior_spend,
            'known_transaction_funds_before_CSR': funds, 'CSR_cost': csr,
            'known_transaction_balance_after_CSR': funds - csr,
            'combat_gross_less_CSR': gross - csr,
            'actual_pre_CSR_balance': None, 'actual_post_CSR_balance': None,
            'unquantified_debits': ['Armor: approximately 1,000, not numerically locked',
                                    'Discretionary life spending'],
            'actual_affordability_condition': f'Unquantified pre-CSR debits <= {funds-csr}; no such spending is assumed zero',
            'failure_detail': None if funds >= csr else f'CSR O2D3 needs {csr}; sourced funds {funds}; shortfall {csr-funds}'}


def reconstruct(root):
    calendar = csv_rows(root, CALENDAR+'.csv')
    mirror = json.loads((root/(CALENDAR+'.json')).read_text(encoding='utf-8-sig'))
    converted = [dict(row) for row in calendar]
    for row in converted:
        for field in ('week','day','illi_credits_earned','purchase_cost','illi_running_balance'):
            row[field] = int(row[field])
    require(converted == mirror, 'Source calendar CSV/JSON mismatch')
    coordinates = [('Red',w,d) for w in range(1,8) for d in range(1,8)] + [('Orange',1,d) for d in range(1,8)] + [('Orange',2,d) for d in range(1,4)]
    require([(r['season'],int(r['week']),int(r['day'])) for r in calendar] == coordinates, 'Kira source scope/order differs')
    tables = reward_tables(root)
    price = json.loads((root/SOURCES[5]).read_text(encoding='utf-8-sig'))
    spec = (root/(PACKAGE+'KIRA_LEDGER_SPEC.md')).read_text(encoding='utf-8-sig')
    csr_lock = re.search(r'CSR spend ([\d,]+) occurs O(\d+)D(\d+)', spec)
    require(csr_lock is not None, 'CSR exact-date source missing')
    csr = price['post_armor_acquisition_prices']['CSR']
    require(csr == int(csr_lock[1].replace(',','')), 'CSR price sources disagree')
    require(csr_lock.group(2,3) == ('2','3'), 'CSR date changed')
    grant_source = (root/SOURCES[6]).read_text(encoding='utf-8-sig')
    grant_match = re.search(r'Starter grant \*\*([\d,]+)\*\*', grant_source)
    require(grant_match is not None, 'Sourced entry grant missing')
    grant = int(grant_match[1].replace(',',''))
    require('Approximately 1000' in price['armor_of_the_abyss'], 'Armor price needs review; no approximate debit invented')
    expected_match = re.search(r'checkpoint before CSR.*?([\d,]+) credits', spec)
    require(expected_match is not None, 'Authored gross checkpoint missing')
    expected_gross = int(expected_match[1].replace(',',''))
    rows = []; minimum = actual = balance = 0
    def add(season, week, day, event, kind, earned=0, surplus=0, noncombat=0, spend=0, source='', notes=''):
        nonlocal minimum, actual, balance
        minimum += earned; actual += earned+surplus; balance += earned+surplus+noncombat-(spend or 0)
        rows.append(dict(season=season,week=week,day=day,event=event,source_kind=kind,
                         kira_credits_earned=earned,kira_progression_spend=spend,
                         kira_actual_surplus_earned=surplus,kira_minimum_running_gross=minimum,
                         kira_actual_running_gross=actual,kira_noncombat_credits=noncombat,
                         kira_known_running_balance=balance,source=source,notes=notes))
    add('Red',1,1,'Entry grant','Noncombat grant',noncombat=grant,source=SOURCES[6],notes='Not combat gross; sourced starting funds.')
    add('Red',1,1,'Armor of the Abyss — entry/Red; exact transaction day OPEN','Unquantified progression spend',spend=None,
        source=SOURCES[5],notes='Entry bucket is not a newly locked purchase day. Approximate 1,000 is not an exact debit; null is OPEN, not free. Known balance excludes this debit.')
    by_kind = {}
    for row in calendar:
        season, week, day = row['season'],int(row['week']),int(row['day'])
        coord=(season,week,day)
        earned,kind,reward_source=earned_for_event(row,tables)
        by_kind[kind]=by_kind.get(kind,0)+earned
        spend = csr if coord==('Orange',2,3) else 0
        if spend:
            require('CSR purchase'+str(csr) in row['kira_combat'], 'CSR calendar lock missing')
        add(season,week,day,row['kira_combat']+' | '+row['combat_event'],kind,earned=earned,spend=spend,
            source=f'{CALENDAR}.csv:{season[0]}{week}D{day};{reward_source}',
            notes=('Known balance excludes unquantified Armor/lifestyle debits. ' +
                   ('CSR purchase; optional illi Solo credits excluded.' if spend else
                    'Failed encounters and optional unsourced awards add no invented reward.')))
        if coord in {('Red',4,5),('Orange',1,6)}:
            boss='Burrower' if season=='Red' else 'Triumvirate'
            require(boss in row['author_notes'] and 'surplus' in row['author_notes'], 'Authored bonus source missing: '+boss)
            add(season,week,day,boss+' Red-B first clear','Authored actual/discretionary surplus',surplus=tables[2]['Red'],
                source=f'{CALENDAR}.csv:{season[0]}{week}D{day};{SOURCES[4]}:boss_rank=Red;{PACKAGE}LIVE_MODEL_DELTA.md',
                notes='Actual eligible combat income; outside minimum progression accounting. Per-boss/season payment only once.')
    coverage=coverage_report(actual,grant,0,csr)
    errors=[]
    if actual != expected_gross: errors.append(f'Sourced row sum {actual} differs from author checkpoint {expected_gross}; delta {actual-expected_gross}. See source_rows for every contribution; no per-row author target was supplied.')
    if coverage['result']!='PASS':errors.append(coverage['failure_detail'])
    return rows,dict(result='FAIL' if errors else 'PASS',errors=errors,rows=len(rows),
                     minimum_combat_gross=minimum,authored_actual_surplus=actual-minimum,
                     authored_actual_combat_gross=actual,expected_author_checkpoint=expected_gross,
                     checkpoint_difference=actual-expected_gross,income_by_kind=by_kind,
                     affordability=coverage,
                     source_rows=[{k:r[k] for k in ('season','week','day','event','kira_credits_earned','kira_actual_surplus_earned','source')} for r in rows],
                     sha256={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in SOURCES})


def row_differences(expected, actual):
    differences=[]
    for i in range(max(len(expected),len(actual))):
        left=expected[i] if i<len(expected) else None; right=actual[i] if i<len(actual) else None
        if left!=right:
            differences.append({'row':i+1,'source_expected':left,'stored_actual':right})
    return differences


def audit(root):
    expected, report = reconstruct(root)
    current=json.loads((root/(LEDGER+'.json')).read_text(encoding='utf-8-sig'))
    csv_current=csv_rows(root,LEDGER+'.csv')
    for row in csv_current:
        for key in NUMERIC: row[key]=None if row[key]=='' else int(row[key])
    report['row_differences']={'json':row_differences(expected,current),'csv':row_differences(expected,csv_current)}
    if any(report['row_differences'].values()):
        report['errors'].append('Ledger differs from independently recomputed source rows')
        report['result']='FAIL'
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--write-ledger',action='store_true',help='Explicitly regenerate only the two Kira ledger mirrors.')
    args=parser.parse_args();root=args.repository.resolve()
    try:
        if args.write_ledger:
            rows,report=reconstruct(root)
            # Preserve computed evidence even if the author checkpoint fails; never adjust rows to force PASS.
            (root/(LEDGER+'.json')).write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
            with (root/(LEDGER+'.csv')).open('w',encoding='utf-8',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
        report=audit(root)
    except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:
        report={'result':'FAIL','errors':[str(exc)]}
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if report['result']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
