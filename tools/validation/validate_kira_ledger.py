"""Recompute Kira's R1D1-O2D3 ledger from her dated events and reward CSVs.

Read-only by default. Initial Armor consumes the full entry grant.
Combat gross and the author-locked pre/post-CSR balances stay distinct.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

CALENDAR = 'world-clock/RED_TO_ORANGE_COMBAT_CALENDAR'
LEDGER = 'world-clock/KIRA_CREDIT_LEDGER'
PACKAGE = 'provenance/live-model-full-repair-2026-10-08/package/package/'
ARMOR_SOURCE = 'provenance/armor-economy-fix-2026-10-08/package/AUTHOR_DECISION.md'
ARMOR_BASELINE = 'edfda188e942fc54c5c5db39e6ece5b42bca1e9a'
SOURCES = [CALENDAR+'.csv', CALENDAR+'.json', 'trial-rewards/TRIAL_WAVE_CREDITS.csv',
           'combat-rewards/DUNGEON_REWARDS.csv', 'combat-rewards/RAID_BOSS_REWARDS.csv',
           'economy/KIRA_BLACK_ACQUISITION_PRICES.json',
           'live-model/25_CHECKPOINT_18_MASTER_LIVE_MODEL.md',
           PACKAGE+'KIRA_LEDGER_SPEC.md', PACKAGE+'LIVE_MODEL_DELTA.md',
           'tools/validation/validate_kira_ledger.py', ARMOR_SOURCE]
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
            'scope': 'Exact initial Armor and O2D3 CSR balances under the surgical author correction',
            'authored_combat_gross_before_CSR': gross,
            'entry_grant': grant, 'locked_numeric_pre_CSR_spend': known_prior_spend,
            'known_transaction_funds_before_CSR': funds, 'CSR_cost': csr,
            'known_transaction_balance_after_CSR': funds - csr,
            'combat_gross_less_CSR': gross - csr,
            'actual_pre_CSR_balance': funds, 'actual_post_CSR_balance': funds - csr,
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
    armor = price['armor_of_the_abyss']
    require(type(armor) is int and armor == grant == 2000, 'Initial Armor must consume the exact 2,000 entry grant')
    require(price['armor_price_source'] == '../'+ARMOR_SOURCE, 'Exact Armor author source missing')
    require("Kira's initial purchase of Armor of the Abyss costs exactly 2,000 credits." in (root/ARMOR_SOURCE).read_text(encoding='utf-8-sig'), 'Armor author lock missing')
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
    add('Red',1,1,'Armor of the Abyss — initial acquisition','Locked progression spend',spend=armor,
        source=SOURCES[5],notes='Exact initial purchase consumes the entire entry grant; post-Armor balance is zero. Existing entry bucket retained.')
    post_armor = balance
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
            notes=('Exact Armor debit included; no additional unsourced transaction introduced. ' +
                   ('CSR purchase; optional illi Solo credits excluded.' if spend else
                    'Failed encounters and optional unsourced awards add no invented reward.')))
        if coord in {('Red',4,5),('Orange',1,6)}:
            boss='Burrower' if season=='Red' else 'Triumvirate'
            require(boss in row['author_notes'] and 'surplus' in row['author_notes'], 'Authored bonus source missing: '+boss)
            add(season,week,day,boss+' Red-B first clear','Authored actual/discretionary surplus',surplus=tables[2]['Red'],
                source=f'{CALENDAR}.csv:{season[0]}{week}D{day};{SOURCES[4]}:boss_rank=Red;{PACKAGE}LIVE_MODEL_DELTA.md',
                notes='Actual eligible combat income; outside minimum progression accounting. Per-boss/season payment only once.')
    prior_spend = sum(r['kira_progression_spend'] for r in rows if (r['season'],r['week'],r['day']) != ('Orange',2,3))
    coverage=coverage_report(actual,grant,prior_spend,csr)
    coverage.update(armor_cost=armor, post_armor_balance=post_armor, balance_status='LOCKED')
    errors=[]
    if (post_armor,coverage['actual_pre_CSR_balance'],coverage['actual_post_CSR_balance']) != (0,63705,2688):
        errors.append('Author-locked balances must be post-Armor 0, pre-CSR 63,705 and post-CSR 2,688')
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


def check_armor_only_rows(before, after):
    """Reject changes to any income, coordinate, CSR cost or other expenditure."""
    require(len(before)==len(after), 'Armor repair changed ledger row count')
    for i,(old,new) in enumerate(zip(before,after)):
        expected=dict(old)
        if i==1:
            require(old['kira_progression_spend'] is None and old['event'].startswith('Armor of the Abyss'), 'Unexpected prior Armor transaction')
            expected.update(kira_progression_spend=2000,event='Armor of the Abyss — initial acquisition',source_kind='Locked progression spend')
        if i>=1:expected['kira_known_running_balance']-=2000
        # Only notes describing the newly resolved debit may change; source computation checks their exact new content.
        expected['notes']=new['notes']
        require(expected==new, 'Non-Armor ledger change at row '+str(i+1))


def armor_preservation(root, rows):
    baseline=json.loads((root/'provenance/armor-economy-fix-2026-10-08/BASELINE.json').read_text(encoding='utf-8-sig'))
    require(baseline['commit']==ARMOR_BASELINE, 'Armor baseline changed')
    git=['git','-c',f'safe.directory={root.as_posix()}','-C',str(root)]
    before=json.loads(subprocess.check_output(git+['show',ARMOR_BASELINE+':'+LEDGER+'.json']))
    check_armor_only_rows(before,rows)
    protected=[p for p in baseline['files'] if p.startswith(('provenance/','combat-rewards/','trial-rewards/')) or
               (p.startswith('world-clock/') and p.endswith(('.csv','.json')) and 'AUDIT' not in p and not p.startswith(LEDGER)) or
               re.match(r'live-model/\d\d_CHECKPOINT_',p)]
    for p in protected:
        require(hashlib.sha256((root/p).read_bytes()).hexdigest()==baseline['files'][p]['sha256'], 'Protected event/reward/history changed: '+p)
    return {'result':'PASS','baseline':ARMOR_BASELINE,'protected_files':len(protected),'all_combat_and_other_ledger_fields_preserved':True}


def validated_armor_replacements(root):
    """Only the exact price field/source and two Armor sentences may differ."""
    git=['git','-c',f'safe.directory={root.as_posix()}','-C',str(root)]
    def old(path):return subprocess.check_output(git+['show',ARMOR_BASELINE+':'+path])
    price_path='economy/KIRA_BLACK_ACQUISITION_PRICES.json'
    expected=json.loads(old(price_path))
    expected.update(armor_of_the_abyss=2000,armor_price_source='../'+ARMOR_SOURCE)
    require(json.loads((root/price_path).read_text(encoding='utf-8-sig'))==expected, 'Non-Armor price field changed')
    prose_path='bindings/PRICING_MODEL.md'
    expected=old(prose_path).replace(b'Armor is the approximately 1,000-credit anomaly',b'initial Armor costs exactly 2,000 credits, consuming the whole 2,000 entry grant and leaving zero').replace(b'The starter grant does not reprice Armor.',b'This explicit author correction supersedes the prior approximate Armor price.')
    require((root/prose_path).read_bytes()==expected, 'Non-Armor pricing prose changed')
    require(audit(root)['result']=='PASS', 'Exact Armor ledger validation failed')
    return {price_path,prose_path}


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
    report['armor_only_preservation']=armor_preservation(root,expected)
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
