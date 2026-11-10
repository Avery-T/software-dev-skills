#!/usr/bin/env python3
"""Verify the pinned pstack files without network access or dependencies."""
import hashlib
import json
import re
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "pstack-import.json").read_text())
errors = []
expected = {}
for entry in manifest["files"]:
    path = entry["path"]
    expected[path] = entry
    file = ROOT / path
    if not file.is_file():
        errors.append(f"Missing file: {path}")
        continue
    data = file.read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if digest != entry["git_blob_sha"]:
        errors.append(f"Content differs from upstream: {path}")
    if len(data) != entry["bytes"]:
        errors.append(f"Size differs from upstream: {path}")
    expected_executable = entry["mode"] == "100755"
    if bool(file.stat().st_mode & stat.S_IXUSR) != expected_executable:
        errors.append(f"Executable mode differs from upstream: {path}")
skills = manifest["selected_skills"] + manifest["companion_skills"]
if len(skills) != len(set(skills)):
    errors.append("Duplicate skill names in selection and companions")
actual_skills = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
if actual_skills != sorted(skills):
    errors.append("Skill folder set differs from manifest")
for name in skills:
    root = ROOT / "skills" / name
    expected_files = {p for p in expected if p.startswith(f"skills/{name}/")}
    actual_files = {str(p.relative_to(ROOT)) for p in root.rglob("*") if p.is_file()}
    if actual_files != expected_files:
        errors.append(f"Skill folder contents differ from manifest: {name}")
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        continue
    text = skill_file.read_text()
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not frontmatter:
        errors.append(f"Missing frontmatter: {name}")
        continue
    if not re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", frontmatter.group(1)):
        errors.append(f"Frontmatter name differs from folder: {name}")
    if not re.search(r"(?m)^description:\s*\S", frontmatter.group(1)):
        errors.append(f"Missing description: {name}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"PASS: {len(expected)} upstream files match pinned hashes and modes; {len(skills)} complete, uniquely named skill folders.")
print(f"Source commit: {manifest['upstream']['commit']}")
