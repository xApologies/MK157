"""Validate Checkpoint 18 reward data with the Python standard library."""

import argparse
import csv
import hashlib
import json
from pathlib import Path


RANKS = ('Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet', 'White')
NORMAL_DUNGEON = (395, 1020, 2305, 4550, 7800, 13750, 34455)
HARD_DUNGEON = (593, 1530, 3458, 6825, 11700, 20625, 51683)
NORMAL_RAID = (2500, 3750, 5000, 7500, 11250, 17500)
HARD_RAID = (3750, 5625, 7500, 11250, 16875, 26250)
AREAS = dict(zip('ROYGBVW', (5, 13, 25, 53, 113, 285, 450)))


def audit(directory, repository):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    tables = json.loads((directory / 'COMBAT_REWARD_TABLES.json').read_text(encoding='utf-8-sig'))
    require(set(tables) == {'dungeons', 'raids', 'domai'}, 'Unexpected reward categories')
    rows_checked = 0
    results = {}
    for section, name, fields, ranks, normal, hard in (
        ('dungeons', 'DUNGEON_REWARDS.csv',
         ('rank', 'normal_completion_credits', 'hard_completion_credits', 'hard_multiplier'),
         RANKS, NORMAL_DUNGEON, HARD_DUNGEON),
        ('raids', 'RAID_BOSS_REWARDS.csv',
         ('boss_rank', 'normal_boss_credits', 'expedition_hard_boss_credits', 'hard_multiplier'),
         RANKS[:-1], NORMAL_RAID, HARD_RAID),
    ):
        with (directory / name).open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            require(reader.fieldnames == list(fields), f'{name}: schema mismatch')
        require([row[fields[0]] for row in rows] == list(ranks), f'{name}: rank order/count mismatch')
        expected_keys = {'normal', 'hard', 'hard_multiplier', 'hard_rounding'}
        if section == 'raids':
            expected_keys |= {'normal_total', 'hard_total'}
        require(set(tables[section]) == expected_keys, f'{section}: unexpected JSON fields')
        require(tables[section]['hard_multiplier'] == 1.5, f'{section}: multiplier must be 1.5')
        require(tables[section]['hard_rounding'] == 'ROUND_HALF_UP', f'{section}: rounding must be HALF_UP')
        values = {'normal': [], 'hard': []}
        for row in rows:
            rank = row[fields[0]]
            n, h = int(row[fields[1]]), int(row[fields[2]])
            require(row[fields[3]] == '1.5', f'{name}/{rank}: multiplier must be 1.5')
            require(n > 0 and h > 0 and h == (n * 3 + 1) // 2,
                    f'{name}/{rank}: hard != HALF_UP(1.5x normal)')
            values['normal'].append(n)
            values['hard'].append(h)
            rows_checked += 1
        for mode, supplied in (('normal', normal), ('hard', hard)):
            require(values[mode] == list(supplied), f'{section}/{mode}: differs from locked values')
            mirror = tables[section][mode]
            require(set(mirror) == set(ranks), f'{section}/{mode}: JSON rank keys mismatch')
            require(all(type(value) is int for value in mirror.values()), f'{section}/{mode}: credits must be integers')
            require(mirror == dict(zip(ranks, values[mode])), f'{section}/{mode}: CSV/JSON mismatch')
        results[section] = {mode: dict(zip(ranks, values[mode])) for mode in values}

    totals = {mode: sum(results['raids'][mode].values()) for mode in ('normal', 'hard')}
    require(totals == {'normal': 47500, 'hard': 71250}, 'Raid one-per-rank totals mismatch')
    require(totals['normal'] * 3 == totals['hard'] * 2, 'Raid total multiplier mismatch')
    for mode, total in totals.items():
        require(type(tables['raids'][mode + '_total']) is int
                and tables['raids'][mode + '_total'] == total, f'{mode}: JSON Raid total mismatch')

    domai = tables['domai']
    require(set(domai) == {'reward_formula', 'rule'}, 'domai must not gain a fixed numeric table')
    require(domai['reward_formula'] == 'OPEN BY DESIGN', 'domai formula must remain OPEN BY DESIGN')
    for concept in ('contextual validated-contribution', 'no fixed rank table', 'eldris kills',
                    'healing/support', 'control', 'operational contribution', 'core assault',
                    'other validated participation', 'CP25 R/O/Y/G core-break awards are a separate layer in DOMAI_CORE_AWARDS.json; Blue/Violet successful core amounts OPEN'):
        require(concept in domai['rule'], f'domai contribution boundary missing: {concept}')

    manifest_path = repository / 'builder/encounters/eldris/MANIFEST.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    require(manifest['areas_mi2'] == manifest['hard_dungeon_areas_mi2'] == AREAS,
            'Hard must use the same seven average areas as Normal; no 1.5x area')
    require(manifest['normal_dungeon_rank_codes'] == manifest['hard_dungeon_rank_codes'] == list(AREAS),
            'Normal and Hard ranks must both be R through W')
    require(manifest['white_eldris'] is False and manifest['total_groups'] == 209
            and manifest['max_atomic_population'] == 4, 'Atomic vocabulary constraints changed')
    require(manifest['domai_rank_codes'] == list('ROYGBV'), 'domai ranks must remain R through V')

    inputs = {name: directory / name for name in
              ('DUNGEON_REWARDS.csv', 'RAID_BOSS_REWARDS.csv', 'COMBAT_REWARD_TABLES.json',
               'README.md', 'validate_rewards.py')}
    inputs['builder/encounters/eldris/MANIFEST.json'] = manifest_path
    return {
        'checkpoint': 18, 'result': 'FAIL' if errors else 'PASS', 'errors': errors,
        'reward_tables': results, 'exact_multiplier_pairs_checked': rows_checked,
        'integer_arithmetic': 'hard == (normal * 3 + 1) // 2 (positive whole-credit HALF_UP)',
        'raid_one_boss_per_rank_totals': totals,
        'hard_and_normal_average_areas_mi2': manifest['hard_dungeon_areas_mi2'],
        'domai_reward_formula': domai['reward_formula'],
        'checks': ['exact supplied values', 'CSV schemas/rank order', 'integer JSON values and CSV mirrors',
                   '13 exact payout multiplications', 'Raid sums and total multiplier',
                   'Hard/Normal areas and rank permissions', 'unchanged atomic vocabulary constraints',
                   'OPEN BY DESIGN domai and contribution dimensions'],
        'sha256': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in inputs.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--repository', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output', type=Path, help='Save the JSON audit; otherwise read-only stdout.')
    args = parser.parse_args()
    try:
        report = audit(args.directory, args.repository)
    except (KeyError, ValueError, TypeError, IndexError, OSError) as error:
        report = {'result': 'FAIL', 'errors': [str(error)]}
    text = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8', newline='\n')
    print(text, end='')
    return 0 if report['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
