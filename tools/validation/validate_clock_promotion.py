"""Bounded R2/R3 exceptions to historical preservation checks.

The approved clock changes one field across 49 rows. Numeric/calendar values,
character overlays and old source evidence remain subject to their original
checks. Every exception also requires the complete author-promotion audit.
"""
import csv
import io
import json
import subprocess

from validate_promotions import audit_promotions

PREFIX = 'provenance/diplomatic-pouch-r2-r3/'
CLOCK = 'world-clock/WORLD_CLOCK_TEMPLATE.csv'
PROSE = {'live-model/PRISM.md', 'builder/COMMUNITY.md',
         'world-clock/ARC5_DIRECTOR_CALENDAR.md'}
OLD = 'Every day at 25:00 (voluntary; implicit baseline)'
NEW = 'Every day at 27:00 (voluntary; implicit baseline)'


def check_clock_bytes(before, after):
    """Accept only the authored timestamp substitution, not other cell edits."""
    if before.count(b'25:00') != 49 or after != before.replace(b'25:00', b'27:00'):
        raise ValueError('R2/R3 clock must change only 49 Highlights timestamps')
    rows = list(csv.DictReader(io.StringIO(after.decode('utf-8-sig'))))
    if len(rows) != 49 or any(r['nightly_highlights'] != NEW for r in rows):
        raise ValueError('R2/R3 clock requires 49 daily 27:00 Highlights entries')


def check_prose_bytes(path, before, after):
    if path not in PROSE:
        raise ValueError('Unapproved prose exception: ' + path)
    if path == 'world-clock/ARC5_DIRECTOR_CALENDAR.md':
        if before.count(b'25:00') != 1 or after != before.replace(b'25:00', b'27:00'):
            raise ValueError('Arc Five prose permits only the Highlights correction')
    elif not after.startswith(before):
        raise ValueError('R2/R3 prose must preserve the existing source prefix: ' + path)


def validated_replacements(root):
    manifest_path = root / (PREFIX + 'INTEGRATION.json')
    if not manifest_path.exists():
        return set()
    git = ['git', '-c', f'safe.directory={root.as_posix()}', '-C', str(root)]
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    def target(path):
        require((root / path.split('#', 1)[0]).exists(), 'Missing promotion target: ' + path)
    audited = audit_promotions(root, git, require, target)
    if errors:
        raise ValueError('; '.join(errors))
    if 'diplomatic-pouch-r2-r3' not in {r['id'] for r in audited['reports']}:
        raise ValueError('Unregistered R2/R3 promotion')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    required = PROSE | {CLOCK}
    if not required <= manifest['changed_paths'].keys():
        raise ValueError('Missing explicit R2/R3 replacement records')
    def old(path):
        return subprocess.check_output(git + ['show', manifest['baseline_commit'] + ':' + path])
    check_clock_bytes(old(CLOCK), (root / CLOCK).read_bytes())
    for path in PROSE:
        check_prose_bytes(path, old(path), (root / path).read_bytes())
    return set(PROSE)


def current_clock_baseline(root, historical_rows):
    """Apply only the validated later timestamp to a historical comparison copy."""
    if not validated_replacements(root):
        return historical_rows
    if len(historical_rows) != 49 or any(r['nightly_highlights'] != OLD for r in historical_rows):
        raise ValueError('Unexpected historical Highlights schedule')
    return [dict(row, nightly_highlights=NEW) for row in historical_rows]
