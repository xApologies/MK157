"""Regression fixtures for the link/coverage/schema boundaries used by R1."""
import unittest
import json
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch
from validate_authoring import fragments, headings, markdown_links, schema_check
from validate_promotions import audit_promotions, check_coverage, digest, historical_content, sections, safe_path, validated_city_replacements


class AuthoringFixtures(unittest.TestCase):
    def test_multifile_coverage_keeps_royal_table_before_first_subheading(self):
        text = '# Family\n\n| Name | Age |\n| Vaelor | ~300 |\n\n## Role\nWORKING.'
        rows = sections(text, include_preamble=True)
        self.assertEqual([r['section'] for r in rows], ['Document introduction', 'Role'])
        self.assertEqual(rows[0]['paragraphs'], [digest('| Name | Age |\n| Vaelor | ~300 |')])
        errors = []
        check_coverage(text, [], lambda ok, msg: errors.append(msg) if not ok else None, lambda _: None, include_preamble=True)
        self.assertIn('promotion section count', errors)
        self.assertEqual(len(sections('# Instructions\n\nRead owners.', True)), 1)

    def test_city_exception_never_exempts_numeric_data(self):
        with patch('validate_promotions.audit_promotions', return_value={'changed': {'visual-references/CITY_LOCATION_REGISTRY.csv', 'live-model/VALNAK_CITY_CULTURE_TRANSPORT.md', 'trial-rewards/TRIAL_WAVE_CREDITS.csv'}}):
            self.assertEqual(validated_city_replacements(Path.cwd()), {'visual-references/CITY_LOCATION_REGISTRY.csv', 'live-model/VALNAK_CITY_CULTURE_TRANSPORT.md'})
        def invalid(root, git, require, target):
            require(False, 'source tampered')
            return {'changed': {'visual-references/CITY_LOCATION_REGISTRY.csv'}}
        with patch('validate_promotions.audit_promotions', side_effect=invalid):
            with self.assertRaisesRegex(ValueError, 'source tampered'):
                validated_city_replacements(Path.cwd())

    def test_promotion_snapshot_rejects_undeclared_drift_and_tampering(self):
        with tempfile.TemporaryDirectory(prefix='mk157-promotion-test-') as directory:
            root = Path(directory)
            git = ['git', '-c', f'safe.directory={root.as_posix()}', '-C', str(root)]
            def run(*args): return subprocess.check_output(git+list(args), stderr=subprocess.PIPE)
            run('init', '-q')
            (root/'owner.md').write_bytes(b'Old owner.\n')
            (root/'untouched.md').write_bytes(b'Preserve.\n')
            run('add', '--', 'owner.md', 'untouched.md')
            run('-c', 'user.name=Validation Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')
            revision = run('rev-parse', 'HEAD').decode().strip()
            original = {}
            for record in run('ls-tree', '-rz', revision).split(b'\0'):
                if not record: continue
                meta, name = record.split(b'\t'); mode, kind, blob = meta.decode().split()
                p = name.decode(); original[p] = {'mode':mode, 'blob':blob, 'sha256':digest((root/p).read_bytes())}
            prefix = 'provenance/fixture/'
            (root/(prefix+'package')).mkdir(parents=True)
            (root/'canon').mkdir()
            def put(path, value): (root/path).write_text(json.dumps(value), encoding='utf-8')
            put(prefix+'BASELINE.json', {'commit':revision, 'files':original})
            (root/'owner.md').write_bytes(b'New owner.\n')
            source = prefix+'package/delta.md'; text = '## Fact\nNew owner.'
            (root/source).write_text(text, encoding='utf-8', newline='\n')
            rows = sections(text)
            rows[0]['paragraphs'] = [{'sha256':h,'status':'CURRENT','reason':'Explicit author update','destinations':['owner.md']} for h in rows[0]['paragraphs']]
            manifest = {'id':'fixture', 'baseline_commit':revision, 'changed_paths':{'owner.md':{'before_sha256':original['owner.md']['sha256'], 'after_sha256':digest((root/'owner.md').read_bytes())}}, 'source':source, 'package_sha256':{source:digest(text)}, 'coverage':rows, 'supersessions':[]}
            second = prefix+'package/family.md'; family = '# Family\n\nA supplied introduction.\n'
            (root/second).write_text(family, encoding='utf-8', newline='\n')
            family_rows = sections(family, True)
            family_rows[0]['paragraphs'] = [{'sha256':h, 'status':'WORKING', 'reason':'Supplied working model', 'destinations':['owner.md']} for h in family_rows[0]['paragraphs']]
            manifest['source_documents'] = [{'source':source, 'coverage':rows}, {'source':second, 'coverage':family_rows, 'include_preamble':True}]
            manifest['package_sha256'][second] = digest(family)
            csv_source = prefix+'package/places.csv'; csv_text = 'serial,name\n002,Gallery\n'
            (root/csv_source).write_text(csv_text, encoding='utf-8', newline='\n')
            (root/'places.csv').write_text(csv_text, encoding='utf-8', newline='\n')
            manifest['package_sha256'][csv_source] = digest(csv_text)
            manifest['tabular_sources'] = [{'source':csv_source, 'destination':'places.csv', 'key':'serial', 'row_digests':[digest(json.dumps({'serial':'002','name':'Gallery'}, sort_keys=True, ensure_ascii=False))]}]
            put(prefix+'INTEGRATION.json', manifest)
            put('canon/PROMOTIONS.json', {'promotions':[{'id':'fixture','manifest':prefix+'INTEGRATION.json'}]})
            def check():
                errors = []
                audit_promotions(root, git, lambda ok, message: errors.append(message) if not ok else None, lambda _: None)
                return errors
            self.assertEqual(check(), [])
            (root/'places.csv').write_text('serial,name\n002,Wrong\n', encoding='utf-8', newline='\n')
            self.assertIn('supplied registry rows differ from current owner', check())
            (root/'places.csv').write_text(csv_text, encoding='utf-8', newline='\n')
            (root/'untouched.md').write_bytes(b'Unexpected edit.\n')
            self.assertTrue(any('undeclared promotion drift' in e and 'untouched.md' in e for e in check()))
            (root/'untouched.md').write_bytes(b'Preserve.\n')
            (root/'owner.md').write_bytes(b'Unaccounted follow-up.\n')
            self.assertTrue(any('undeclared promotion drift' in e and 'owner.md' in e for e in check()))
            (root/source).write_text('## Fact\nTampered source.', encoding='utf-8')
            self.assertTrue(any('package bytes' in e for e in check()))

    def test_promotion_requires_every_paragraph_and_real_destination(self):
        text = '# Delta\n\n## One\nLocked fact.\n\nExact price OPEN.\n\n## Two\nSecond decision.'
        rows = sections(text)
        for row in rows:
            row['paragraphs'] = [{'sha256': h, 'status': 'CURRENT', 'reason': 'Explicit source', 'destinations': ['owner.md']} for h in row['paragraphs']]
        errors = []; targets = []
        require = lambda ok, message: errors.append(message) if not ok else None
        check_coverage(text, rows, require, targets.append)
        self.assertEqual(errors, [])
        self.assertEqual(targets, ['owner.md'] * 3)
        rows[0]['paragraphs'].pop()
        check_coverage(text, rows, require, targets.append)
        self.assertTrue(any('paragraph partition' in e for e in errors))

    def test_promotion_rejects_tampered_source_and_omitted_section(self):
        text = '## One\nClaim.'
        errors = []; require = lambda ok, message: errors.append(message) if not ok else None
        rows = [{'section': 'One', 'body_sha256': 'wrong', 'paragraphs': []}]
        check_coverage(text, rows, require, lambda _: None)
        self.assertTrue(any('digest' in e for e in errors))
        check_coverage(text, [], require, lambda _: None)
        self.assertIn('promotion section count', errors)

    def test_only_declared_promotion_uses_historical_coverage(self):
        calls = []
        def old(path): calls.append(path); return b'original'
        self.assertEqual(historical_content('a.md', 'changed', 'abc', set(), old), 'changed')
        self.assertEqual(calls, [])
        self.assertEqual(historical_content('a.md', 'changed', 'abc', {'a.md'}, old), 'original')
        self.assertEqual(calls, ['abc:a.md'])

    def test_promotion_paths_stay_in_repository(self):
        for p in ('/etc/file', '../file', 'C:/file', 'a/../../b', 'a\\b'):
            self.assertFalse(safe_path(p))
        self.assertTrue(safe_path('provenance/pouch/INTEGRATION.json'))

    def test_code_fences_comments_and_inline_code(self):
        text = '```md\n[x](missing.md)\n~~~\n[y](missing.md)\n```\n`[z](missing.md)`\n<!-- [c](bad) -->\n[ok](good.md)'
        self.assertEqual([(r[1],r[2]) for r in markdown_links(text)], [('good.md','inline')])

    def test_reference_forms_and_missing_definition(self):
        text = '[One][ref]\n[Ref][]\n[ref]\n[broken][absent]\n[ref]: <a%20b.md#one> "title"'
        targets = [r[1] for r in markdown_links(text)]
        self.assertEqual(targets.count('a%20b.md#one'), 4)
        self.assertIn('UNDEFINED_REFERENCE:absent', targets)

    def test_balanced_destination_and_nested_label(self):
        self.assertEqual([r[1] for r in markdown_links('![a [b]](one(two).png) [x](<a b.md#x> "Title")')], ['one(two).png','a b.md#x'])

    def test_duplicate_and_unicode_anchors(self):
        values = headings('# A *B* / C\n## A *B* / C\n# Café\n# `Literal`\nSetext\n======')
        self.assertEqual([r[1] for r in values], ['a-b--c','a-b--c-1','café','literal','setext'])

    def test_coverage_folds_wrapped_prose_but_keeps_items(self):
        value = fragments('First sentence wraps\nonto the next line. Next claim.\n\n- A; B\n- C')
        self.assertEqual(set(value), {(1,1),(1,2),(2,1),(2,2),(2,3)})

    def test_mixed_open_enumeration(self):
        self.assertEqual(len(fragments('Exact dates OPEN, local names, purchase days.')), 3)

    def test_schema_rejects_missing_invalid_and_unsupported(self):
        schema = {'type':'object','required':['status'],'properties':{'status':{'enum':['OPEN','CURRENT']}}}
        schema_check({'status':'OPEN'}, schema)
        for value in ({}, {'status':'invented'}):
            with self.assertRaises(ValueError): schema_check(value, schema)
        with self.assertRaises(ValueError): schema_check({}, {'additionalProperties':False})


if __name__ == '__main__': unittest.main()
