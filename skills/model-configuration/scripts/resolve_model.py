#!/usr/bin/env python3
"""Resolve pstack preferences against supplied runtime facts. Never spawn agents."""
import argparse
import json
from pathlib import Path

ALIASES = {"auto", "inherit-parent"}
DEFAULTS = Path(__file__).resolve().parents[1] / "references/pstack-models.md"


def read_settings(path):
    result = {}
    in_frontmatter = False
    for number, raw in enumerate(Path(path).read_text().splitlines(), 1):
        line = raw.strip()
        if line == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{number}: expected role: value")
        key, value = (part.strip() for part in line.split(":", 1))
        if not key or not value or key in result:
            raise ValueError(f"{path}:{number}: empty or duplicate setting")
        result[key] = value
    if in_frontmatter:
        raise ValueError(f"{path}: unclosed frontmatter")
    return result


def resolve(settings, role, runtime, cross_family=False):
    """runtime.models maps exact IDs to efforts and authoritative family metadata."""
    choices = settings.get(role, settings["subagents"]).split(",")
    effort = settings.get(f"{role} effort", settings["subagent effort"])
    models = runtime.get("models", {})
    current = runtime.get("current_model")
    current_info = models.get(current, {})
    output = []
    for choice in choices:
        requested = choice.strip()
        if not requested:
            raise ValueError("empty panel entry")
        args = {}
        notices = []
        selected = None
        if requested in ALIASES:
            notices.append("Configured inheritance alias; omit model override.")
        elif not runtime.get("can_select_model", False):
            notices.append("Model override unavailable for this call.")
        elif requested not in models or requested in runtime.get("rejected_models", []):
            notices.append(f"{requested} unavailable, unverified, or rejected.")
        else:
            args["model"] = requested
            selected = requested
        action = "spawn" if runtime.get("can_spawn", False) else "run-in-current-session"
        if selected is None:
            selected = current
            if not runtime.get("inherits_current_model", False):
                action = "run-in-current-session"
                notices.append("Inheritance is not confirmed; perform role in current session.")
            notices.append("Using " + (current or "current session model; exact identity not exposed") + ".")
        if action == "run-in-current-session":
            selected = current
            args = {}
            notices.append("Delegation unavailable; no separate worker will run.")
        info = models.get(selected, {})
        if effort not in ALIASES:
            if action != "spawn":
                notices.append("Cannot change effort of the current session.")
            elif runtime.get("can_select_effort", False) and effort in info.get("efforts", []) and not info.get("effort_encoded", False):
                args["reasoning_effort"] = effort
            else:
                notices.append(f"Effort {effort} not independently supported; omit override.")
        if cross_family:
            # Inheritance never qualifies, even if a catalog is inconsistent.
            family = info.get("family")
            parent_family = current_info.get("family")
            if "model" not in args or not family or not parent_family or family == parent_family:
                action = "skip-cross-family-judge"
                selected = None
                args = {}
                notices.append("No verified different-family model for this seat.")
        if role == "oversight":
            action = "main-session-preference-only"
            args = {}
            selected = current
            notices.append("This preference does not change the running main session.")
        output.append({"requested_model": requested, "effective_model": selected,
                       "action": action, "parameters": args, "notices": notices})
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, help="One selected project or user override file")
    parser.add_argument("--runtime", type=Path, required=True, help="Fresh normalized runtime facts as JSON")
    parser.add_argument("--role", required=True)
    parser.add_argument("--cross-family", action="store_true")
    args = parser.parse_args()
    settings = read_settings(DEFAULTS)
    if args.settings:
        settings.update(read_settings(args.settings))
    result = resolve(settings, args.role, json.loads(args.runtime.read_text()), args.cross_family)
    print(json.dumps({"defaults": str(DEFAULTS), "override": str(args.settings) if args.settings else None,
                      "role": args.role, "selections": result}, indent=2))


if __name__ == "__main__":
    main()
