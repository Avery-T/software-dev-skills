import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('import_verifier', ROOT / 'scripts/verify_pstack_import.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class ImportVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__'))

    def errors(self):
        return verifier.verify(self.root)[0]

    def test_current_collection_passes(self):
        self.assertEqual(self.errors(), [])

    def test_unchanged_import_tampering_fails(self):
        (self.root / 'LICENSE').write_text('changed')
        self.assertTrue(any('LICENSE' in error for error in self.errors()))

    def test_modified_import_tampering_fails(self):
        with (self.root / 'skills/arena/SKILL.md').open('a') as output:
            output.write('unrecorded change')
        self.assertTrue(any('skills/arena/SKILL.md' in error for error in self.errors()))

    def test_added_skill_file_tampering_fails(self):
        (self.root / 'skills/model-configuration/SKILL.md').write_text('changed')
        self.assertTrue(any('model-configuration' in error for error in self.errors()))

    def test_wrong_upstream_provenance_fails(self):
        path = self.root / 'pstack-local-changes.json'
        data = json.loads(path.read_text())
        data['modified_files'][0]['upstream_git_blob_sha'] = '0' * 40
        path.write_text(json.dumps(data))
        self.assertTrue(any('provenance' in error for error in self.errors()))

    def test_unregistered_skill_file_fails(self):
        (self.root / 'skills/model-configuration/unregistered.txt').write_text('new')
        self.assertTrue(any('folder contents' in error for error in self.errors()))

    def test_executable_mode_tampering_fails(self):
        path = self.root / 'skills/model-configuration/SKILL.md'
        path.chmod(path.stat().st_mode | 0o100)
        self.assertTrue(any('Executable mode' in error for error in self.errors()))


if __name__ == '__main__':
    unittest.main()
