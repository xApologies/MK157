"""Tests use disposable fixtures, not the actual MK157 repository."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'cleanup_guard.py'
spec = importlib.util.spec_from_file_location('cleanup_guard', SCRIPT)
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'repo'; self.root.mkdir()
        self.run_git('init', '-q')
        self.run_git('config', 'user.name', 'Fixture')
        self.run_git('config', 'user.email', 'fixture@example.invalid')
        self.run_git('config', 'core.autocrlf', 'false')
        self.run_git('remote', 'add', 'origin', 'https://github.com/xApologies/MK157.git')
        self.write('README.md', b'old navigation\n')
        self.write('live-model/INDEX.md', b'old index\n')
        self.write('world-clock/data.json', b'{"n": 1, "open": null}\n')
        self.write('provenance/source.md', b'immutable history\n')
        self.run_git('add', '.')
        self.run_git('commit', '-qm', 'fixture baseline')
        self.before = g.snapshot(self.root)

    def tearDown(self): self.tmp.cleanup()

    def run_git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True).stdout

    def write(self, path, data):
        p = self.root / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)

    def test_identity_and_clean_snapshot(self):
        self.assertEqual(g.repository(self.root), self.root)
        self.assertEqual(self.before['tracked_file_count'], 4)
        self.assertEqual(g.check(self.root, self.before)['result'], 'PASS')

    def test_origin_rejection(self):
        self.run_git('remote', 'set-url', 'origin', 'https://github.com/xApologies/Mk-147.git')
        with self.assertRaises(ValueError): g.repository(self.root)
        self.assertFalse(g.origin_matches('https://evil.invalid/xApologies/MK157.git'))
        self.assertTrue(g.origin_matches('git@github.com:xApologies/MK157.git'))

    def test_dirty_snapshot_rejected(self):
        self.write('README.md', b'dirty\n')
        with self.assertRaises(ValueError): g.snapshot(self.root)

    def test_wrong_expected_head_rejected(self):
        with self.assertRaises(ValueError): g.snapshot(self.root, '0' * 40)

    def test_allowed_navigation_needs_backup(self):
        self.write('README.md', b'new nav\n')
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')
        self.write(g.ARCHIVE + 'README.md', b'old navigation\n')
        self.assertEqual(g.check(self.root, self.before)['result'], 'PASS')

    def test_wrong_backup_rejected(self):
        self.write('README.md', b'new nav\n')
        self.write(g.ARCHIVE + 'README.md', b'not original\n')
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    def test_protected_source_change_rejected(self):
        self.write('provenance/source.md', b'changed canon\n')
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    def test_deletion_rejected(self):
        (self.root / 'world-clock/data.json').unlink()
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    def test_staged_delete_even_if_working_file_restored(self):
        self.run_git('rm', '--cached', 'provenance/source.md')
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    def test_allowed_addition_and_unexpected_addition(self):
        self.write('canon/INDEX.md', b'new view\n')
        self.assertEqual(g.check(self.root, self.before)['result'], 'PASS')
        self.write('unrelated.txt', b'not authorized\n')
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    def test_preexisting_untracked_preserved(self):
        self.write('personal-notes.txt', b'user work\n')
        before = g.snapshot(self.root)
        self.assertEqual(g.check(self.root, before)['result'], 'PASS')
        self.write('personal-notes.txt', b'oops\n')
        self.assertEqual(g.check(self.root, before)['result'], 'FAIL')

    def test_staging_user_untracked_rejected(self):
        self.write('personal-notes.txt', b'user work\n')
        before = g.snapshot(self.root)
        self.run_git('add', 'personal-notes.txt')
        self.assertEqual(g.check(self.root, before)['result'], 'FAIL')

    @unittest.skipIf(os.name == 'nt', 'Physical executable bit is not portable on Windows')
    def test_mode_change_rejected(self):
        p = self.root / 'provenance/source.md'; p.chmod(p.stat().st_mode | 0o100)
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    @unittest.skipIf(os.name == 'nt', 'Symlink test requires native symlink support')
    def test_symlink_replacement_rejected(self):
        p = self.root / 'provenance/source.md'; p.unlink(); p.symlink_to('../README.md')
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    def test_guard_output_must_be_external_and_new(self):
        with self.assertRaises(ValueError): g.write_external(self.root, str(self.root / 'report.json'), {})
        out = Path(self.tmp.name) / 'report.json'; g.write_external(self.root, str(out), {})
        with self.assertRaises(FileExistsError): g.write_external(self.root, str(out), {})

    def test_invariants_and_strict_types(self):
        spec = {'repository':'xApologies/MK157','assertions':[
            {'path':'world-clock/data.json','pointer':'/n','equals':1},
            {'path':'world-clock/data.json','pointer':'/open','equals':None}]}
        self.assertEqual(g.invariants(self.root, spec)['result'], 'PASS')
        spec['assertions'][0]['equals'] = True
        self.assertEqual(g.invariants(self.root, spec)['result'], 'FAIL')
        self.assertEqual(g.json_pointer({'a/b': [{'~': 7}]}, '/a~1b/0/~0'), 7)

    def test_committed_candidate_preserved(self):
        self.write('canon/INDEX.md', b'new view\n')
        self.run_git('add', 'canon/INDEX.md'); self.run_git('commit', '-qm', 'candidate')
        self.assertEqual(g.check(self.root, self.before)['result'], 'PASS')

    def test_staged_protected_change_detected_even_if_working_restored(self):
        self.write('provenance/source.md', b'bad staged bytes\n')
        self.run_git('add', 'provenance/source.md')
        self.write('provenance/source.md', b'immutable history\n')
        self.assertEqual(g.check(self.root, self.before)['result'], 'FAIL')

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError): g.safe_path(self.root, '../escape')


if __name__ == '__main__': unittest.main()
