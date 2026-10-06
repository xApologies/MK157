#!/usr/bin/env python3
"""Verify this instruction package against its non-self-referential manifest."""
import hashlib
import json
from pathlib import Path
import sys


def verify(root: Path) -> dict:
    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    errors = []; expected = set()
    for row in manifest['files']:
        relative = row['path']; p = Path(relative)
        if p.is_absolute() or '..' in p.parts or relative in expected:
            errors.append({'path': relative, 'issue': 'unsafe_or_duplicate_entry'}); continue
        expected.add(relative); target = root / p
        if not target.is_file() or target.is_symlink():
            errors.append({'path': relative, 'issue': 'missing_or_symlink'}); continue
        data = target.read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            errors.append({'path': relative, 'issue': 'hash_or_size_mismatch'})
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
              and not ('__pycache__' in p.parts and p.suffix == '.pyc')}
    extras = actual - expected - {'PACKAGE_MANIFEST.json'}
    if extras: errors.append({'issue': 'unexpected_files', 'paths': sorted(extras)})
    return {'result': 'FAIL' if errors else 'PASS', 'verified_files': len(expected), 'errors': errors,
            'scope': 'Package integrity only; not repository cleanup execution.'}


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    try:
        report = verify(root); print(json.dumps(report, indent=2))
        raise SystemExit(0 if report['result'] == 'PASS' else 1)
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({'result': 'ERROR', 'detail': str(exc)})); raise SystemExit(2)
