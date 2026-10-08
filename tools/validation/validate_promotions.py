"""Read-only accounting for explicit author promotions after the R1 audit.

Historical coverage is evidence about its pinned revision. A declared promotion
must account for the replacement bytes and every supplied source paragraph;
it is not permission to ignore later, undeclared drift.
"""
from pathlib import PurePosixPath
import csv
import hashlib
import json
import re
import subprocess


def digest(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def sections(text, include_preamble=False):
    """Partition the supplied delta at level-two headings, preserving paragraphs."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith('## ')]
    result = []
    if include_preamble:
        body = '\n'.join(lines[1:starts[0] if starts else len(lines)]).strip()
        if body:
            result.append({'section': 'Document introduction', 'body_sha256': digest(body),
                           'paragraphs': [digest(p) for p in re.split(r'\n\s*\n', body) if p.strip()]})
    for n, start in enumerate(starts):
        end = starts[n+1] if n+1 < len(starts) else len(lines)
        body = '\n'.join(lines[start+1:end]).strip()
        result.append({'section': lines[start][3:], 'body_sha256': digest(body),
                       'paragraphs': [digest(p) for p in re.split(r'\n\s*\n', body) if p.strip()]})
    return result


def check_coverage(text, rows, require, target, include_preamble=False):
    expected = sections(text, include_preamble)
    require(len(rows) == len(expected), 'promotion section count')
    for actual, row in zip(expected, rows):
        require(row.get('section') == actual['section'], 'promotion section order/title')
        require(row.get('body_sha256') == actual['body_sha256'], 'promotion section digest: ' + actual['section'])
        claims = row.get('paragraphs', [])
        require([p.get('sha256') for p in claims] == actual['paragraphs'], 'promotion paragraph partition: ' + actual['section'])
        for claim in claims:
            require(claim.get('status') in {'CURRENT', 'WORKING', 'OPEN', 'MIXED_PARTIAL'}, 'promotion claim status')
            require(bool(claim.get('reason')), 'promotion claim decision missing')
            require(bool(claim.get('destinations')), 'promotion claim has no destination')
            for dest in claim.get('destinations', []): target(dest)


def safe_path(path):
    return isinstance(path, str) and bool(path) and not PurePosixPath(path).is_absolute() and ':' not in path and '\\' not in path and '..' not in PurePosixPath(path).parts


def historical_content(path, current, revision, promoted, git_read):
    """Only a separately validated promotion admits a historical coverage input."""
    return git_read(revision + ':' + path).decode('utf-8-sig') if path in promoted else current


def relocated_city_row(row, old_serial, new_serial):
    """Only the October 8 festival-ID correction; preserve the venue record."""
    if (old_serial, new_serial) != ('007', '008') or row.get('serial') != old_serial:
        raise ValueError('Unapproved city serial relocation')
    if row.get('canonical_name') != 'Opening Ceremony / civic festival grounds':
        raise ValueError('City relocation must preserve the existing festival venue')
    result = dict(row, serial=new_serial)
    result['notes'] = re.sub(r'(?<![\w-])007(?![\w-])', '008', row['notes'])
    return result


def current_tabular_rows(rows, destination, source_order, relocations, require):
    """Apply later, explicitly recorded relocations to historical source rows."""
    result = [dict(row) for row in rows]
    for order, relocation in relocations:
        if order <= source_order or relocation['destination'] != destination:
            continue
        matches = [i for i, row in enumerate(result) if row.get('serial') == relocation['from_value']]
        for i in matches:
            require(result[i] == relocation['before_row'], 'relocation source row differs')
            result[i] = relocated_city_row(result[i], relocation['from_value'], relocation['to_value'])
    return result


def audit_promotions(root, git, require, target):
    registry_path = root/'canon/PROMOTIONS.json'
    empty = {'changed': set(), 'source_paths': set(), 'asset_paths': set(), 'owner_paths': set(), 'prefixes': (), 'package_prefixes': (), 'reports': []}
    if not registry_path.exists(): return empty
    registry = json.loads(registry_path.read_text(encoding='utf-8-sig'))
    entries = registry['promotions']
    require(len({e['id'] for e in entries}) == len(entries), 'duplicate promotion id')
    result = empty
    tabular_checks = []
    relocations = []
    latest = {}
    modes = {}
    for record in subprocess.check_output(git+['ls-files', '--stage', '-z']).split(b'\0'):
        if record:
            meta, name = record.split(b'\t'); mode, blob, stage = meta.decode().split()
            require(stage == '0', 'unmerged promotion file: '+name.decode())
            modes[name.decode()] = mode
    for entry_order, entry in enumerate(entries):
        path = entry['manifest']
        require(safe_path(path) and path.startswith('provenance/') and path.endswith('/INTEGRATION.json'), 'unsafe promotion manifest path')
        if not safe_path(path): continue
        target(path)
        manifest = json.loads((root/path).read_text(encoding='utf-8-sig'))
        prefix = str(PurePosixPath(path).parent) + '/'
        require(manifest['id'] == entry['id'], 'promotion identity mismatch')
        revision = manifest['baseline_commit']
        require(bool(re.fullmatch('[0-9a-f]{40}', revision)), 'promotion baseline must be a full commit')
        if not re.fullmatch('[0-9a-f]{40}', revision): continue
        snapshot = json.loads((root/(prefix+'BASELINE.json')).read_text(encoding='utf-8-sig'))
        require(snapshot['commit'] == revision, 'promotion baseline mismatch')
        tree = subprocess.check_output(git+['ls-tree', '-rz', revision]).split(b'\0')
        originals = {}
        for record in tree:
            if not record: continue
            meta, name = record.split(b'\t'); mode, kind, blob = meta.decode().split()
            originals[name.decode()] = {'mode': mode, 'blob': blob}
        require(set(snapshot['files']) == set(originals), 'promotion baseline file inventory')
        # Git object identities verify baseline bytes without one process per file.
        blob_ids = [r['blob'] for r in originals.values()]
        raw = subprocess.check_output(git+['cat-file', '--batch'], input=('\n'.join(blob_ids)+'\n').encode())
        position = 0
        for p, original in originals.items():
            end = raw.index(b'\n', position); size = int(raw[position:end].split()[2])
            data = raw[end+1:end+1+size]; position = end+2+size
            record = snapshot['files'].get(p, {})
            require(all(record.get(k) == v for k, v in original.items()) and record.get('sha256') == digest(data), 'promotion baseline object: '+p)
        changes = manifest['changed_paths']
        require(set(changes) <= set(originals), 'promotion changes reference unknown baseline file')
        for p, record in changes.items():
            require(record['before_sha256'] == snapshot['files'][p]['sha256'], 'promotion preimage: '+p)
            require(record['before_sha256'] != record['after_sha256'], 'promotion declares unchanged file: '+p)
            latest[p] = record['after_sha256']
        # Every baseline file is preserved or explicitly accounted for. Later
        # promotions override earlier current hashes, never the archived evidence.
        for p, record in snapshot['files'].items():
            latest.setdefault(p, record['sha256'])
            require(modes.get(p) == record['mode'], 'promotion file mode changed or untracked: '+p)
        for p, expected in manifest['package_sha256'].items():
            require(safe_path(p) and p.startswith(prefix+'package/'), 'package outside promotion')
            if safe_path(p): require((root/p).is_file() and digest((root/p).read_bytes()) == expected, 'promotion package bytes: '+p)
        for p, expected in manifest.get('generated_owners', {}).items():
            require(entry['id'] == 'live-model-full-repair-2026-10-08' and
                    p in {'world-clock/KIRA_CREDIT_LEDGER.csv', 'world-clock/KIRA_CREDIT_LEDGER.json'},
                    'unapproved generated owner: '+p)
            require(prefix+'package/package/KIRA_LEDGER_SPEC.md' in manifest['package_sha256'],
                    'Kira ledger specification missing')
            if safe_path(p):
                require((root/p).is_file() and digest((root/p).read_bytes()) == expected,
                        'generated owner drift: '+p)
                result['owner_paths'].add(p)
        for asset in manifest.get('asset_copies', []):
            source, dest = asset['source'], asset['destination']
            require(source in manifest['package_sha256'], 'asset source not accounted for')
            require(safe_path(dest) and dest.startswith('visual-references/'), 'unapproved asset destination')
            if safe_path(dest) and safe_path(source):
                target(source); target(dest)
                require((root/dest).is_file() and digest((root/dest).read_bytes()) == manifest['package_sha256'].get(source), 'asset copy differs from supplied bytes')
                result['asset_paths'].add(dest)
        for relocation in manifest.get('registry_relocations', []):
            dest = relocation['destination']
            require(dest == 'visual-references/CITY_LOCATION_REGISTRY.csv' and dest in changes, 'unapproved relocation destination')
            require(relocation.get('key') == 'serial', 'unapproved relocation key')
            require(relocation['source'].split('#')[0] in manifest['package_sha256'], 'relocation source not accounted for')
            require(bool(relocation.get('reason')), 'relocation reason missing')
            target(relocation['source']); target(dest)
            original = subprocess.check_output(git + ['show', revision + ':' + dest]).decode('utf-8-sig')
            original_rows = list(csv.DictReader(original.splitlines()))
            require(relocation['before_row'] in original_rows, 'relocation preimage missing from baseline')
            require(not any(r['serial'] == relocation['to_value'] for r in original_rows), 'relocation target serial already used')
            expected_row = relocated_city_row(relocation['before_row'], relocation['from_value'], relocation['to_value'])
            require(relocation['after_row'] == expected_row, 'relocation alters unrelated venue fields')
            relocations.append((entry_order, relocation))
        documents = manifest.get('source_documents', [{'source': manifest.get('source'), 'coverage': manifest.get('coverage', [])}])
        require(bool(documents), 'promotion has no source coverage')
        require(len({d['source'] for d in documents}) == len(documents), 'duplicate promotion source')
        for document in documents:
            source = document['source']
            require(source in manifest['package_sha256'], 'unaccounted promotion source')
            target(source)
            check_coverage((root/source).read_text(encoding='utf-8-sig'), document['coverage'], require, target, document.get('include_preamble', False))
            result['source_paths'].add(source)
        table_rows = 0
        for table in manifest.get('tabular_sources', []):
            source = table['source']; dest = table['destination']; key = table['key']
            require(source in manifest['package_sha256'], 'unaccounted tabular source')
            target(source); target(dest)
            with (root/source).open(encoding='utf-8-sig', newline='') as f: supplied = list(csv.DictReader(f))
            with (root/dest).open(encoding='utf-8-sig', newline='') as f: current = list(csv.DictReader(f))
            require(len({r[key] for r in current}) == len(current), 'duplicate target registry key')
            require(len({r[key] for r in supplied}) == len(supplied), 'duplicate supplied registry key')
            require(table['row_digests'] == [digest(json.dumps(r, sort_keys=True, ensure_ascii=False)) for r in supplied], 'tabular source row accounting')
            tabular_checks.append((entry_order, dest, key, supplied, current))
            table_rows += len(supplied)
        for decision in manifest['supersessions']:
            require(bool(decision.get('scope')) and bool(decision.get('decision')), 'unscoped promotion supersession')
            for dest in decision['destinations']: target(dest)
        result['changed'].update(changes)
        result['prefixes'] += (prefix,)
        result['package_prefixes'] += (prefix+'package/',)
        result['reports'].append({'id': entry['id'], 'baseline_commit': revision, 'baseline_files': len(originals), 'changed_files': len(changes), 'source_documents': len(documents), 'source_sections': sum(len(d['coverage']) for d in documents), 'source_paragraphs': sum(len(r['paragraphs']) for d in documents for r in d['coverage']), 'tabular_source_rows': table_rows, 'semantic_limit': 'Digests and destinations verify accounting; the integration record separately records semantic decisions and unresolved chronology.'})
    for p, expected in latest.items():
        require((root/p).is_file() and digest((root/p).read_bytes()) == expected, 'undeclared promotion drift or missing file: '+p)
    for order, dest, key, supplied, current in tabular_checks:
        expected = current_tabular_rows(supplied, dest, order, relocations, require)
        indexed = {r[key]: r for r in current}
        require(all(indexed.get(r[key]) == r for r in expected), 'supplied registry rows differ from current owner')
    for _, relocation in relocations:
        with (root/relocation['destination']).open(encoding='utf-8-sig', newline='') as stream:
            current = list(csv.DictReader(stream))
        require(relocation['after_row'] in current, 'relocated venue missing from current registry')
    return result


def validated_city_replacements(root):
    """Narrow later-author exception to old checkpoint byte-preservation guards.

    No numeric input is exempted. City paths require explicit replacement
    records in a fully valid promotion chain; undeclared drift still fails.
    The October 8 visual index is append-only against its own pinned baseline.
"""
    git = ['git', '-c', f'safe.directory={root.as_posix()}', '-C', str(root)]
    errors = []
    def require(ok, message):
        if not ok: errors.append(message)
    def target(path):
        require((root/path.split('#', 1)[0]).exists(), 'missing promotion destination: '+path)
    report = audit_promotions(root, git, require, target)
    if errors: raise ValueError('; '.join(errors))
    allowed = report['changed'] & {'live-model/VALNAK_CITY_CULTURE_TRANSPORT.md', 'visual-references/CITY_LOCATION_REGISTRY.csv'}
    manifest_path = root/'provenance/diplomatic-pouch-2026-10-08/INTEGRATION.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
        path = 'visual-references/INDEX.md'
        if path in report['changed'] and path in manifest['changed_paths']:
            before = subprocess.check_output(git + ['show', manifest['baseline_commit'] + ':' + path])
            if not (root/path).read_bytes().startswith(before):
                raise ValueError('October 8 visual index must preserve its historical prefix')
            allowed.add(path)
    return allowed
