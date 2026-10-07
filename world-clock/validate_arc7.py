"""Audit the corrected CP25 calendar/economy and preserve the CP24 boundary."""
import argparse
from collections import Counter
import csv
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools' / 'validation'))
from validate_promotions import validated_city_replacements


def audit(root):
    errors = []
    def require(ok, message):
        if not ok: errors.append(message)
    def text(p): return (root / p).read_text(encoding='utf-8-sig')
    def js(p): return json.loads(text(p))
    def sha(p): return hashlib.sha256((root / p).read_bytes()).hexdigest()
    def rows(p): return list(csv.DictReader(io.StringIO(text(p), newline='')))
    before = js('provenance/CHECKPOINT_25_BEFORE_REVIEW.json')
    def old(p):
        return subprocess.check_output(['git', '-c', f'safe.directory={root.as_posix()}', 'show', before['baseline_commit'] + ':' + p], cwd=root)
    require(before['baseline_commit'] == before['fetched_origin_main'] == 'e540b07afd6d231c771e5e744e5a0ee3d5aabcf8', 'Unexpected reconciliation baseline')
    sources = []
    for name, package in before['packages'].items():
        directory = package['archive']
        actual = {p.relative_to(root / directory).as_posix() for p in (root / directory).rglob('*') if p.is_file()}
        require(actual == set(package['source_sha256']), 'Source membership changed: ' + name)
        for p, digest in package['source_sha256'].items():
            require(sha(directory + '/' + p) == digest, 'Source bytes changed: ' + p)
            sources.append(directory + '/' + p)
        inventory = 'MANIFEST.json' if name == 'correction' else 'FILE_INVENTORY.json'
        for item in js(directory + '/' + inventory):
            require(sha(directory + '/' + item['path']) == item['sha256'] and (root / directory / item['path']).stat().st_size == item['bytes'], 'Manifest mismatch: ' + item['path'])
    require(len(sources) == 21, 'Expected both complete source packages')
    for extension in ('csv', 'md'):
        p = 'ARC7_REVISED_DIRECTOR_CALENDAR.' + extension
        require((root / 'world-clock' / p).read_bytes() == (root / 'provenance/checkpoint-25-correction-package' / p).read_bytes(), 'Revised calendar differs from author source')
    calendar = rows('world-clock/ARC7_REVISED_DIRECTOR_CALENDAR.csv')
    require(calendar == js('world-clock/ARC7_REVISED_DIRECTOR_CALENDAR.json') and len(calendar) == 12, 'Calendar mirrors/row count mismatch')
    state = js('world-clock/ARC7_HANDOFF.json')
    require((state['arc6_close'], state['arc7_open'], state['arc7_close']) == ('B6D3', 'B6D4', 'Valnak departure after White W7'), 'Arc boundaries changed')
    require((state['two_orb_operational_by'], state['three_orb_training_begins'], state['three_orb_operational_window']) == ('V2D3', 'V2D4', 'late V7'), 'Application anchors changed')
    require(state['domain'] == {'window': 'Late Violet', 'date': None, 'cost': 61017}, 'Domain boundary changed')
    require(not state['genesis_orb_mastery_asserted'] and state['exact_blue_violet_daily_calendar'] is None, 'Invented mastery or training dates')
    for key in ('exact_departure_date', 'white_raid_dates', 'white_raid_runtimes', 'illi_rank_purchase_dates', 'support_binding_names', 'support_binding_count', 'discretionary_final_balances'):
        require(state[key] is None, 'Unprovided exact detail invented: ' + key)
    require(state['blue_core_attempt'] == {'white_week': 1, 'result': 'fails/aborts', 'award': 0, 'date': None} and not state['violet_core_attempt'], 'Failed Blue/absent Violet core scope changed')
    require(not state['trio_booked'] and not state['blue_violet_raid_clear'] and not state['required_hard_dungeon_program'], 'Extra major combat booked')
    require(state['final_standings'] == {'Solo': 100, 'Duo': 100} and state['recovery_between_trial_runs'], 'Final standings or recovery changed')

    base = js('trial-rewards/TRIAL_WAVE_CREDITS.json')
    require(len(base) == 35 and base[-1]['cumulative'] == 26955, 'Base Trial schedule changed')
    extension = js('trial-rewards/TRIAL_EXTENDED_REWARDS.json')
    require([extension[k] for k in ('base_completed_wave', 'base_cumulative', 'extension_starts', 'credits_per_completed_wave', 'upper_wave_limit', 'failed_next_wave_credits', 'party_size_divisor')] == [35, 26955, 36, 1600, None, 0, 1], 'Extension/reward allocation changed')
    require(extension['legitimate_repeats_pay'] and extension['eligible_modes'] == ['Solo', 'Duo', 'Trio'] and extension['numeric_population_cap'] is None, 'Repeat/mode/population boundary changed')
    def cumulative(wave): return base[wave-1]['cumulative'] if wave <= 35 else base[-1]['cumulative'] + (wave-35)*extension['credits_per_completed_wave']
    require((cumulative(96), cumulative(100)) == (124555, 130955), 'W96/W100 formula mismatch')
    trial = js('world-clock/ARC7_TRIAL_LEDGER.json')
    expected = []
    for sequence, mode, wave in ((1, 'Solo', 96), (2, 'Duo', 100), (3, 'Solo', 100)):
        expected.append({'white_week': 1, 'sequence': sequence, 'mode': mode, 'wave': wave, 'termination': 'voluntary', 'date': None, 'credits_each': cumulative(wave), 'kira': cumulative(wave), 'illi': cumulative(wave) if mode == 'Duo' else 0})
    require(trial == expected, 'Trial sequence/payout mismatch')
    require(state['trial_sequence'] == [{k:v for k,v in r.items() if k not in ('credits_each','kira','illi')} for r in expected], 'Handoff Trial sequence mismatch')
    trial_totals = {who:sum(r[who] for r in trial) for who in ('kira', 'illi')}
    require(trial_totals == {'kira': 386465, 'illi': 130955}, 'Trial gross mismatch')

    awards = js('combat-rewards/DOMAI_CORE_AWARDS.json')
    collective = {'Red': 1000000, 'Orange': 2300000, 'Yellow': 3700000, 'Green': 5000000, 'Blue': None, 'Violet': None}
    require(awards['collective'] == collective and awards['each'] == {k:v//2 if v is not None else None for k,v in collective.items()}, 'Core ladder mismatch')
    require(awards['eligible_members'] == 2 and awards['illi_participates_legitimately'] and not awards['white_domai_exist'], 'Core unit/eligibility/ontology changed')
    core = js('world-clock/ARC7_DOMAI_CORE_LEDGER.json')
    expected = []
    for week in range(1, 8):
        ranks = ['Red','Orange','Yellow','Green','Green'] if week == 1 else ['Green']*(2 if week == 7 else 4)
        for sequence, rank in enumerate(ranks, 1):
            expected.append((week, sequence, (1 if sequence == 1 else 3) if week == 7 else None, rank, collective[rank], collective[rank]//2, collective[rank]//2))
    keys = ('white_week','sequence','day','rank','collective_bonus','kira_share','illi_share')
    require([tuple(r[k] for k in keys) for r in core] == expected, 'Core event sequence or amounts mismatch')
    require(all('mature established campaign' in r['doctrine'] for r in core if r['white_week'] > 1), 'Closer doctrine missing')
    require('second Green' in state['closer_doctrine'], 'Ethical correction trigger missing')
    weekly_core = {w:sum(r['illi_share'] for r in core if r['white_week'] == w) for w in range(1, 8)}
    require(list(weekly_core.values()) == [8500000, 10000000, 10000000, 10000000, 10000000, 10000000, 5000000], 'Weekly core totals mismatch')
    core_total = sum(weekly_core.values())
    require(core_total == 63500000 and Counter(r['rank'] for r in core) == {'Red':1,'Orange':1,'Yellow':1,'Green':24}, 'Core total/count mismatch')
    tables = js('combat-rewards/COMBAT_REWARD_TABLES.json')
    raids = {mode:sum(tables['raids'][mode][rank] for rank in ('Red','Orange','Yellow','Green')) for mode in ('normal','hard')}
    require(raids == {'normal':18750, 'hard':28125}, 'Raid endpoint mismatch')
    require(state['white_raid_first_clear_ranks'] == {mode:['Red','Orange','Yellow','Green'] for mode in raids}, 'Raid rank scope mismatch')
    gross = {who:core_total + value + sum(raids.values()) for who,value in trial_totals.items()}
    require(gross == state['fixed_white_gross'] == {'kira':63933340,'illi':63677830}, 'Fixed White gross mismatch')

    bindings = {r['name']:r for r in js('bindings/BINDINGS.json')}
    primes = {r['name']:r for r in js('summons/PRIME_ELEMENTAL_PRICING.json')}
    endpoints = {'Persistent Coherence':'Blue','Absorption Shield':'Green','Genesis Prime Elemental':'Yellow','Coherence Prime Elemental':'Red','Resonance Prime Elemental':'Red'}
    ranks = ['Red','Orange','Yellow','Green','Blue','Violet','White']
    expected_bill = []
    for name, start in endpoints.items():
        prices = (primes if name in primes else bindings)[name]
        for rank in ranks[ranks.index(start)+1:]:
            expected_bill.append({'binding':name,'from_B6D3_rank':start,'purchase_rank':rank,'base_price':prices[rank],'illi_cost':int((Decimal(prices[rank])*Decimal('0.55')).quantize(Decimal('1'),rounding=ROUND_HALF_UP)),'purchase_date':None})
    bill = js('economy/ILLI_REMAINING_WHITE_BILL.json')
    require(bill == expected_bill, 'Remaining bill differs from current registries/55%-per-rank HALF_UP')
    bill_total = sum(r['illi_cost'] for r in bill)
    require(bill_total == state['illi_remaining_bill'] == 9513297, 'White bill mismatch')
    require(gross['illi'] - bill_total == state['illi_fixed_gross_after_bill'] == 54164533, 'After-bill amount mismatch')
    require(state['decoherence'] == {'available_after':'first White Legacy completion','deferred_this_cycle':True,'reason':'illi voluntarily agrees to Elara request','mechanical_block':False}, 'Decoherence deferral changed')
    require(state['kira_rank'] == 'Black' and state['support_one_off_each'] == 61017 and state['next_black_node'] == {'ontology':None,'natural_price':None,'temporary_cycle_price':999999999999}, 'Black support/administrative price scope changed')
    require(state['white_ring'] == {'acquired_before_departure':True,'price':None}, 'Ring price or acquisition changed')
    card = js('economy/ADVANCED_CARD_PRICES.json')
    require(card['rank_prices'] == js('bindings/PRICING_CLASS_MATRIX.json')['ADVANCED'] == dict(zip(ranks,[5700,9120,16416,34474,86185,258555,1034220])), 'Advanced card ladder mismatch')
    require(card['specific_prior_exception'] == {'item':'Arc Three specific Blue Fireball Genesis Card','price':86000,'preserved':True}, 'Specific earlier card purchase changed')
    purchases = js('economy/KIRA_ARC7_PURCHASE_DIRECTION.json')
    require(purchases['support']['each_one_off'] == 61017 and purchases['support']['independent_thought_action_shaping'] and not purchases['support']['mind_control'] and purchases['support']['names'] is None and purchases['support']['count'] is None, 'Support interface boundary changed')
    require(purchases['next_black_node'] == state['next_black_node'] and purchases['white_dimensional_ring'] == state['white_ring'] and purchases['domain'] == state['domain'], 'Purchase mirrors mismatch')

    metric = js('combat-rewards/DOMAI_SPATIAL_METRIC.json')
    require([r['rank'] for r in metric] == ranks[:-1] and [r['exterior_radius_miles'] for r in metric] == [3,5,7,11,13,17], 'Spatial metric ranks/radii changed')
    require(all(Decimal(str(r['equivalent_interior_radius_miles'])) == Decimal(r['exterior_radius_miles'])*Decimal('1.7') for r in metric), 'Equivalent traversal scale mismatch')
    require((root/'combat-rewards/DOMAI_SPATIAL_METRIC.csv').read_bytes() == (root/'provenance/checkpoint-25-master-package/DOMAI_SPATIAL_METRIC.csv').read_bytes(), 'Spatial CSV differs from source')
    for stem, data in [('world-clock/ARC7_DOMAI_CORE_LEDGER',core),('world-clock/ARC7_TRIAL_LEDGER',trial),('economy/ILLI_REMAINING_WHITE_BILL',bill),('combat-rewards/DOMAI_SPATIAL_METRIC',metric)]:
        csv_data = rows(stem+'.csv')
        require(csv_data == [{k:'' if v is None else str(v) for k,v in row.items()} for row in data], 'CSV mirror differs: '+stem)

    # Exact preservation of all unaffected baseline files, including historical provenance.
    allowed = {'.gitattributes','README.md','THREAD_DEVELOPMENT_CONSTITUTION.md',
        *['live-model/'+p for p in ('01_KIRA.md','03_VALNEK_PATHS.md','04_COMBAT_WORLD.md','BLACK_SYSTEMS_MASTERY.md','COMBAT_ECOLOGY.md','COMBAT_THRESHOLDS.md','DOMAI_PARTICIPATION.md','ECONOMY_PURCHASE_SCHEDULE.md','GENESIS_CARDS.md','ILLI_PROGRESSION.md','INDEX.md','OPEN.md','PARTNERSHIP_AND_CARRY.md','PRIME_ELEMENTALS.md','RAEON.md','STORY_CLOCK_STATE.md','SUPERSESSIONS.md','TRIAL_ARENA.md','WORLD_CLOCK.md')],
        *['world-clock/'+p for p in ('WORLD_CLOCK.md','WORLD_CLOCK_TEMPLATE.csv','validate_arc3.py','validate_arc4_handoff.py','validate_arc4_yellow.py','validate_arc5.py','validate_arc6.py','validate_yellow_director.py','ARC3_ECONOMY_AUDIT.json','ARC4_HANDOFF_AUDIT.json','ARC4_YELLOW_AUDIT.json','ARC5_DIRECTOR_AUDIT.json','ARC6_DIRECTOR_AUDIT.json','YELLOW_DIRECTOR_AUDIT.json')],
        'trial-rewards/README.md','combat-rewards/README.md','combat-rewards/COMBAT_REWARD_TABLES.json','combat-rewards/DOMAI_PARTICIPATION_RULES.json','combat-rewards/validate_rewards.py','economy/validate_economy.py','economy/AUDIT.json'}
    # Only the two explicitly promoted city surfaces may differ from this
    # historical snapshot, and their complete promotion chain must validate.
    try:
        allowed.update(validated_city_replacements(root))
    except (OSError, ValueError, KeyError) as exc:
        require(False, 'City promotion preservation: ' + str(exc))
    protected = []
    for p, digest in before['sha256'].items():
        if p not in allowed:
            require(sha(p) == digest, 'Unrelated baseline file changed: '+p)
            protected.append(p)
    old_tables = json.loads(old('combat-rewards/COMBAT_REWARD_TABLES.json'))
    require({k:v for k,v in tables.items() if k != 'domai'} == {k:v for k,v in old_tables.items() if k != 'domai'}, 'Fixed combat reward data changed')
    require(tables['domai']['reward_formula'] == old_tables['domai']['reward_formula'] == 'OPEN BY DESIGN', 'Ordinary contribution formula replaced')
    participant = js('combat-rewards/DOMAI_PARTICIPATION_RULES.json')
    old_participant = json.loads(old('combat-rewards/DOMAI_PARTICIPATION_RULES.json'))
    require({k:v for k,v in participant.items() if k != 'core_break_bonus'} == {k:v for k,v in old_participant.items() if k != 'core_break_bonus'}, 'Participant rules changed beyond core reference')
    for p in ('live-model/BLACK_SYSTEMS_MASTERY.md',):
        require((root/p).read_bytes().startswith(old(p).rstrip()), 'Prior mastery doctrine changed')
    carry = re.compile(r'(?ms)^## Project Princess Carry — LOCK\n.*?(?=^## )')
    require(carry.search(old('live-model/PARTNERSHIP_AND_CARRY.md').decode()).group() == carry.search(text('live-model/PARTNERSHIP_AND_CARRY.md')).group(), 'Carry character doctrine changed')
    weekly = rows('world-clock/WORLD_CLOCK_TEMPLATE.csv')
    previous = list(csv.DictReader(io.StringIO(old('world-clock/WORLD_CLOCK_TEMPLATE.csv').decode('utf-8-sig'))))
    changed = []
    require(len(weekly) == len(previous) == 49, 'Weekly row count changed')
    for a,b in zip(previous, weekly):
        require({k:v for k,v in a.items() if k not in ('kira_clock','illi_clock')} == {k:v for k,v in b.items() if k not in ('kira_clock','illi_clock')}, 'Standing world schedule changed')
        if a != b: changed.append((b['season'],int(b['week'])))
        if b['season']=='Blue' and b['week']=='6':
            require(b['illi_clock']==a['illi_clock'] and b['kira_clock']==a['kira_clock']+'; D4 onward two-Orb development', 'B6D1–D3 changed')
    require(changed == [('Blue',6),('Blue',7)]+[('Violet',w) for w in range(1,8)]+[('White',w) for w in range(1,8)], 'Weekly overlay scope mismatch')
    require(state['finale'] == {'W7D1':'mature Green close','W7D2':'social/vacation','W7D3':'mature Green close','W7D4':'shopping/friends/final preparation','W7D5':'raeon Championship; Final Auction begins','W7D6':'Final Auction/social','W7D7':'Final Auction conclusion; spending/goodbyes/departure preparation'}, 'Finale days changed')
    # Compatible master sections must survive fully in the current canonical addendum.
    master = text('provenance/checkpoint-25-master-package/CHECKPOINT25_LIVE_MODEL_DELTA.md')
    sections = {p.split('\n',1)[0]:p.split('\n',1)[1].strip() for p in re.split(r'(?m)^## ',master)[1:]}
    canonical = text('live-model/32_CHECKPOINT_25_ARC7_FINALE.md')
    for name in ('Author understory','Kira remains BLACK','Genesis Orbs knowledge firewall','Trial W36+ — NEW LOCK','Project Princess Carry','domai ontology / metric','Crack-team doctrine','Core-break bonus — NEW LOCK','White Raid endpoint','Cards / spending','Dimensional Ring','White W7 finale'):
        require(sections[name] in canonical, 'Compatible master material lost: '+name)
    require(text('provenance/checkpoint-25-correction-package/ARC7_REVISED_DIRECTOR_CALENDAR.md') in canonical, 'Full correction missing from current addendum')
    for name in ('Final Eternal Standings','White core schedule','White fixed income'):
        require(sections[name] not in canonical, 'Superseded draft section promoted: '+name)
    require('2.5M conversational price is not canon' in text('live-model/DIMENSIONAL_RINGS.md'), 'Ring placeholder price boundary missing')
    source_audit = js('provenance/checkpoint-25-correction-package/ARC7_REVISED_ECONOMY_AUDIT.json')
    require(source_audit['fixed_white_gross'] == gross and source_audit['white_trials'] == trial_totals and source_audit['white_core_breaks']['total_each'] == core_total and source_audit['illi']['remaining_first_white_legacy_bill'] == bill_total, 'Derived totals differ from corrected author audit')
    return {'checkpoint':25,'result':'FAIL' if errors else 'PASS','errors':errors,'baseline_commit':before['baseline_commit'],'calendar_rows':len(calendar),'source_files':sources,'trial_totals':trial_totals,'W96_each':cumulative(96),'W100_each':cumulative(100),'core_successes':len(core),'core_rank_counts':dict(Counter(r['rank'] for r in core)),'weekly_core_each':weekly_core,'core_each':core_total,'raids_each':raids,'fixed_white_gross':gross,'illi_remaining_bill':bill_total,'illi_fixed_gross_after_bill':gross['illi']-bill_total,'bill_by_binding':{n:sum(r['illi_cost'] for r in bill if r['binding']==n) for n in endpoints},'weekly_overlay_changes':changed,'protected_baseline_files':protected,'arc6_and_prior_calendars_byte_identical':True,'dated_illi_ledger_byte_identical':True,'fixed_combat_reward_numbers_unchanged':True,'ordinary_domai_participation_unchanged':True,'standing_world_tracks_unchanged':True,'carry_section_unchanged':True,'superseded_master_schedule_not_promoted':True,'no_invented_exact_training_or_purchase_dates':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args();report=audit(args.repository)
    if args.write:
        (args.repository/'world-clock/ARC7_ECONOMY_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('protected_baseline_files','source_files')},indent=2,ensure_ascii=False))
    raise SystemExit(0 if report['result']=='PASS' else 1)


if __name__=='__main__': main()
