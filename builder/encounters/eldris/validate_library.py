"""Audit author-facing atomic eldris data using only the Python standard library."""

import argparse
from collections import Counter
import csv
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import re


CODES = 'ROYGBV'
BASINS = ('Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet')
COUNTS = dict(zip(CODES, (4, 10, 20, 35, 56, 84)))
AREAS = dict(zip(CODES + 'W', (5, 13, 25, 53, 113, 285, 450)))
EXPRESSIONS = ('Physical', 'Intrusion', 'Ranged force',
               'Juggernaut / persistence threshold', 'Expressed projection',
               'High Genesis expression')
PRESSURES = ('physical pressure', 'intrusion pressure', 'ranged-force pressure',
             'persistent/juggernaut anchor', 'projected-expression pressure',
             'high-Genesis-expression pressure')
NUMERIC = ('population', 'red', 'orange', 'yellow', 'green', 'blue', 'violet',
           'melee_count', 'transductionist_count')
FIELDS = ('group_id', 'highest_basin', 'highest_basin_code', 'population',
          'composition', 'red', 'orange', 'yellow', 'green', 'blue', 'violet',
          'melee_count', 'transductionist_count', 'tactical_profile', 'builder_note')
NOTES = {
    'Singleton atomic unit; combine with other atomic groups for larger encounters.',
    'Melee-family atomic group; combine with Transductionist groups when ranged/projected support is desired.',
    'Transductionist-family atomic group; combine with melee groups when screening/frontline pressure is desired.',
    'Self-contained mixed-role atomic group; suitable as a nucleus or flank when combined.',
}


