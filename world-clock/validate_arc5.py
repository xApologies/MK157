"""Audit the locked CP23 Arc Five calendar against reward tables and preserved canon."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools' / 'validation'))
from validate_promotions import validated_city_replacements
from validate_clock_promotion import current_clock_baseline, validated_replacements


def audit(root):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    def text(path): return (root / path).read_text(encoding='utf-8-sig')
    def js(path): return json.loads(text(path))
    def sha(path): return hashlib.sha256((root / path).read_bytes()).hexdigest()
    def rows(path):
        with (root / path).open(encoding='utf-8-sig', newline='') as stream:
            return list(csv.DictReader(stream))
    before = js('provenance/CHECKPOINT_23_BEFORE_REVIEW.json')
    archive = 'provenance/checkpoint-23-package/'
    require(set(before['package_source_sha256']) == {p.name for p in (root / archive).iterdir()} and len(before['package_source_sha256']) == 8, 'Source membership mismatch')
    for path, digest in before['package_source_sha256'].items():
        require(sha(archive + path) == digest, 'Uploaded source altered: ' + path)
    for item in js(archive + 'FILE_INVENTORY.json'):
        require(sha(archive + item['path']) == item['sha256'] and (root / archive / item['path']).stat().st_size == item['bytes'], 'Source inventory mismatch: ' + item['path'])
    for ext in ('csv', 'json'):
        path = 'ARC5_DIRECTOR_CALENDAR.' + ext
        require((root / 'world-clock' / path).read_bytes() == (root / archive / path).read_bytes(), 'Calendar differs from source: ' + path)
    calendar = rows('world-clock/ARC5_DIRECTOR_CALENDAR.csv')
    require(calendar == js('world-clock/ARC5_DIRECTOR_CALENDAR.json'), 'CSV/JSON disagreement')
    dates = [f"{r['season'][0]}{r['week']}D{r['day']}" for r in calendar]
    expected_dates = ['Y6D' + str(d) for d in range(4, 8)] + ['Y7D' + str(d) for d in range(1, 8)] + [f'G{w}D{d}' for w in range(1, 6) for d in range(1, 8)] + ['G6D1', 'G6D2']
    require(dates == expected_dates and len(set(dates)) == 48, '48 consecutive dates/order required')
    lookup = dict(zip(dates, calendar))
    trials = {r['wave']: r['cumulative'] for r in js('trial-rewards/TRIAL_WAVE_CREDITS.json')}
    reward = js('combat-rewards/COMBAT_REWARD_TABLES.json')
    duo_dates = ['Y6D5', 'Y6D6', 'G2D2', 'G3D6', 'G5D6']
    kira_waves = {'G1D1': 3, 'G2D1': 5, 'G2D6': 7, 'G3D4': 10, 'G4D1': 14, 'G5D1': 19}
    illi_waves = {'G1D4': 8, 'G3D2': 9, 'G5D2': 10}
    yellow_dates = ['G1D2', 'G1D6', 'G2D3', 'G3D1']
    green_fail = ['G4D2', 'G4D6']; green_clear = ['G5D3', 'G5D4', 'G5D7']
    raids = {'G2D4': ('Red', 'A', 'Red boss B'), 'G3D3': ('Red', 'B', 'Orange boss A'), 'G4D4': ('Orange', 'A', 'Orange boss B')}
    counts = Counter(); total = {'kira': 0, 'illi': 0}
    categories = defaultdict(lambda: {'kira': 0, 'illi': 0})
    daily = []; paid_bosses = set(); raid_bookings = []
    noncombat = {'Arc Five opening', 'Recovery', 'raeon', 'Seasonal Auction', 'Builder Night', 'Open', 'Arc Five endpoint'}
    for date, row in zip(dates, calendar):
        event = row['event']; result = row['result']; k = i = 0; category = 'noncombat'
        if event == 'Shared Duo Trial':
            require(date in duo_dates and 'W18 clear' in result and 'W19' in result and 'fail' in result.lower(), 'Duo result/date mismatch: ' + date)
            k = i = trials[18]; counts['shared_W18_duo'] += 1; category = 'duo'
        elif event == 'Kira Solo Trial':
            wave = kira_waves.get(date)
            require(wave is not None and f'W{wave} ' in result, 'Kira paid wave/date mismatch: ' + date)
            k = trials[wave]; counts['kira_paid_solo'] += 1; category = 'solo'
            if wave == 19:
                require(result == 'W19 Blue CLEAR; W20 reached/fails', 'Blue breakthrough outcome changed')
            else:
                require('clear' in result.lower(), 'Practice run lacks a completed wave')
        elif event.startswith('illi Solo Trial'):
            wave = illi_waves.get(date)
            require(wave is not None and f'W{wave} ' in result and f'W{wave+1} reached' in result, 'illi Solo wave/date mismatch: ' + date)
            i = trials[wave]; counts['illi_solo'] += 1; category = 'solo'
            if wave == 10:
                require(result == 'illi W10 Yellow CLEAR; W11 reached/fails' and row['kira_activity'].startswith('Recovery / Highlights'), 'illi endpoint/Kira recovery mismatch')
        elif event == 'Dungeon session':
            require(date in yellow_dates and result == '2 Yellow clears', 'Yellow farm/date mismatch')
            k = i = 2 * reward['dungeons']['normal']['Yellow']; category = 'yellow_dungeon'; counts['yellow_clears'] += 2
        elif event.startswith('Green Dungeon #'):
            counts['green_attempts'] += 1; category = 'green_dungeon'
            if 'CLEAR' in result:
                require(date in green_clear, 'Unexpected Green clear date')
                k = i = reward['dungeons']['normal']['Green']; counts['green_clears'] += 1
                require((date == 'G5D3') == (result == 'FIRST GREEN CLEAR'), 'First Green clear changed')
            else:
                require(date in green_fail and result.startswith('FAIL') and 'OPEN/excluded' in row['notes'], 'Failed Green reward scope changed')
                counts['green_failures'] += 1
        elif event.startswith('Raid outing #'):
            require(date in raids, 'Extra/undated Normal Raid')
            rank, identity, failed_boss = raids[date]
            key = ('Green', 'normal', rank, identity)
            require(key not in paid_bosses, 'Raid boss paid twice in season')
            require(f'{rank} boss {identity} clear' in result and failed_boss + ' fail' in result, 'Raid clear/fail identity changed')
            paid_bosses.add(key); k = i = reward['raids']['normal'][rank]; category = 'normal_raid'; counts['normal_raid_outings'] += 1
            raid_bookings.append({'date': date, 'season': 'Green', 'mode': 'normal', 'cleared_boss': f'{rank} {identity}', 'failed_boss': failed_boss, 'each': k})
        elif event == 'Orange domai':
            require(date == 'Y7D4' and result.startswith('SUCCESS') and 'Payout OPEN' in row['notes'], 'Orange contextual event changed')
            counts['orange_domai_success'] += 1; category = 'domai_excluded'
        elif event == 'Yellow domai':
            require(date == 'G6D1' and result == 'FAIL / no conquest payout', 'Yellow domai failure changed')
            counts['yellow_domai_failure'] += 1; category = 'domai_excluded'
        elif event in noncombat:
            counts['noncombat_rows'] += 1
        else:
            require(False, 'Unexpected event: ' + event)
        require((int(row['kira_fixed_credits']), int(row['illi_fixed_credits'])) == (k, i), 'Row reward differs from tables: ' + date)
        for who, value in (('kira', k), ('illi', i)):
            total[who] += value; categories[category][who] += value
        daily.append({'date': date, 'event': event, 'kira': k, 'illi': i, 'cumulative_fixed_gross': total.copy()})
    expected_counts = {'shared_W18_duo': 5, 'kira_paid_solo': 6, 'illi_solo': 3, 'yellow_clears': 8, 'green_attempts': 5, 'green_clears': 3, 'green_failures': 2, 'normal_raid_outings': 3, 'orange_domai_success': 1, 'yellow_domai_failure': 1, 'noncombat_rows': 20}
    require(dict(counts) == expected_counts, 'Combat/noncombat counts mismatch')
    require(total == {'kira': 88595, 'illi': 78430}, 'Fixed gross mismatch')
    require(total == {k.lower(): v for k, v in js(archive + 'AUDIT.json')['final_fixed_gross'].items()} == {k.lower(): v for k, v in js(archive + 'LOCKED_DECISIONS.json')['final_fixed_gross'].items()}, 'Authored totals disagree')
    require(all('Trio' not in r['event'] + r['kira_activity'] + r['illi_activity'] and r['event'] != 'Green domai' for r in calendar), 'Invented Trio/Green domai')
    nights = [d for d, r in lookup.items() if r['event'] == 'Builder Night']
    require(nights == [f'G{w}D5' for w in range(1, 6)], 'Recurring Builder nights changed')
    require(lookup['Y6D5']['event'] == 'Shared Duo Trial' and 'displaced' in lookup['Y6D5']['notes'] and lookup['Y7D5']['event'] == 'Seasonal Auction', 'D5 displacement lost')
    require(lookup['G6D2']['illi_activity'] == 'Coherence Prime Elemental → Red' and '9,350' in lookup['G6D2']['result'], 'Arc endpoint moved/repriced')
    require(lookup['G5D4']['event'] == 'Green Dungeon #4' and 'fourth Normal Raid' in lookup['G5D4']['notes'], 'Fourth Raid replacement lost')

    # Independently reconcile the entire 11-date intersection; no new Yellow income.
    yellow = {f"Y{r['week']}D{r['day']}": r for r in js('world-clock/YELLOW_DIRECTOR_CALENDAR.json')}
    overlap = [date for date in dates if date in yellow]
    require(overlap == expected_dates[:11], 'Unexpected calendar overlap')
    overlap_total = {who: sum(int(lookup[d][who + '_fixed_credits']) for d in overlap) for who in total}
    for date in overlap:
        for who in total:
            require(int(lookup[date][who + '_fixed_credits']) == int(yellow[date][who + '_deterministic_credits']), 'Overlapping Yellow credit conflict: ' + date)
    require(overlap_total == {'kira': 13110, 'illi': 13110}, 'Overlapping Duo gross mismatch')
    require('Arc Five opening' == yellow['Y6D4']['event'] == lookup['Y6D4']['event'], 'Opening overlap conflict')
    for date in ('Y6D5', 'Y6D6'):
        require(yellow[date]['event'] == lookup[date]['event'] == 'Shared Duo Trial', 'Overlapping Trial conflict')
    require(yellow['Y6D7']['event'] == lookup['Y6D7']['event'] == 'Recovery', 'Overlapping recovery conflict')
    for day in (1, 2, 3):
        require('run ends by Y7D3' in yellow[f'Y7D{day}']['result'] and 'eliminated by D3' in lookup[f'Y7D{day}']['result'], 'raeon block conflict')
    require(yellow['Y7D4']['result'].startswith('Successful') and lookup['Y7D4']['event'] == 'Orange domai', 'Y7D4 outcome conflict')
    for day in (5, 6, 7):
        require('Auction' in yellow[f'Y7D{day}']['event'] and lookup[f'Y7D{day}']['result'] == f'Auction Day {day-4}', 'Auction overlap conflict')
    combined = {who: sum(int(r[who + '_deterministic_credits']) for r in yellow.values()) + total[who] - overlap_total[who] for who in total}
    require(combined == {'kira': 155625, 'illi': 136600}, 'Combined non-duplicated gross mismatch')

    handoff = js('world-clock/ARC5_HANDOFF.json')
    require(handoff['checkpoint'] == 23 and handoff['start'] == 'Y6D4' and handoff['close'] == {'date': 'G6D2', 'purchase': 'Coherence Prime Elemental Red', 'cost': 9350}, 'Handoff boundaries changed')
    require(handoff['kira_solo']['first_blue_clear_date'] == 'G5D1' and handoff['kira_solo']['failed_wave'] == 20 and handoff['kira_solo']['w20_failure_depth'] is None, 'Kira milestone/depth mismatch')
    require(handoff['kira_solo']['paid_dates'] == list(kira_waves), 'Paid Solo dates mismatch')
    require(handoff['illi_solo']['outings'] == [{'date': 'G1D4', 'cleared_wave': 8, 'reached_wave': 9}, {'date': 'G3D2', 'cleared_wave': 9, 'reached_wave': 10}, {'date': 'G5D2', 'cleared_wave': 10, 'reached_wave': 11, 'failed_wave': 11}], 'illi milestones mismatch')
    require(handoff['illi_solo']['w11_failure_depth'] is None and not handoff['illi_solo']['green_solo_graduation'], 'illi scope exceeded')
    require(handoff['green_dungeon']['first_attempt_date'] == green_fail[0] and handoff['green_dungeon']['first_clear_date'] == green_clear[0] and handoff['green_dungeon']['failed_dates'] == green_fail and handoff['green_dungeon']['clear_dates'] == green_clear, 'Green milestones mismatch')
    require(handoff['fixed_gross_excluding_contextual_awards'] == total and handoff['gross_is_balance'] is False, 'Handoff income scope mismatch')
    require(handoff['domai_events'] == [{'date': 'Y7D4', 'rank': 'Orange', 'result': 'success', 'contextual_award': None, 'included_in_fixed_gross': False}, {'date': 'G6D1', 'rank': 'Yellow', 'result': 'failure', 'conquest_payout': 0}], 'Contextual domai/outcomes mismatch')
    require(handoff['girls_builder_nights'] == {'dates': nights, 'displaced': {'Y6D5': 'Duo Trial', 'Y7D5': 'Auction'}}, 'Social handoff mismatch')
    require(not handoff['green_domai'] and not handoff['meaningful_trio_push'] and handoff['reopen_requires_explicit_author'] and handoff['calendar_rows'] == 48, 'Frozen schedule scope mismatch')

    # Every unaffected baseline file, including all old provenance, must survive exactly.
    allowed = {
        '.gitattributes', 'README.md', 'THREAD_DEVELOPMENT_CONSTITUTION.md', 'builder/COMMUNITY.md', 'combat-rewards/DOMAI_GROUP_ECONOMY.md',
        *['live-model/' + p for p in ('00_GOVERNANCE.md', '01_KIRA.md', '03_VALNEK_PATHS.md', '04_COMBAT_WORLD.md', 'BLACK_SYSTEMS_MASTERY.md', 'COMBAT_ECOLOGY.md', 'COMBAT_THRESHOLDS.md', 'DOMAI_PARTICIPATION.md', 'ECONOMY_PURCHASE_SCHEDULE.md', 'ILLI_PROGRESSION.md', 'INDEX.md', 'OPEN.md', 'PARTNERSHIP_AND_CARRY.md', 'SOCIAL_LIFE_AND_FOUNDATIONS.md', 'STORY_CLOCK_STATE.md', 'SUPERSESSIONS.md', 'TRIAL_ARENA.md', 'WORLD_CLOCK.md')],
        *['world-clock/' + p for p in ('ARC5_HANDOFF.json', 'ARC5_HANDOFF.md', 'WORLD_CLOCK.md', 'YELLOW_DIRECTOR_CALENDAR.md', 'validate_yellow_director.py', 'YELLOW_DIRECTOR_AUDIT.json', 'ARC4_HANDOFF_AUDIT.json', 'ARC4_YELLOW_AUDIT.json')],
    }
    # CP24 replaces only the post-G6D2 projection; validate_arc6 checks prefix, mirrors and clock fields.
    allowed.update({'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json', 'world-clock/ARC3_ECONOMY_AUDIT.json', 'economy/validate_economy.py', 'combat-rewards/README.md', 'live-model/PRIME_ELEMENTALS.md', 'world-clock/validate_arc4_handoff.py', 'world-clock/WORLD_CLOCK_TEMPLATE.csv', 'bindings/PRICING_MODEL.md', 'world-clock/validate_arc3.py', 'economy/AUDIT.json', 'world-clock/ILLI_PROGRESSION_SKELETON.csv', 'world-clock/ARC4_HANDOFF.md', 'economy/KIRA_BLACK_ACQUISITION_PRICES.json', 'world-clock/validate_arc4_yellow.py', 'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv', 'world-clock/ILLI_PROGRESSION_SKELETON.json'})
    # Explicit CP25 surfaces; field/prefix preservation is audited by validate_arc7.
    allowed.update({'live-model/RAEON.md', 'live-model/GENESIS_CARDS.md', 'trial-rewards/README.md', 'combat-rewards/validate_rewards.py', 'combat-rewards/DOMAI_PARTICIPATION_RULES.json', 'combat-rewards/COMBAT_REWARD_TABLES.json'})
    # R2 city and cumulative R2/R3 prose changes require complete promotion
    # accounting; fixed reward and required-calendar assertions remain.
    try:
        allowed.update(validated_city_replacements(root))
        allowed.update(validated_replacements(root))
    except (OSError, ValueError, KeyError) as exc:
        require(False, 'Author promotion preservation: ' + str(exc))
    protected = []
    for path, digest in before['sha256'].items():
        if path not in allowed:
            require(sha(path) == digest, 'Unrelated baseline file altered: ' + path)
            protected.append(path)
    def old(path):
        return subprocess.check_output(['git', '-c', f'safe.directory={root.as_posix()}', 'show', before['baseline_commit'] + ':' + path], cwd=root).decode('utf-8')
    old_handoff = json.loads(old('world-clock/ARC5_HANDOFF.json'))
    replaced = {'checkpoint', 'status', 'kira_solo', 'green_dungeon'}
    for key, value in old_handoff.items():
        if key not in replaced:
            require(handoff[key] == value, 'Non-conflicting handoff doctrine altered: ' + key)
    for key, value in old_handoff['kira_solo'].items():
        if key != 'first_blue_clear_date': require(handoff['kira_solo'][key] == value, 'Kira capability altered: ' + key)
    carry = re.compile(r'(?ms)^## Project Princess Carry — LOCK\n.*?(?=^## )')
    require(carry.search(old('live-model/PARTNERSHIP_AND_CARRY.md')).group() == carry.search(text('live-model/PARTNERSHIP_AND_CARRY.md')).group(), 'Later Project Princess Carry changed')
    ledger = js('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json')
    require(len(ledger) == 19 and sum(r['cost'] for r in ledger) == 292772, 'illi ledger changed')
    require(next((r['season'], r['week'], r['day'], r['cost']) for r in ledger if r['purchase_or_upgrade'] == 'Coherence Prime → Red') == ('Green', 6, 2, 9350), 'Coherence Prime moved')
    registry_counts = {'bindings': len(js('bindings/BINDINGS.json')), 'summons': len(js('summons/SUMMONED_ENTITIES.json')), 'builder_paths': len(js('builder/paths/PATHS.json'))}
    require(registry_counts == {'bindings': 1016, 'summons': 229, 'builder_paths': 200}, 'Registry counts changed')
    require(text('live-model/30_CHECKPOINT_23_ARC5_COMBAT_CALENDAR.md').endswith(text(archive + 'ARC5_CALENDAR_SUMMARY.md')), 'Full author summary missing')
    content = {
        'world-clock/ARC5_DIRECTOR_CALENDAR.md': ['structurally frozen', '48 consecutive', 'SCAFFOLD', '88,595', '78,430', '13,110', '155,625', '136,600', '21–38', '31-hour', 'exact intraday', 'Arc Six'],
        'live-model/01_KIRA.md': ['G5D1', 'no defined mastery ceiling', '11-foot', 'W20 failure depth'],
        'live-model/BLACK_SYSTEMS_MASTERY.md': ['G5D1', 'G5D2', 'G5D3', 'G5D4/G5D7', 'No defined mastery ceiling', 'hundreds of yards/meters', 'Do not back-port'],
        'live-model/ILLI_PROGRESSION.md': ['G1D4', 'G3D2', 'G5D2', '1,275', '1,590', '1,950', '78,430', '9,350'],
        'live-model/OPEN.md': ['G5D1', 'G5D2', 'G5D3/G5D4/G5D7', 'OPEN BY DESIGN', 'W20 failure depth', 'W11 failure depth', 'Training Yard', 'Arc Six'],
        'live-model/DOMAI_PARTICIPATION.md': ['Y7D4 Orange', 'G6D1 Yellow', '0.8^deaths', 'group_award / eligible_members'],
        'builder/COMMUNITY.md': ['Girls\' Builder Night', 'G1D5', 'G5D5', 'Y6D5', 'Y7D5', 'G5D2', '200'],
    }
    for path, phrases in content.items():
        for phrase in phrases: require(phrase.lower() in text(path).lower(), 'Active content missing: ' + path + ': ' + phrase)
    stale = re.compile(r'at an (?:\*\*)?OPEN date|exact (?:breakthrough date|first Green clear/date|attempt/first-clear dates|attempts/first clear).{0,25}(?:OPEN|undated)|illi Solo exact standing remains OPEN|Exact date inside Arc Five|Exact illi Solo standing/rank during Arc Five', re.I)
    stale_hits = []
    for directory in ('live-model', 'world-clock'):
        for path in sorted((root / directory).glob('*.md')):
            if re.match(r'\d+_CHECKPOINT_', path.name): continue
            for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                if stale.search(line): stale_hits.append({'path': path.relative_to(root).as_posix(), 'line': number, 'text': line})
    require(not stale_hits, 'Stale active Arc Five date-OPEN language')
    inputs = ['world-clock/ARC5_DIRECTOR_CALENDAR.csv', 'world-clock/ARC5_DIRECTOR_CALENDAR.json', 'world-clock/ARC5_HANDOFF.json', 'world-clock/validate_arc5.py', 'trial-rewards/TRIAL_WAVE_CREDITS.json', 'combat-rewards/COMBAT_REWARD_TABLES.json', *content]
    return {'checkpoint': 23, 'result': 'FAIL' if errors else 'PASS', 'errors': errors, 'baseline_commit': before['baseline_commit'], 'calendar_rows': len(calendar), 'arc': 'Y6D4–G6D2', 'status': 'FULLY LOCKED', 'counts': dict(counts), 'fixed_gross_excluding_contextual_awards': total, 'income_by_category': dict(categories), 'daily_fixed_gross': daily, 'raid_bookings': raid_bookings, 'overlapping_yellow_dates': overlap, 'overlap_fixed_gross': overlap_total, 'combined_full_yellow_through_G6D2_fixed_gross': combined, 'girls_builder_nights': nights, 'registry_counts': registry_counts, 'illi_milestones': len(ledger), 'illi_progression_total': 292772, 'project_princess_carry_section_byte_identical': True, 'baseline_files_required_byte_identical': protected, 'stale_pattern': stale.pattern, 'stale_active_matches': stale_hits, 'gross_is_not_balance': True, 'contextual_orange_domai_award': None, 'failed_dungeon_partial_credits': 'OPEN/excluded', 'intraday_timing_and_failure_depth': 'OPEN; dates and completed waves locked', 'sha256': {p: sha(p) for p in sorted(set(inputs))}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write-audit', action='store_true')
    args = parser.parse_args()
    try:
        report = audit(args.repository.resolve())
    except (OSError, KeyError, ValueError, TypeError, IndexError, AttributeError, StopIteration, subprocess.CalledProcessError) as exc:
        report = {'result': 'FAIL', 'errors': [str(exc)]}
    if args.write_audit and report['result'] == 'PASS':
        (args.repository / 'world-clock/ARC5_DIRECTOR_AUDIT.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('daily_fixed_gross', 'baseline_files_required_byte_identical', 'sha256')}, indent=2, ensure_ascii=False))
    return 0 if report['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
