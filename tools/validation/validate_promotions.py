"""Read-only accounting for explicit author promotions after the R1 audit.

Historical coverage is evidence about its pinned revision. A declared promotion
must account for the replacement bytes and every supplied source paragraph;
it is not permission to ignore later, undeclared drift.
"""
from pathlib import PurePosixPath
import hashlib
import json
import re
import subprocess


def digest(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def sections(text):
    """Partition the supplied delta at level-two headings, preserving paragraphs."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith('## ')]
    result = []
    for n, start in enumerate(starts):
        end = starts[n+1] if n+1 < len(starts) else len(lines)
        body = '\n'.join(lines[start+1:end]).strip()
        result.append({'section': lines[start][3:], 'body_sha256': digest(body),
                       'paragraphs': [digest(p) for p in re.split(r'\n\s*\n', body) if p.strip()]})
    return result


def check_coverage(text, rows, require, target):
    expected = sections(text)
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


def audit_promotions(root, git, require, target):
    registry_path = root/'canon/PROMOTIONS.json'
    empty = {'changed': set(), 'source_paths': set(), 'prefixes': (), 'package_prefixes': (), 'reports': []}
    if not registry_path.exists(): return empty
    registry = json.loads(registry_path.read_text(encoding='utf-8-sig'))
    entries = registry['promotions']
    require(len({e['id'] for e in entries}) == len(entries), 'duplicate promotion id')
    result = empty
    latest = {}
    modes = {}
    for record in subprocess.check_output(git+['ls-files', '--stage', '-z']).split(b'\0'):
        if record:
            meta, name = record.split(b'\t'); mode, blob, stage = meta.decode().split()
            require(stage == '0', 'unmerged promotion file: '+name.decode())
            modes[name.decode()] = mode
    for entry in entries:
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
        source = manifest['source']
        require(source in manifest['package_sha256'], 'unaccounted promotion source')
        target(source)
        check_coverage((root/source).read_text(encoding='utf-8-sig'), manifest['coverage'], require, target)
        for decision in manifest['supersessions']:
            require(bool(decision.get('scope')) and bool(decision.get('decision')), 'unscoped promotion supersession')
            for dest in decision['destinations']: target(dest)
        result['changed'].update(changes)
        result['source_paths'].add(source)
        result['prefixes'] += (prefix,)
        result['package_prefixes'] += (prefix+'package/',)
        result['reports'].append({'id': entry['id'], 'baseline_commit': revision, 'baseline_files': len(originals), 'changed_files': len(changes), 'source_sections': len(manifest['coverage']), 'source_paragraphs': sum(len(r['paragraphs']) for r in manifest['coverage']), 'semantic_limit': 'Digests and destinations verify accounting; the integration record separately records semantic decisions and unresolved chronology.'})
    for p, expected in latest.items():
        require((root/p).is_file() and digest((root/p).read_bytes()) == expected, 'undeclared promotion drift or missing file: '+p)
    return result
