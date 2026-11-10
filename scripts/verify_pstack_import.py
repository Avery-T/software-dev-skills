#!/usr/bin/env python3
"""Verify pinned imports plus explicitly recorded local changes, offline."""
import hashlib
import json
import re
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify(root):
    manifest = json.loads((root / "pstack-import.json").read_text())
    local = json.loads((root / "pstack-local-changes.json").read_text())
    errors = []
    upstream = {entry["path"]: entry for entry in manifest["files"]}
    modified = {entry["path"]: entry for entry in local["modified_files"]}
    added = {entry["path"]: entry for entry in local["added_files"]}
    for label, entries, mapped in [("upstream", manifest["files"], upstream),
                                  ("modified", local["modified_files"], modified),
                                  ("added", local["added_files"], added)]:
        if len(entries) != len(mapped):
            errors.append(f"Duplicate {label} file paths")
    expected = dict(upstream)
    for path, entry in modified.items():
        original = upstream.get(path)
        if not original or entry["upstream_git_blob_sha"] != original["git_blob_sha"]:
            errors.append(f"Local change has no matching upstream provenance: {path}")
        elif entry["git_blob_sha"] == original["git_blob_sha"]:
            errors.append(f"Unchanged file recorded as modified: {path}")
        if not entry.get("reason", "").strip():
            errors.append(f"Missing local change reason: {path}")
        expected[path] = entry
    for path, entry in added.items():
        if path in upstream:
            errors.append(f"Added file is already upstream: {path}")
        expected[path] = entry
    for path, entry in expected.items():
        file = root / path
        if Path(path).is_absolute() or ".." in Path(path).parts:
            errors.append(f"Unsafe manifest path: {path}")
            continue
        if not file.is_file() or file.is_symlink():
            errors.append(f"Missing or non-regular file: {path}")
            continue
        data = file.read_bytes()
        if blob_sha(data) != entry["git_blob_sha"]:
            errors.append(f"Content differs from recorded hash: {path}")
        if len(data) != entry["bytes"]:
            errors.append(f"Size differs from recorded value: {path}")
        if bool(file.stat().st_mode & stat.S_IXUSR) != (entry["mode"] == "100755"):
            errors.append(f"Executable mode differs from recorded value: {path}")
    skills = manifest["selected_skills"] + manifest["companion_skills"] + local["added_skills"]
    if len(skills) != len(set(skills)):
        errors.append("Duplicate skill names")
    actual_skills = sorted(path.name for path in (root / "skills").iterdir() if path.is_dir())
    if actual_skills != sorted(skills):
        errors.append("Skill folder set differs from manifests")
    for name in skills:
        skill_root = root / "skills" / name
        expected_files = {p for p in expected if p.startswith(f"skills/{name}/")}
        actual_files = {str(p.relative_to(root)) for p in skill_root.rglob("*") if p.is_file()
                        and "__pycache__" not in p.parts}
        if actual_files != expected_files:
            errors.append(f"Skill folder contents differ from manifests: {name}")
        file = skill_root / "SKILL.md"
        if not file.is_file():
            continue
        frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", file.read_text(), re.S)
        if not frontmatter:
            errors.append(f"Missing frontmatter: {name}")
        elif not re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", frontmatter.group(1)):
            errors.append(f"Frontmatter name differs from folder: {name}")
        elif not re.search(r"(?m)^description:\s*\S", frontmatter.group(1)):
            errors.append(f"Missing description: {name}")
    return errors, len(upstream), len(modified), len(added), len(skills), manifest["upstream"]["commit"]


def main():
    errors, upstream, modified, added, skills, commit = verify(ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {upstream - modified} unchanged upstream files, {modified} recorded local modifications, {added} additions; {skills} complete skill folders.")
    print(f"Source commit: {commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
