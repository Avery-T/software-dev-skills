#!/usr/bin/env python3
"""Validate and reproducibly package this skills-only plugin without network access."""
import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path

import yaml

from verify_pstack_import import verify

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = (
    "plugin.json", "AGENTS.md", "LICENSE", "README.md", "PLUGIN.md",
    "PSTACK_IMPORT.md", "pstack-import.json", "pstack-local-changes.json",
    "requirements-packaging.txt",
)
DIRECTORIES = ("skills", "agents", "docs", "scripts", "tests")
SKIP_PARTS = {"__pycache__", "node_modules", ".git", ".pytest_cache", "dist"}
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter is not an object: {path}")
    return data


def package_files(root):
    files = [root / name for name in ROOT_FILES]
    for directory in DIRECTORIES:
        parent = root / directory
        if parent.is_symlink():
            raise ValueError(f"Symlink not allowed: {directory}")
        for path in parent.rglob("*"):
            parts = path.relative_to(root).parts
            if SKIP_PARTS.intersection(parts):
                continue
            if path.is_symlink():
                raise ValueError(f"Symlink not allowed: {path}")
            if path.is_file():
                files.append(path)
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or non-regular package file: {path}")
        name = path.relative_to(root).as_posix()
        if any(part.startswith(".") for part in Path(name).parts):
            raise ValueError(f"Hidden package file needs review: {name}")
        if path.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".zip", ".pyc"}:
            raise ValueError(f"Disallowed package file: {name}")
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def validate(root):
    errors = verify(root)[0]
    if errors:
        raise ValueError("Import integrity failed:\n" + "\n".join(errors))
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("$schema") != SCHEMA:
        raise ValueError("Invalid plugin schema")
    name = manifest.get("name", "")
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?", name) or "--" in name or ".." in name:
        raise ValueError("Invalid plugin name")
    if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", manifest.get("version", "")):
        raise ValueError("Invalid plugin version")
    if any(key in manifest for key in ("skills", "mcpServers", "apps", "interface")):
        raise ValueError("Portable manifest contains legacy top-level components")
    interface = manifest["extensions"]["com.openai"]["interface"]
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            raise ValueError(f"Invalid interface.{key}")
    for key in ("displayName", "shortDescription"):
        if len(interface[key]) > 30:
            raise ValueError(f"interface.{key} exceeds 30 characters")
    if interface["category"] != "Developer Tools" or interface.get("capabilities") != []:
        raise ValueError("This is a skills-only Developer Tools plugin")
    prompts = interface["defaultPrompt"]
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise ValueError("Invalid default prompts")
    if any(not isinstance(p, str) or not p.strip() or len(p) > 128 or "\n" in p for p in prompts):
        raise ValueError("Invalid default prompt")
    files = package_files(root)
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if len(skills) != 49:
        raise ValueError(f"Expected 49 skills, found {len(skills)}")
    names = set()
    for path in skills:
        if path.stat().st_size > 1024 * 1024:
            raise ValueError(f"Skill too large: {path}")
        data = frontmatter(path)
        if data.get("name") != path.parent.name or data["name"] in names:
            raise ValueError(f"Duplicate or mismatched skill name: {path}")
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            raise ValueError(f"Missing skill description: {path}")
        names.add(data["name"])
        agent_path = path.parent / "agents/openai.yaml"
        agent = yaml.safe_load(agent_path.read_text()) if agent_path.exists() else {}
        if not isinstance(agent, dict):
            raise ValueError(f"Invalid agent metadata: {agent_path}")
        if data.get("disable-model-invocation") is True:
            if agent.get("policy", {}).get("allow_implicit_invocation") is not False:
                raise ValueError(f"Explicit invocation policy not preserved: {path}")
        policy = agent.get("policy", {})
        if set(policy) - {"products", "allow_implicit_invocation"}:
            raise ValueError(f"Unsupported agent policy: {agent_path}")
        implicit = policy.get("allow_implicit_invocation")
        if implicit is not None and not isinstance(implicit, bool):
            raise ValueError(f"Invocation policy is not boolean: {agent_path}")
    for path in files:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix in {".yaml", ".yml"}:
            yaml.safe_load(path.read_text(encoding="utf-8"))
    return manifest, files


def build(root, output):
    root, output = root.resolve(), output.resolve()
    if output == root or root in output.parents:
        raise ValueError("Write the archive outside the source directory")
    manifest, files = validate(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{manifest['name']}/{relative}", (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            mode = 0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(output) as archive:
        expected = {f"{manifest['name']}/{p.relative_to(root).as_posix()}": p for p in files}
        if archive.testzip() or set(archive.namelist()) != set(expected):
            raise ValueError("Archive inventory or CRC mismatch")
        for name, path in expected.items():
            if archive.read(name) != path.read_bytes():
                raise ValueError(f"Archive content mismatch: {name}")
            expected_exec = bool(path.stat().st_mode & stat.S_IXUSR)
            if bool((archive.getinfo(name).external_attr >> 16) & stat.S_IXUSR) != expected_exec:
                raise ValueError(f"Archive executable mode mismatch: {name}")
    return {"archive": str(output), "version": manifest["version"], "files": len(files),
            "skills": 49, "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "bytes": output.stat().st_size}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(build(ROOT, args.output), indent=2))
    except (ValueError, KeyError, OSError, yaml.YAMLError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
