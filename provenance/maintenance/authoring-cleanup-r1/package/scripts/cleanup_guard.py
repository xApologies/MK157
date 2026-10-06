#!/usr/bin/env python3
"""Read-only MK157 maintenance guards. Writes reports only outside the repo.

No source rewriting, Git checkout/reset/clean, commit, network call or push occurs.
This verifies bytes/modes and selected assertions, not semantic completeness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any
from urllib.parse import urlparse

TARGET = 'xapologies/mk157'
NAVIGATION = {'README.md', 'live-model/INDEX.md'}
NEW_ROOT_FILES = {'AGENTS.md', 'CANON_STATUS.md'}
NEW_PREFIXES = ('canon/', 'story/', 'data/', 'tools/', 'upstream/',
                'provenance/maintenance/authoring-cleanup-r1/')
ARCHIVE = 'provenance/maintenance/authoring-cleanup-r1/baseline/'


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if result.returncode:
        raise RuntimeError(f'git {args[0]} failed: {result.stderr.decode(errors="replace").strip()}')
    return result.stdout


def origin_matches(url: str) -> bool:
    url = url.strip()
    if url.startswith('git@github.com:'):
        path = url.split(':', 1)[1]
    else:
        parsed = urlparse(url)
        if parsed.scheme not in ('https', 'ssh') or parsed.hostname != 'github.com':
            return False
        path = parsed.path.lstrip('/')
    path = path.rstrip('/')
    if path.lower().endswith('.git'):
        path = path[:-4]
    return path.lower() == TARGET


def repository(path: str | Path) -> Path:
    requested = Path(path).resolve()
    root = Path(os.fsdecode(git(requested, 'rev-parse', '--show-toplevel')).strip()).resolve()
    remote = git(root, 'remote', 'get-url', 'origin').decode().strip()
    if not origin_matches(remote):
        raise ValueError('Refusing non-MK157 origin; expected xApologies/MK157.')
    return root


def safe_path(root: Path, rel: str) -> Path:
    part = Path(rel)
    if part.is_absolute() or '..' in part.parts or not part.parts or part.parts[0] == '.git':
        raise ValueError(f'Unsafe repository-relative path: {rel!r}')
    here = root
    for name in part.parts[:-1]:
        here = here / name
        if here.is_symlink():
            raise ValueError(f'Symlink ancestor is not permitted: {rel}')
    return root / part


def file_info(root: Path, rel: str) -> dict[str, Any]:
    path = safe_path(root, rel)
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode):
        data = os.fsencode(os.readlink(path))
        return {'kind': 'symlink', 'sha256': hashlib.sha256(data).hexdigest(),
                'bytes': len(data), 'executable': None}
    if not stat.S_ISREG(st.st_mode):
        raise ValueError(f'Not a regular file or tracked symlink: {rel}')
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return {'kind': 'file', 'sha256': digest.hexdigest(), 'bytes': st.st_size,
            'executable': bool(st.st_mode & stat.S_IXUSR) if os.name != 'nt' else None}


def git_tree(root: Path) -> list[dict[str, str]]:
    entries = []
    for raw in git(root, 'ls-tree', '-r', '--full-tree', '-z', 'HEAD').split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        mode, kind, oid = meta.decode('ascii').split()
        if kind != 'blob':
            raise ValueError(f'Unsupported tracked object {kind}: {os.fsdecode(name)}; review separately.')
        entries.append({'path': os.fsdecode(name), 'mode': mode, 'git_blob_sha': oid})
    return entries


def hash_git_blobs(root: Path, ids: list[str]) -> dict[str, dict[str, Any]]:
    """Hash committed bytes in bounded chunks, without materializing the repository."""
    out: dict[str, dict[str, Any]] = {}
    proc = subprocess.Popen(['git', '-C', str(root), 'cat-file', '--batch'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None and proc.stdout is not None
    try:
        for oid in sorted(set(ids)):
            proc.stdin.write((oid + '\n').encode('ascii'))
            proc.stdin.flush()
            header = proc.stdout.readline().decode('ascii').strip().split()
            if len(header) != 3 or header[1] != 'blob':
                raise RuntimeError(f'Unexpected cat-file response for {oid}: {header}')
            size = int(header[2]); left = size; digest = hashlib.sha256()
            while left:
                chunk = proc.stdout.read(min(left, 1024 * 1024))
                if not chunk:
                    raise RuntimeError('Unexpected EOF reading Git blob')
                digest.update(chunk); left -= len(chunk)
            if proc.stdout.read(1) != b'\n':
                raise RuntimeError('Missing Git blob record terminator')
            out[oid] = {'git_sha256': digest.hexdigest(), 'git_bytes': size}
        proc.stdin.close()
        err = proc.stderr.read().decode(errors='replace') if proc.stderr else ''
        if proc.wait(timeout=30):
            raise RuntimeError('git cat-file failed: ' + err)
        return out
    finally:
        if proc.poll() is None:
            proc.kill(); proc.wait()
        for handle in (proc.stdin, proc.stdout, proc.stderr):
            if handle and not handle.closed:
                handle.close()


def untracked_paths(root: Path) -> list[str]:
    return [os.fsdecode(x) for x in git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if x]


def snapshot(root: Path, expected_head: str | None = None) -> dict[str, Any]:
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    if expected_head and expected_head != head:
        raise ValueError('HEAD differs from the explicitly chosen execution baseline; review drift.')
    if git(root, 'status', '--porcelain=v1', '--untracked-files=no').strip():
        raise ValueError('Tracked working tree/index is dirty; preserve existing work before snapshotting.')
    entries = git_tree(root)
    hashes = hash_git_blobs(root, [row['git_blob_sha'] for row in entries])
    files = {}
    groups: dict[str, list[str]] = {}
    for row in entries:
        rel = row['path']
        files[rel] = {**row, **hashes[row['git_blob_sha']], 'working': file_info(root, rel)}
        groups.setdefault(row['git_blob_sha'], []).append(rel)
    return {
        'schema_version': 1, 'repository': 'xApologies/MK157', 'baseline_commit': head,
        'tree_sha': git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
        'branch': git(root, 'rev-parse', '--abbrev-ref', 'HEAD').decode().strip(),
        'mode_scope': 'Git modes and physical executable bits' if os.name != 'nt' else 'Git modes; physical executable bits unavailable',
        'files': files, 'tracked_file_count': len(files),
        'committed_blob_bytes_by_path': sum(row['git_bytes'] for row in files.values()),
        'same_git_blob_groups': [ps for ps in groups.values() if len(ps) > 1],
        'same_blob_warning': 'Equal blobs are inventory evidence, not deletion permission.',
        'preexisting_untracked': {p: file_info(root, p) for p in untracked_paths(root)},
        'allowed_existing_edits': sorted(NAVIGATION),
        'new_prefixes': list(NEW_PREFIXES), 'new_root_files': sorted(NEW_ROOT_FILES)
    }


def index_entries(root: Path) -> dict[str, dict[str, str]]:
    out = {}
    for raw in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not raw:
            continue
        meta, path = raw.split(b'\t', 1)
        mode, oid, stage = meta.decode('ascii').split()
        if stage != '0':
            raise ValueError('Unmerged index entries require conflict review before maintenance.')
        out[os.fsdecode(path)] = {'mode': mode, 'git_blob_sha': oid}
    return out


def check(root: Path, baseline: dict[str, Any]) -> dict[str, Any]:
    if baseline.get('repository') != 'xApologies/MK157' or baseline.get('schema_version') != 1:
        raise ValueError('Invalid baseline schema/repository')
    ancestor = subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor',
                               baseline['baseline_commit'], 'HEAD'], capture_output=True)
    if ancestor.returncode:
        raise ValueError('Baseline is absent or is not an ancestor of HEAD; do not force a rollback.')
    failures: list[dict[str, Any]] = []
    edits = []; idx = index_entries(root)
    for rel, before in baseline['files'].items():
        try:
            now = file_info(root, rel)
        except (OSError, ValueError) as exc:
            failures.append({'path': rel, 'issue': 'missing_or_unsafe', 'detail': str(exc)}); continue
        if rel not in idx:
            failures.append({'path': rel, 'issue': 'tracked_entry_removed'})
        elif idx[rel]['mode'] != before['mode']:
            failures.append({'path': rel, 'issue': 'git_mode_changed'})
        if now['kind'] != before['working']['kind'] or now['executable'] != before['working']['executable']:
            failures.append({'path': rel, 'issue': 'working_kind_or_mode_changed'})
        working_changed = now['sha256'] != before['working']['sha256']
        index_changed = rel in idx and idx[rel]['git_blob_sha'] != before['git_blob_sha']
        if working_changed or index_changed:
            if rel not in NAVIGATION:
                failures.append({'path': rel, 'issue': 'protected_content_changed',
                                 'working_changed': working_changed, 'index_changed': index_changed})
            else:
                edits.append(rel)
        if rel in NAVIGATION and (working_changed or index_changed):
            backup = ARCHIVE + rel
            try:
                info = file_info(root, backup)
                if info['kind'] != 'file' or info['sha256'] != before['git_sha256']:
                    failures.append({'path': backup, 'issue': 'backup_not_exact_committed_bytes'})
            except (OSError, ValueError) as exc:
                failures.append({'path': backup, 'issue': 'missing_navigation_backup', 'detail': str(exc)})
    for rel, original in baseline['preexisting_untracked'].items():
        try:
            if file_info(root, rel) != original:
                failures.append({'path': rel, 'issue': 'preexisting_untracked_changed'})
        except (OSError, ValueError) as exc:
            failures.append({'path': rel, 'issue': 'preexisting_untracked_missing', 'detail': str(exc)})
        if rel in idx:
            failures.append({'path': rel, 'issue': 'preexisting_untracked_was_staged'})
    candidates = set(idx) | set(untracked_paths(root))
    additions = sorted(candidates - set(baseline['files']) - set(baseline['preexisting_untracked']))
    for rel in additions:
        if rel not in NEW_ROOT_FILES and not rel.startswith(NEW_PREFIXES):
            failures.append({'path': rel, 'issue': 'addition_outside_approved_surface'})
        try:
            if file_info(root, rel)['kind'] != 'file':
                failures.append({'path': rel, 'issue': 'new_symlink_not_authorized'})
        except (OSError, ValueError) as exc:
            failures.append({'path': rel, 'issue': 'unsafe_addition', 'detail': str(exc)})
    return {'schema_version': 1, 'result': 'FAIL' if failures else 'PASS',
            'scope': 'Existing byte/mode preservation and addition scope only; not semantic equivalence.',
            'baseline_commit': baseline['baseline_commit'],
            'candidate_head': git(root, 'rev-parse', 'HEAD').decode().strip(),
            'baseline_tracked_count': len(baseline['files']),
            'approved_navigation_edits': edits, 'additions': additions,
            'failures': failures, 'semantic_review_required': True}


def json_pointer(value: Any, pointer: str) -> Any:
    if pointer == '':
        return value
    if not pointer.startswith('/'):
        raise ValueError('JSON pointer must be empty or begin with /')
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            if not token.isdigit():
                raise ValueError('Array pointer token must be a nonnegative integer')
            value = value[int(token)]
        else:
            value = value[token]
    return value


def strict_equal(a: Any, b: Any) -> bool:
    """Avoid Python's True == 1 shortcut for categorical canon guards."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(strict_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def invariants(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    if spec.get('repository') != 'xApologies/MK157':
        raise ValueError('Wrong invariant repository')
    cache: dict[str, Any] = {}; failures = []
    for i, row in enumerate(spec['assertions']):
        try:
            rel = row['path']
            if rel not in cache:
                path = safe_path(root, rel)
                if path.is_symlink():
                    raise ValueError('Invariant data must not be a symlink')
                cache[rel] = json.loads(path.read_text(encoding='utf-8-sig'))
            actual = json_pointer(cache[rel], row['pointer'])
            if not strict_equal(actual, row['equals']):
                failures.append({'index': i, 'path': rel, 'pointer': row['pointer'],
                                 'expected': row['equals'], 'actual': actual})
        except (OSError, KeyError, IndexError, TypeError, ValueError) as exc:
            failures.append({'index': i, 'path': row.get('path'), 'error': str(exc)})
    return {'result': 'FAIL' if failures else 'PASS', 'assertions': len(spec['assertions']),
            'source_observed_commit': spec.get('observed_commit'), 'failures': failures,
            'scope': 'Selected supplied assertions only; review baseline drift and complete source semantics separately.'}


