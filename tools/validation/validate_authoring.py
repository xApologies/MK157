"""Read-only R1 authoring audit. Python standard library; JSON on stdout.

Validates the supplied schemas' explicit keyword subset (not a general JSON
Schema engine), coverage partitions, local Markdown routes and source owners.
Historical links are inventoried separately from the active authoring surface.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import collections
import hashlib
import html
import json
import re
import subprocess
import unicodedata

MAINT = 'provenance/maintenance/authoring-cleanup-r1'
NAV = {'README.md', 'live-model/INDEX.md'}
PREFIXES = ('canon/', 'story/', 'data/', 'tools/', 'upstream/', MAINT + '/')


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def visible_markdown(text):
    """Blank fenced/indented code and comments, retaining line positions."""
    text = re.sub(r'<!--.*?-->', lambda m: re.sub(r'[^\n]', ' ', m[0]), text, flags=re.S)
    out = []; fence = None
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            out.append(''); continue
        if match:
            fence = match[1]; out.append(''); continue
        out.append('' if line.startswith(('    ', '\t')) else line)
    return '\n'.join(out)


def slug(text):
    text = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = html.unescape(text).replace('`', '').replace('**', '').lower()
    return ''.join(c for c in text if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')


def headings(text):
    seen = collections.Counter(); result = []
    lines = visible_markdown(text).splitlines()
    for i, line in enumerate(lines):
        match = re.match(r'^ {0,3}#{1,6}\s+(.+?)\s*#*$', line)
        title = match[1] if match else None
        if title is None and i + 1 < len(lines) and line.strip() and re.fullmatch(r' {0,3}(?:=+|-+)\s*', lines[i+1]):
            title = line.strip()
        if title is not None:
            base = slug(title); count = seen[base]; seen[base] += 1
            result.append((title, base + (f'-{count}' if count else ''), i + 1))
    return result


def destination(value):
    value = value.strip()
    if value.startswith('<'):
        end = value.find('>')
        return value[1:end] if end >= 0 else value
    return re.split(r'\s+[\'\"]', value, maxsplit=1)[0].strip()


def markdown_links(text):
    """Inline/image, full/collapsed/shortcut references, and HTML href/src."""
    clean = visible_markdown(text)
    clean = re.sub(r'(`+)([^`]|(?!\1)`)*?\1', lambda m: ' ' * len(m[0]), clean)
    refs = {}; excluded = set(); results = []
    normalize = lambda s: ' '.join(s.lower().split())
    for i, line in enumerate(clean.splitlines(), 1):
        m = re.match(r'^ {0,3}\[([^]]+)\]:\s*(.+)$', line)
        if m:
            refs[normalize(m[1])] = destination(m[2]); excluded.add(i)
            results.append((i, destination(m[2]), 'reference-definition'))
    for line_no, line in enumerate(clean.splitlines(), 1):
        if line_no in excluded: continue
        for m in re.finditer(r'\b(?:href|src)=[\"\']([^\"\']+)[\"\']', line):
            results.append((line_no, html.unescape(m[1]), 'html'))
        i = 0
        while i < len(line):
            if line[i] != '[' or (i and line[i-1] == '\\'):
                i += 1; continue
            start = i; depth = 1; i += 1
            while i < len(line) and depth:
                if line[i] == '\\': i += 2; continue
                depth += (line[i] == '[') - (line[i] == ']'); i += 1
            if depth: break
            label = line[start+1:i-1]
            if i < len(line) and line[i] == '(':
                begin = i+1; i += 1; depth = 1; angle = False
                while i < len(line) and depth:
                    c = line[i]
                    if c == '\\': i += 2; continue
                    if c == '<': angle = True
                    if c == '>': angle = False
                    if not angle: depth += (c == '(') - (c == ')')
                    i += 1
                if not depth: results.append((line_no, destination(line[begin:i-1]), 'inline'))
            elif i < len(line) and line[i] == '[':
                end = line.find(']', i+1)
                if end >= 0:
                    key = normalize(line[i+1:end] or label); i = end+1
                    results.append((line_no, refs.get(key, 'UNDEFINED_REFERENCE:' + key), 'reference'))
            elif normalize(label) in refs:
                results.append((line_no, refs[normalize(label)], 'shortcut'))
    return results


def fragments(body):
    """Stable coordinates used by the R1 ledger; no status inference here."""
    result = {}
    for pn, paragraph in enumerate(re.split(r'\n\s*\n', body), 1):
        logical = []; pending = []
        for line in paragraph.splitlines():
            if re.match(r'^\s*(?:[-*+] |\d+\. |\|)', line):
                if pending: logical.append(' '.join(pending)); pending = []
                logical.append(line.strip())
            else: pending.append(line.strip())
        if pending: logical.append(' '.join(pending))
        parts = []
        for line in logical:
            if re.fullmatch(r'[-| :]+', line): continue
            for atom in re.split(r'(?<=[.!?;])\s+(?=[A-Za-z*`])', line):
                parts.extend(re.split(r',\s+(?=[A-Za-z*`])', atom) if 'open' in atom.lower() and atom.count(',') > 1 else [atom])
        for n, part in enumerate(parts, 1): result[(pn, n)] = sha(part)
    return result


def schema_check(value, schema, at='$'):
    allowed = {'$schema', 'type', 'required', 'properties', 'items', 'minItems', 'minLength', 'enum', 'const', 'pattern'}
    unknown = set(schema) - allowed
    if unknown: raise ValueError(f'{at}: unsupported schema keywords {sorted(unknown)}')
    kinds = {'object': dict, 'array': list, 'string': str, 'null': type(None)}
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not any(isinstance(value, kinds[t]) for t in types): raise ValueError(f'{at}: wrong type')
    for key in ('enum', 'const'):
        if key in schema and (value not in schema[key] if key == 'enum' else value != schema[key]): raise ValueError(f'{at}: {key}')
    if 'pattern' in schema and not re.search(schema['pattern'], value): raise ValueError(f'{at}: pattern')
    for key in ('minItems', 'minLength'):
        if key in schema and len(value) < schema[key]: raise ValueError(f'{at}: {key}')
    if isinstance(value, dict):
        if set(schema.get('required', [])) - value.keys(): raise ValueError(f'{at}: missing required property')
        for key, rule in schema.get('properties', {}).items():
            if key in value: schema_check(value[key], rule, at + '.' + key)
    if isinstance(value, list) and 'items' in schema:
        for i, item in enumerate(value): schema_check(item, schema['items'], f'{at}[{i}]')


def audit(root):
    failures = []; checks = {}; cache = {}
    def require(condition, message):
        if not condition: failures.append(message)
    def read(path): return (root/path).read_text(encoding='utf-8-sig')
    def load(path): return json.loads(read(path))
    baseline = load(MAINT + '/BASELINE.json'); original = set(baseline['files'])
    git = ['git', '-c', f'safe.directory={root.as_posix()}', '-C', str(root)]
    tracked = subprocess.check_output(git + ['ls-files', '-z']).decode().split('\0')
    untracked = subprocess.check_output(git + ['ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0')
    files = sorted(set(tracked + untracked) - {''})
    added = set(files) - original
    require(all(p in {'AGENTS.md', 'CANON_STATUS.md'} or p.startswith(PREFIXES) for p in added), 'new path outside allowed surfaces')
    parsed = []
    for p in files:
        if p in added and p.endswith('.json'):
            try: load(p); parsed.append(p)
            except (ValueError, OSError) as e: failures.append(f'JSON {p}: {e}')
    coverage = load(MAINT + '/SOURCE_COVERAGE.json'); authority = load('canon/AUTHORITY_MAP.json')
    for value, name in ((coverage, 'coverage'), (authority, 'authority_map')):
        try: schema_check(value, load(MAINT + f'/package/schemas/{name}.schema.json'))
        except ValueError as e: failures.append(str(e))
    checks['json'] = {'parsed_count': len(parsed), 'files': parsed, 'schemas': ['coverage', 'authority_map'], 'engine': 'Strict implementation of the keyword subset present in the two supplied schemas; unknown keywords fail.'}
    def target_error(source, raw):
        if raw.startswith('UNDEFINED_REFERENCE:'): return raw
        raw = re.sub(r'\\([()\[\] ])', r'\1', html.unescape(raw))
        parts = urlsplit(raw)
        if parts.scheme or raw.startswith('//'): return None
        path = unquote(parts.path)
        candidate = (root/path.lstrip('/') if path.startswith('/') else (root/source).parent/path).resolve() if path else (root/source).resolve()
        if not candidate.is_relative_to(root): return 'outside repository'
        if not candidate.exists(): return 'missing target'
        if parts.fragment and candidate.suffix.lower() == '.md':
            if candidate not in cache:
                content = candidate.read_text(encoding='utf-8-sig')
                cache[candidate] = {a for _, a, _ in headings(content)} | set(re.findall(r'\b(?:id|name)=[\"\']([^\"\']+)[\"\']', visible_markdown(content)))
            if unquote(parts.fragment) not in cache[candidate]: return 'missing anchor'
        return None
    def root_target(path):
        error = target_error('README.md', path)
        require(not error, f'owner/metadata target {path}: {error}')
    for topic in authority['topics']:
        for p in topic['view_paths']: root_target(p)
        for owner in topic['owners']:
            root_target(owner['path'] + ('#' + owner['anchor'] if owner.get('anchor') else ''))
            if owner['path'].endswith('.md'):
                require(owner['path'] in coverage['reviewed_scope'], f'admitted Markdown owner lacks section coverage: {owner["path"]}')
    require(len({t['id'] for t in authority['topics']}) == 11, 'eleven unique canon topics required')
    require(authority['source_commit'] == baseline['baseline_commit'] == coverage['source_commit'], 'authority/coverage baseline mismatch')
    rowmap = {r['id']: r for r in coverage['rows']}; sectionmap = {s['id']: s for s in coverage['sections']}
    require(len(rowmap) == len(coverage['rows']), 'duplicate coverage row id')
    expected_sections = set(); total_fragments = 0; status_counts = collections.Counter()
    for p in coverage['reviewed_scope']:
        require(p in original, f'coverage source not in baseline: {p}')
        content = read(p); lines = content.splitlines(); byline = {i:(h,a) for h,a,i in headings(content)}
        starts = sorted({1, *byline})
        for index, start in enumerate(starts):
            end = starts[index+1]-1 if index+1 < len(starts) else len(lines)
            body = '\n'.join(lines[start if start in byline else start-1:end]).strip()
            if not body: continue
            sid = f'{p}:L{start}'; expected_sections.add(sid); sec = sectionmap.get(sid)
            require(sec is not None, f'uncovered section: {sid}')
            if not sec: continue
            require(sec['body_sha256'] == sha(body) and sec['end_line'] == end, f'section bytes/range: {sid}')
            parts = fragments(body); total_fragments += len(parts); represented = []
            for rid in sec['row_ids']:
                row = rowmap[rid]; coords = [tuple(c) for c in row['fragments']]; represented += coords
                require(row['section_id'] == sid, f'row section mismatch {rid}')
                require(all(c in parts for c in coords), f'unknown fragment in {rid}')
                if all(c in parts for c in coords): require(row['fragment_digest'] == sha('\n'.join(parts[c] for c in coords)), f'fragment digest {rid}')
                require(row['fragment_count'] == len(coords), f'fragment count {rid}')
                status_counts[row['status']] += len(coords)
                for dest in row['destinations']: root_target(dest)
                if row.get('superseding_source'): root_target(row['superseding_source'])
            require(set(represented) == set(parts) and len(represented) == len(set(represented)), f'incomplete/duplicated fragment partition {sid}')
            require(sec['expected_fragment_count'] == len(parts), f'section fragment count {sid}')
    require(set(sectionmap) == expected_sections, 'source section inventory mismatch')
    require(coverage['section_count'] == len(expected_sections) and coverage['claim_count'] == total_fragments, 'coverage summary mismatch')
    require(dict(status_counts) == coverage['fragment_status_counts'], 'status counts mismatch')
    require(coverage['unresolved_review_count'] == status_counts['UNRESOLVED_REVIEW'] == 0, 'unresolved source review')
    checks['coverage'] = {'sources': len(coverage['reviewed_scope']), 'sections': len(expected_sections), 'fragments': total_fragments, 'rows': len(rowmap), 'fragment_status_counts': dict(status_counts), 'semantic_limit': 'Partition/digests validate accounting, not factual truth. See SOURCE_STATUS_DECISIONS.md for the separate agent semantic review.'}
    arcs = load('story/ARC_MAP.json'); require(len(arcs['arcs']) == 7 and arcs['new_chapters_created'] == 0, 'arc/chapter count')
    for n, arc in enumerate(arcs['arcs'], 1):
        require(arc['id'] == f'ARC_{n:02}' and arc['macro_status'] == 'AUTHORIALLY_CLOSED' and arc['chapter_count'] is None and arc['chapter_state'] == 'NOT_CREATED', f'arc state {n}')
        root_target(arc['path']); root_target(f'story/ARC_{n:02}/chapters/README.md')
        for owner in arc['owners']: root_target(owner['path'])
        require(len(read(arc['path']).split()) > 300, f'insubstantial arc dossier {n}')
    require(not any('/chapters/' in p and not p.endswith('/README.md') for p in files if p.startswith('story/')), 'unexpected authored chapter')
    commands = load('tools/validation/commands.json')
    entries = commands.get('commands', commands.get('validators', []))
    require(len(entries) == 10, 'ten original validator routes required')
    for command in entries: root_target(command['script']); require(command['read_only'], 'write-mode validator route')
    pins = load('upstream/SOURCE_PINS.json')
    require(all(x is None for x in pins['verified_upstream_heads'].values()), 'unverified upstream HEAD asserted')
    for repo in pins['repositories']:
        if repo.get('record_owner'): root_target(repo['record_owner'])
        for item in repo.get('sources', []):
            if item.get('snapshot'): root_target(item['snapshot'])
    checks['ownership_and_arcs'] = {'topics': len(authority['topics']), 'arcs': len(arcs['arcs']), 'chapter_files': 0, 'existing_validator_routes': len(entries)}
    active = sorted((added | NAV) - {p for p in added if p.startswith((MAINT+'/package/', MAINT+'/baseline/'))})
    active = [p for p in active if p.endswith('.md')]
    historical = sorted(p for p in files if p.endswith('.md') and p not in active)
    link_report = {'active': {'files': len(active), 'links': 0, 'broken': []}, 'historical': {'files': len(historical), 'links': 0, 'broken': []}, 'external_urls': 'Not requested or checked over network; local path/anchor validation only.'}
    history_targets = set()
    for category, paths in (('active', active), ('historical', historical)):
        for p in paths:
            for line, raw, kind in markdown_links(read(p)):
                link_report[category]['links'] += 1
                error = target_error(p, raw)
                if error:
                    archive_class = 'existing baseline source' if p in original else ('byte-exact navigation backup with original relative base' if p.startswith(MAINT+'/baseline/') else 'preserved instruction package')
                    link_report[category]['broken'].append({'source': p, 'line': line, 'target': raw, 'kind': kind, 'error': error, 'archive_class': archive_class if category == 'historical' else None})
                if p == 'upstream/HISTORICAL_INDEX.md' and not urlsplit(raw).scheme:
                    resolved = ((root/p).parent/unquote(urlsplit(raw).path)).resolve()
                    if resolved.is_relative_to(root): history_targets.add(resolved.relative_to(root).as_posix())
    require(not link_report['active']['broken'], f"active broken links: {len(link_report['active']['broken'])}")
    link_report['historical']['broken_by_class'] = dict(collections.Counter(r['archive_class'] for r in link_report['historical']['broken']))
    require(original <= history_targets, f'baseline files missing from historical index: {sorted(original-history_targets)}')
    checks['historical_inventory'] = {'baseline_files': len(original), 'linked_baseline_files': len(original & history_targets)}
    return {'result': 'FAIL' if failures else 'PASS', 'source_commit': baseline['baseline_commit'], 'checks': checks, 'links': link_report, 'failures': list(dict.fromkeys(failures))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    report = audit(args.repository.resolve())
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(report['result'] != 'PASS')
