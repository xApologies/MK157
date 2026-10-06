"""Regression fixtures for the link/coverage/schema boundaries used by R1."""
import unittest
from validate_authoring import fragments, headings, markdown_links, schema_check


class AuthoringFixtures(unittest.TestCase):
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
