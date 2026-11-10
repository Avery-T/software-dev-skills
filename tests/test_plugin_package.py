import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("plugin_builder", ROOT / "scripts/build_plugin.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__"))
        self.output = Path(self.temp.name) / "plugin.zip"

    def edit_manifest(self, edit):
        path = self.root / "plugin.json"
        data = json.loads(path.read_text())
        edit(data)
        path.write_text(json.dumps(data))

    def test_complete_archive_and_executable_modes(self):
        result = builder.build(self.root, self.output)
        self.assertEqual(result["skills"], 49)
        with zipfile.ZipFile(self.output) as archive:
            names = archive.namelist()
            self.assertEqual(sum(p.endswith("/SKILL.md") for p in names), 49)
            self.assertIn("software-development-skills/LICENSE", names)
            path = "software-development-skills/skills/show-me-your-work/scripts/log.sh"
            self.assertTrue((archive.getinfo(path).external_attr >> 16) & 0o100)

    def test_deterministic_build(self):
        first = builder.build(self.root, self.output)
        second = builder.build(self.root, self.output.with_name("second.zip"))
        self.assertEqual(first["sha256"], second["sha256"])

    def test_preserves_48_explicit_policies(self):
        files = list((self.root / "skills").glob("*/agents/openai.yaml"))
        self.assertEqual(len(files), 48)
        self.assertTrue(all("allow_implicit_invocation: false" in p.read_text() for p in files))

    def test_archive_cannot_be_inside_source(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            builder.build(self.root, self.root / "plugin.zip")

    def test_symlink_is_rejected(self):
        (self.root / "docs/link").symlink_to(self.root / "LICENSE")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            builder.build(self.root, self.output)

    def test_hidden_file_is_rejected(self):
        (self.root / "docs/.env").write_text("NOT_A_SECRET=fixture")
        with self.assertRaisesRegex(ValueError, "Hidden"):
            builder.build(self.root, self.output)

    def test_caches_and_dependencies_are_excluded(self):
        for directory in ("node_modules", "__pycache__"):
            path = self.root / "docs" / directory
            path.mkdir()
            (path / "ignored.txt").write_text("not shipped")
        builder.build(self.root, self.output)
        with zipfile.ZipFile(self.output) as archive:
            self.assertFalse(any("ignored.txt" in p for p in archive.namelist()))

    def test_oversize_subtitle_is_rejected(self):
        self.edit_manifest(lambda d: d["extensions"]["com.openai"]["interface"].update(shortDescription="x" * 31))
        with self.assertRaisesRegex(ValueError, "30 characters"):
            builder.validate(self.root)

    def test_legacy_component_declaration_is_rejected(self):
        self.edit_manifest(lambda d: d.update(skills="./skills"))
        with self.assertRaisesRegex(ValueError, "legacy"):
            builder.validate(self.root)

    def test_imported_skill_tampering_is_rejected(self):
        (self.root / "skills/arena/SKILL.md").write_text("broken")
        with self.assertRaisesRegex(ValueError, "Import integrity"):
            builder.validate(self.root)


if __name__ == "__main__":
    unittest.main()