def write_external(root: Path, out: str, report: dict[str, Any]) -> None:
    destination = Path(out).resolve()
    if destination == root or root in destination.parents:
        raise ValueError('Guard report output must be outside the repository working tree.')
    if destination.exists():
        raise FileExistsError('Refusing to overwrite evidence; select a new report filename.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('snapshot', 'check', 'invariants'):
        p = sub.add_parser(name); p.add_argument('--repo', required=True); p.add_argument('--out', required=True)
        if name == 'snapshot': p.add_argument('--expected-head')
        elif name == 'check': p.add_argument('--baseline', required=True)
        else: p.add_argument('--spec', required=True)
    args = parser.parse_args()
    try:
        root = repository(args.repo)
        if args.command == 'snapshot': report = snapshot(root, args.expected_head)
        elif args.command == 'check': report = check(root, json.loads(Path(args.baseline).read_text(encoding='utf-8')))
        else: report = invariants(root, json.loads(Path(args.spec).read_text(encoding='utf-8')))
        write_external(root, args.out, report)
        print(json.dumps({'result': report.get('result', 'SNAPSHOT_CAPTURED'),
                          'report': str(Path(args.out).resolve()),
                          'failures': len(report.get('failures', []))}, indent=2))
        return 1 if report.get('result') == 'FAIL' else 0
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({'result': 'ERROR', 'detail': str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