def audit(directory):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def read_json(name):
        return json.loads((directory / name).read_text(encoding='utf-8-sig'))

    def read_csv(name):
        with (directory / name).open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            return reader.fieldnames, rows

    fields, rows = read_csv('ELDRIS_ATOMIC_GROUPS.csv')
    mirror = read_json('ELDRIS_ATOMIC_GROUPS.json')
    require(fields == list(FIELDS), 'CSV schema differs from the atomic composition schema')
    require(isinstance(mirror, list), 'JSON mirror must be a list')
    require(len(rows) == len(mirror) == 209, 'CSV/JSON must each contain 209 groups')
    ids, multisets, counts, populations = [], set(), Counter(), Counter()
    for row in rows:
        group_id = row['group_id']
        require(re.fullmatch(r'[ROYGBV][0-9]{3}', group_id) is not None,
                f'{group_id}: invalid ID or White group')
        for field in NUMERIC:
            require(re.fullmatch(r'\d+', row[field]) is not None,
                    f'{group_id}: {field} must be a nonnegative integer')
            row[field] = int(row[field])
        composition = tuple(row[basin.lower()] for basin in BASINS)
        represented = [i for i, count in enumerate(composition) if count]
        if not represented:
            errors.append(f'{group_id}: empty group')
            continue
        ceiling = max(represented)
        population = sum(composition)
        require(1 <= population <= 4 and row['population'] == population,
                f'{group_id}: atomic population must equal composition and be 1–4')
        require(row['highest_basin_code'] == CODES[ceiling]
                and row['highest_basin'] == BASINS[ceiling]
                and group_id.startswith(CODES[ceiling]),
                f'{group_id}: highest represented basin must equal the ID ceiling')
        expected_composition = '+'.join(f'{composition[i]}{CODES[i]}' for i in represented)
        require(row['composition'] == expected_composition,
                f'{group_id}: composition label mismatch')
        melee = sum(composition[i] for i in (0, 1, 3))
        transductionist = sum(composition[i] for i in (2, 4, 5))
        require(row['melee_count'] == melee and row['transductionist_count'] == transductionist,
                f'{group_id}: family counts mismatch')
        profile = row['tactical_profile'].split('; ')
        family = ('mixed melee/Transductionist' if melee and transductionist
                  else 'melee-only' if melee else 'Transductionist-only')
        require(profile[0] == family and len(profile[1:]) == len(represented)
                and set(profile[1:]) == {PRESSURES[i] for i in represented},
                f'{group_id}: profile must use the present basins and canonical family')
        require(row['builder_note'] in NOTES, f'{group_id}: unrecognized authoring note')
        require(composition not in multisets, f'{group_id}: duplicate unordered basin multiset')
        multisets.add(composition)
        ids.append(group_id)
        counts[CODES[ceiling]] += 1
        populations[population] += 1
    require(len(set(ids)) == len(ids), 'Duplicate group IDs')
    require(dict(counts) == COUNTS, 'Per-highest-basin counts mismatch')
    for code, count in COUNTS.items():
        require([group_id for group_id in ids if group_id.startswith(code)]
                == [f'{code}{n:03d}' for n in range(1, count + 1)],
                f'{code}: IDs must be unique and contiguous')
    expected = {
        tuple(combo.count(i) for i in range(6))
        for population in range(1, 5)
        for combo in combinations_with_replacement(range(6), population)
    }
    require(multisets == expected, 'Library does not exhaust all 1–4-body basin multisets')
    for row in mirror:
        require(set(row) == set(FIELDS), 'JSON row schema mismatch')
        for field in NUMERIC:
            require(type(row.get(field)) is int, f'{row.get("group_id")}: JSON {field} must be integer')
    require(rows == mirror, 'CSV/JSON records differ')

    availability = read_json('TIER_AVAILABILITY.json')
    require(set(availability) == set(CODES + 'W'), 'Availability tier keys mismatch')
    cumulative = {}
    for tier_index, code in enumerate(CODES + 'W'):
        legal = [group_id for group_id in ids if CODES.index(group_id[0]) <= min(tier_index, 5)]
        require(availability.get(code) == legal, f'{code}: cumulative availability is incomplete or illegal')
        cumulative[code] = len(legal)
    require(availability.get('W') == availability.get('V'), 'White availability must equal R→V only')

    _, references = read_csv('BASIN_REFERENCE.csv')
    require([row['code'] for row in references] == list(CODES + 'W'), 'Basin reference rows mismatch')
    for i, row in enumerate(references):
        code = row['code']
        require(int(row['normal_dungeon_area_mi2']) == AREAS[code], f'{code}: supplied area changed')
        if code == 'W':
            require(row['basin'] == 'White' and row['canonical_expression'] == 'No White eldris'
                    and row['combat_family'] == 'N/A', 'White reference must not introduce an eldris basin')
            require(row['normal_dungeon_rank_enabled'] == 'true'
                    and row['area_scope'] == 'locked_normal_dungeon_average', 'White Valnak Normal Dungeon must be enabled')
        else:
            require(row['basin'] == BASINS[i] and row['canonical_expression'] == EXPRESSIONS[i],
                    f'{code}: inherited basin taxonomy changed')
            require(row['combat_family'] == ('Melee' if code in 'ROG' else 'Transductionist'),
                    f'{code}: basin combat family mismatch')
            require(row['normal_dungeon_rank_enabled'] == 'true'
                    and row['area_scope'] == 'locked_normal_dungeon_average', f'{code}: area scope mismatch')
    manifest = read_json('MANIFEST.json')
    require(manifest['total_groups'] == 209 and manifest['counts_by_highest_basin'] == COUNTS
            and manifest['max_atomic_population'] == 4 and manifest['white_eldris'] is False,
            'Manifest group constraints mismatch')
    require(manifest['areas_mi2'] == AREAS and manifest['author_tooling_only'] is True
            and manifest['normal_dungeon_rank_codes'] == list(CODES + 'W')
            and manifest['domai_rank_codes'] == list(CODES)
            and manifest['white_area_application'] == 'locked_valnak_normal_dungeon_average',
            'Manifest area/tooling scope mismatch')
    lookup = {row['group_id']: row for row in rows}
    example = sum(lookup[group_id]['population'] * copies for group_id, copies in
                  [('R004', 2), ('O006', 2), ('Y012', 1), ('G018', 1), ('B021', 1)])
    require(example == 25, 'Documented example population mismatch')
    for name in ('README.md', 'BUILDER_CONTRACT.md', 'BASIN_REFERENCE.csv'):
        text = (directory / name).read_text(encoding='utf-8')
        require(all(match.group() == 'eldris' for match in re.finditer(r'\beldris\b', text, re.I)),
                f'{name}: active eldris prose must be lowercase')
    inputs = ('ELDRIS_ATOMIC_GROUPS.csv', 'ELDRIS_ATOMIC_GROUPS.json', 'TIER_AVAILABILITY.json',
              'BASIN_REFERENCE.csv', 'MANIFEST.json', 'BUILDER_CONTRACT.md', 'README.md', 'validate_library.py')
    return {
        'result': 'FAIL' if errors else 'PASS', 'errors': errors,
        'total_groups': len(rows), 'counts_by_highest_basin': dict(counts),
        'population_distribution': dict(sorted(populations.items())),
        'population_bounds': [1, 4], 'cumulative_availability': cumulative,
        'exhaustive_unordered_multisets': multisets == expected,
        'csv_json_equivalent': rows == mirror, 'white_eldris': False,
        'normal_dungeon_rank_codes': list(CODES + 'W'), 'domai_rank_codes': list(CODES), 'areas_mi2': AREAS,
        'white_area_scope': 'locked_valnak_normal_dungeon_average',
        'example_population': example,
        'checks': ['ID uniqueness and sequence', 'population and composition', 'highest-basin ceilings',
                   'exhaustive combinations', 'combat-family partitions', 'mechanistic-only profile vocabulary',
                   'CSV/JSON schemas and equality', 'cumulative availability', 'basin taxonomy',
                   'area values and content permission', 'author-tooling scope', 'lowercase active terminology'],
        'sha256': {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in inputs},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, help='Optional JSON audit file; default is read-only stdout.')
    args = parser.parse_args()
    try:
        report = audit(args.directory)
    except (KeyError, ValueError, TypeError, IndexError, OSError) as error:
        report = {'result': 'FAIL', 'errors': [str(error)]}
    text = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8', newline='\n')
    print(text, end='')
    return 0 if report['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
