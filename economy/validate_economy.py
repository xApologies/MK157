"""Audit CP18 pricing/rewards with CP24 current progression and the early calendar."""

import argparse
from collections import Counter
import csv
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import statistics
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "validation"))
from validate_red_orange_reconciliation import reconcile_dates, audit as reconciliation_audit
BASELINE = '74d0bbeda7503110f9701edb8755400e34e45946'
RANKS = ('Red','Orange','Yellow','Green','Blue','Violet','White')
ANCHORS = dict(zip(('FOUNDATIONAL','COMMON_SPECIALIZATION','ADVANCED','POWERFUL','EXCEPTIONAL'),
                   (1700,3100,5700,11000,17000)))
MULTIPLIERS = ('1.60','1.80','2.10','2.50','3','4')
PRICE_FIELDS = {'red_base_cost','rank_costs','pricing_status',*RANKS}


def half(value):
    return int(Decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def audit(root):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def read(path):
        return (root/path).read_text(encoding='utf-8-sig')
    def js(path):
        return json.loads(read(path))
    def rows(path):
        with (root/path).open(encoding='utf-8-sig',newline='') as stream:
            return list(csv.DictReader(stream))
    def previous(path):
        return subprocess.check_output(['git','-c',f'safe.directory={root.as_posix()}',
                                        'show',f'{BASELINE}:{path}'],cwd=root).decode('utf-8-sig')
    def stripped(record):
        return {k:v for k,v in record.items() if k not in PRICE_FIELDS}

    matrix = {}
    for cls,base in ANCHORS.items():
        costs = [base]
        for multiplier in MULTIPLIERS:
            costs.append(half(Decimal(costs[-1])*Decimal(multiplier)))
        matrix[cls] = dict(zip(RANKS,costs))
    require(js('bindings/PRICING_CLASS_MATRIX.json') == matrix, 'Supplied JSON matrix differs from recursive anchors')
    require(rows('bindings/PRICING_CLASS_MATRIX.csv') ==
            [dict(pricing_class=cls,**{k:str(v) for k,v in ladder.items()}) for cls,ladder in matrix.items()],
            'CSV class matrix mismatch')

    pricing = {}
    registries = {}
    for base,id_key,expected_count in [('bindings/BINDINGS','id',1016),
                                      ('summons/SUMMON_PRICING','entity_id',229),
                                      ('summons/PRIME_ELEMENTAL_PRICING','prime_id',9)]:
        current = js(base+'.json')
        prior = json.loads(previous(base+'.json'))
        registries[base] = current
        require(len(current) == len(prior) == expected_count, f'{base}: count mismatch')
        require(len({row[id_key] for row in current}) == expected_count, f'{base}: duplicate IDs')
        require([stripped(row) for row in current] == [stripped(row) for row in prior],
                f'{base}: class or other non-price field changed')
        for row in current:
            ladder = matrix[row['pricing_class']]
            require(row['red_base_cost'] == ladder['Red'] and type(row['red_base_cost']) is int,
                    f'{base}/{row[id_key]}: incorrect Red anchor')
            require(all(row[rank] == ladder[rank] and type(row[rank]) is int for rank in RANKS),
                    f'{base}/{row[id_key]}: recursive ladder mismatch')
            require(row['pricing_status'] == 'LOCKED — Checkpoint 18', f'{base}: stale price status')
            if base == 'bindings/BINDINGS':
                require(row['rank_costs'] == ladder, f'{row[id_key]}: nested ladder mismatch')
        if (root/(base+'.jsonl')).exists():
            require([json.loads(line) for line in read(base+'.jsonl').splitlines()] == current,
                    f'{base}: JSONL mirror mismatch')
        csv_current = rows(base+'.csv')
        csv_prior = list(csv.DictReader(previous(base+'.csv').splitlines()))
        require(len(csv_current) == expected_count, f'{base}: CSV count mismatch')
        require([stripped(row) for row in csv_current] == [stripped(row) for row in csv_prior],
                f'{base}: CSV non-price field changed')
        require(list(csv_current[0]) == list(csv_prior[0]), f'{base}: CSV schema changed')
        lookup = {row[id_key]:row for row in current}
        require([row[id_key] for row in csv_current] == [row[id_key] for row in current], f'{base}: CSV ID order mismatch')
        for row in csv_current:
            for field in PRICE_FIELDS.intersection(row):
                require(row[field] == str(lookup[row[id_key]][field]), f'{base}/{row[id_key]}: CSV {field} mismatch')
        pricing[base] = {
            'checkpoint':18,'records':len(current),'priced':len(current),
            'counts_by_pricing_class':dict(sorted(Counter(row['pricing_class'] for row in current).items())),
            'red_base_statistics':{'min':min(row['Red'] for row in current),
                                   'median':statistics.median(row['Red'] for row in current),
                                   'max':max(row['Red'] for row in current)},
            'fixed_class_anchors':ANCHORS,'arithmetic':'sequential decimal ROUND_HALF_UP',
            'non_price_fields_including_classes_preserved':True,'csv_json_jsonl_mirrors':'PASS',
            'baseline_commit':BASELINE,
        }
    compendium = read('bindings/COMPENDIUM.md')
    old_compendium = previous('bindings/COMPENDIUM.md').replace('\r\n','\n')
    mask = lambda s: re.sub(r'^\*\*Prices:\*\*.*$', '**Prices:** <PRICE>',s,flags=re.M)
    require(mask(compendium) == mask(old_compendium), 'Compendium non-price text changed')
    bindings_by_id = {row['id']:row for row in registries['bindings/BINDINGS']}
    current_id, price_lines = None, 0
    for line in compendium.splitlines():
        heading = re.match(r'^## ([A-Z]{2}-[0-9]+) ',line)
        if heading: current_id = heading[1]
        if line.startswith('**Prices:**'):
            expected = '**Prices:** '+', '.join(f'{rank} {bindings_by_id[current_id][rank]:,}' for rank in RANKS)
            require(line.rstrip() == expected, f'Compendium {current_id}: price mirror mismatch')
            price_lines += 1
    require(price_lines == 1016, 'Compendium price row count mismatch')
    entity_ids = [row['entity_id'] for row in js('summons/SUMMONED_ENTITIES.json')]
    require(entity_ids == [row['entity_id'] for row in registries['summons/SUMMON_PRICING']], 'Entity pricing IDs differ from atlas')
    for row in registries['summons/PRIME_ELEMENTAL_PRICING']:
        require(row['pricing_class'] == 'EXCEPTIONAL', 'Prime class must remain Exceptional')
        match = [x for x in registries['summons/SUMMON_PRICING'] if x['name'] == row['name']]
        require(len(match) == 1 and all(match[0][rank] == row[rank] for rank in RANKS), 'Prime atlases disagree')

    trials = [{k:int(v) for k,v in row.items()} for row in rows('trial-rewards/TRIAL_WAVE_CREDITS.csv')]
    require(trials == js('trial-rewards/TRIAL_WAVE_CREDITS.json'), 'Trial CSV/JSON mismatch')
    prior_trials = json.loads(previous('trial-rewards/TRIAL_WAVE_CREDITS.json'))
    require(len(trials) == 35 and [row['wave'] for row in trials] == list(range(1,36)), 'Trial waves must be 1–35')
    total = 0
    for row,old in zip(trials,prior_trials):
        require(row['credits'] == half(Decimal(old['credits'])/2), f'Wave {row["wave"]}: not HALF_UP half of CP17')
        total += row['credits']
        require(row['cumulative'] == total, f'Wave {row["wave"]}: cumulative mismatch')
    require(total == 26955, 'Trial total mismatch')
    spec = importlib.util.spec_from_file_location('combat_reward_validator',root/'combat-rewards/validate_rewards.py')
    reward_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reward_module)
    reward_report = reward_module.audit(root/'combat-rewards',root)
    require(reward_report['result'] == 'PASS', 'Combat reward audit failed: '+str(reward_report['errors']))
    combat = js('combat-rewards/COMBAT_REWARD_TABLES.json')
    prior_combat = json.loads(previous('combat-rewards/COMBAT_REWARD_TABLES.json'))
    for category in ('dungeons','raids'):
        require(combat[category]['normal'] == {k:half(Decimal(v)/2) for k,v in prior_combat[category]['normal'].items()},
                f'{category}: Normal not half of baseline')
        require(combat[category]['hard'] == {k:half(Decimal(v)*Decimal('1.5')) for k,v in combat[category]['normal'].items()},
                f'{category}: Hard not HALF_UP(1.5x new Normal)')
    domai = js('combat-rewards/DOMAI_PARTICIPATION_RULES.json')
    require(set(domai) == {'checkpoint','reward_formula','awards_halved','eligibility_starts','eligibility_days',
            'conquest_required_within_window','eligible_after_leaving','no_conquest_in_window','recovery_triggers',
            'recovery_full_days','recovery_scope','death_multiplier_per_death','eventual_payout_rule',
            'core_break_bonus','scoring_and_fractional_credit_rounding'}, 'Unexpected domai fields or invented scoring table')
    require(domai['scoring_and_fractional_credit_rounding'].startswith('OPEN')
            and 'DOMAI_CORE_AWARDS.json' in domai['core_break_bonus'] and 'Blue/Violet' in domai['core_break_bonus']
            and 'OPEN' in domai['core_break_bonus'], 'domai scoring or CP25 core-layer boundary lost')
    require(domai['reward_formula'] == 'OPEN BY DESIGN' and domai['awards_halved'] is False, 'domai scoring/halving boundary changed')
    require(domai['eligibility_starts'] == 'first validated eldris kill' and domai['eligibility_days'] == 7
            and domai['conquest_required_within_window'] is True and domai['eligible_after_leaving'] is True,
            'domai eligibility rule mismatch')
    require(domai['recovery_triggers'] == ['voluntary exit','death'] and domai['recovery_full_days'] == 1
            and domai['recovery_scope'] == 'same domai', 'domai recovery rule mismatch')
    require(domai['death_multiplier_per_death'] == 0.8
            and domai['eventual_payout_rule'] == 'validated contribution award * 0.8^deaths', 'domai cumulative death rule mismatch')

    reconciliation_audit(root)
    ledger = rows('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv')
    for row in ledger:
        for key in ('week','day','cost','cumulative_progression_spend'): row[key] = int(row[key])
    require(ledger == js('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json'), 'illi ledger mirrors differ')
    old_ledger = reconcile_dates(json.loads(previous('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json')))
    omit = {'cost','cumulative_progression_spend'}
    require([{k:v for k,v in row.items() if k not in omit} for row in ledger[:13]] ==
            [{k:v for k,v in row.items() if k not in omit} for row in old_ledger[:13]], 'Pre-Arc-Six milestone dates/events changed')
    require(ledger == reconcile_dates(js('provenance/checkpoint-24-package/ILLI_PROGRESSION_LEDGER_REPLACEMENT.json')), 'Current ledger differs from CP24 author source')
    binding_lookup = {row['name']:row for row in registries['bindings/BINDINGS']}
    name_map = {'Genesis Prime':'Genesis Prime Elemental','Coherence Prime':'Coherence Prime Elemental',
                'Resonance Prime / Juggernaut':'Resonance Prime Elemental'}
    prime_lookup = {row['name']:row for row in registries['summons/PRIME_ELEMENTAL_PRICING']}
    cumulative = 0
    accepted = False
    for row in ledger:
        item = row['purchase_or_upgrade']
        if item == 'Accept White Legacy':
            require((row['season'],row['week'],row['day']) == ('Orange',1,3), 'Legacy acceptance date changed')
            expected_cost = 0
            accepted = True
        else:
            name,rank = item.split(' → ')
            price_row = prime_lookup[name_map[name]] if name in name_map else binding_lookup[name]
            expected_cost = price_row[rank]
            if accepted: expected_cost = half(Decimal(expected_cost)*Decimal('0.55'))
        cumulative += expected_cost
        require(row['cost'] == expected_cost and row['cumulative_progression_spend'] == cumulative,
                f'illi {item}: cost/cumulative error')
    require(len(ledger) == 19 and cumulative == 292772, 'illi count/total mismatch')
    require(sum(row['cost'] for row in ledger[:5]) == 45303, 'PC R→Blue cost mismatch')

    calendar = rows('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.csv')
    for row in calendar:
        for key in ('week','day','illi_credits_earned','purchase_cost','illi_running_balance'): row[key] = int(row[key])
    require(calendar == js('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json'), 'Calendar mirrors differ')
    coordinates = [('Red',w,d) for w in range(1,8) for d in range(1,8)] + [('Orange',1,d) for d in range(1,8)] + [('Orange',2,d) for d in range(1,4)]
    require([(row['season'],row['week'],row['day']) for row in calendar] == coordinates, 'Calendar not 59 ordered days')
    ledger_dates = {}
    for row in ledger:
        key=(row['season'],row['week'],row['day'])
        ledger_dates[key] = ledger_dates.get(key,0)+row['cost']
    balance,gross = 2000,0
    gates=[]
    wave_credits={row['wave']:row['cumulative'] for row in trials}
    lookup={coord:row for coord,row in zip(coordinates,calendar)}
    raid_dates={('Red',3,2):2500,('Red',6,6):3750,('Orange',1,6):2500}
    for row in calendar:
        coord=(row['season'],row['week'],row['day'])
        event=row['combat_event']
        trial_match=re.fullmatch(r'(?:Duo Trial|illi Solo Trial) W(\d+)',event)
        dungeon_match=re.fullmatch(r'(Red|Orange) Dungeon(?: ×(\d+))?',event)
        if trial_match: earned=wave_credits[int(trial_match[1])]
        elif dungeon_match: earned=combat['dungeons']['normal'][dungeon_match[1]]*int(dungeon_match[2] or 1)
        elif coord in raid_dates: earned=raid_dates[coord]
        else:
            require(event in ('NO REQUIRED COMBAT','Kira Solo Trial','domai excursion — active day 1',
                              'domai excursion — active day 2','domai recovery lock'), 'Unknown calendar event: '+event)
            earned=0
        require(row['illi_credits_earned'] == earned, f'{coord}: income does not match current rewards/eligibility')
        cost=ledger_dates.get(coord,0)
        require(row['purchase_cost'] == cost, f'{coord}: purchase differs from milestone ledger')
        gross+=earned
        before=balance+earned
        balance=before-cost
        require(balance >= 0 and row['illi_running_balance'] == balance, f'{coord}: balance negative or incorrect')
        if cost: gates.append({'season':coord[0],'week':coord[1],'day':coord[2],'purchase':row['purchase'],
                               'balance_before':before,'cost':cost,'balance_after':balance})
        if event == 'NO REQUIRED COMBAT':
            require(earned == 0 and row['duration_block'] == '', f'{coord}: negative space consumed')
    require(gross == 52695 and balance == 42, 'Calendar gross/end balance mismatch')
    require(sum(row['combat_event']=='NO REQUIRED COMBAT' for row in calendar) == 21, 'Protected negative-space row count changed')
    require(sum(row['combat_event'].startswith('illi Solo Trial') for row in calendar) == 2, 'illi Solo experiment count changed')
    require(lookup[('Orange',1,3)]['illi_running_balance'] == 952
            and 'White Legacy qualifies' in lookup[('Orange',1,3)]['purchase'], 'PC Blue/Legacy gate mismatch')
    require('Absorption Shield' in lookup[('Orange',2,2)]['purchase'], 'Absorption gate missing')
    require(lookup[('Red',5,3)]['combat_event'] == 'domai recovery lock', 'Mandatory recovery missing')
    require('no major reward' in lookup[('Red',6,6)]['result'], 'Red repeat eligibility lost')
    inputs=['bindings/PRICING_CLASS_MATRIX.json','bindings/BINDINGS.json','bindings/BINDINGS.csv','bindings/BINDINGS.jsonl','bindings/COMPENDIUM.md',
            'summons/SUMMON_PRICING.json','summons/SUMMON_PRICING.csv','summons/SUMMON_PRICING.jsonl',
            'summons/PRIME_ELEMENTAL_PRICING.json','summons/PRIME_ELEMENTAL_PRICING.csv',
            'trial-rewards/TRIAL_WAVE_CREDITS.csv','trial-rewards/TRIAL_WAVE_CREDITS.json',
            'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv','world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json',
            'world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.csv','world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json',
            'combat-rewards/DOMAI_PARTICIPATION_RULES.json','economy/validate_economy.py']
    result='FAIL' if errors else 'PASS'
    for summary in pricing.values(): summary['result']=result
    return {'checkpoint':18,'result':result,'errors':errors,'baseline_commit':BASELINE,'pricing_matrix':matrix,
            'pricing':pricing,'trial_total':total,'trial_rows':len(trials),'combat_rewards':reward_report,
            'illi_ledger':{'rows':len(ledger),'total':cumulative,'first_13_dates_authority':'Original milestones except explicit October8 PC/Legacy O1D3 and Absorption O2D2 correction','post_G6D2_authority':'CP24 six-event replacement','events':ledger},
            'calendar':{'result':result,'rows':len(calendar),'starting_credits':2000,'gross_illi_credits':gross,
                        'ending_balance':balance,'minimum_daily_closing_balance':min(row['illi_running_balance'] for row in calendar),
                        'negative_space_rows':21,'illi_solo_attempts':2,'purchase_gates':gates,'all_balances_nonnegative':not any('balance negative' in e for e in errors)},
            'domai':domai,'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in inputs}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write-audits',action='store_true')
    args=parser.parse_args()
    try:
        report=audit(args.repository.resolve())
    except (KeyError,ValueError,TypeError,IndexError,OSError,subprocess.CalledProcessError) as error:
        report={'result':'FAIL','errors':[str(error)]}
    if args.write_audits and report['result']=='PASS':
        outputs={'economy/AUDIT.json':report,
                 'bindings/PRICING_AUDIT.json':report['pricing']['bindings/BINDINGS'],
                 'summons/PRICING_AUDIT.json':{'checkpoint':18,'result':'PASS','entities':report['pricing']['summons/SUMMON_PRICING'],
                                             'primes':report['pricing']['summons/PRIME_ELEMENTAL_PRICING']},
                 'world-clock/CALENDAR_AUDIT.json':report['calendar']}
        for path,data in outputs.items():
            (args.repository/path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'result':report['result'],'errors':report['errors'],
                      'pricing_records':{k:v['records'] for k,v in report.get('pricing',{}).items()},
                      'trial_total':report.get('trial_total'),'illi_total':report.get('illi_ledger',{}).get('total'),
                      'calendar':report.get('calendar')},indent=2,ensure_ascii=False))
    return 0 if report['result']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
