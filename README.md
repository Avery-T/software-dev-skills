# Software development skills

Selected [pstack](https://github.com/backnotprop/pstack) skills for agent-assisted software development, with one shared model-configuration policy.

- 32 requested skills, 16 upstream companions, and the added `model-configuration` skill.
- Pinned to [pstack 08547969e1df](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1), version 0.15.36.
- Original [MIT license](LICENSE) and source hashes preserved. Deliberate local changes are recorded separately.

See [PSTACK_IMPORT.md](PSTACK_IMPORT.md) for the original selection, required companions, and update procedure. [pstack-import.json](pstack-import.json) preserves upstream provenance. [pstack-local-changes.json](pstack-local-changes.json) identifies customized files and their current hashes.

## One configuration for the collection

The [model-configuration skill](skills/model-configuration/SKILL.md) governs model selection for all skills in this repository that choose models or launch subagents, including nested workflows. Skills that only give guidance run on the current session model and do not need to select another one.

The [bundled preferences](skills/model-configuration/references/pstack-models.md) are:

- Main-session oversight: **Astra, high reasoning** (`gpt-6-astra`, effort `high`).
- Every subagent role: **Sol 6.1** (`gpt-6.1-sol`). Worker effort is left to the harness unless configured separately. `inherit-parent` omits the effort override; actual inheritance depends on the harness.
- Unavailable, unverified, or disallowed model: inherit the current calling session's model and disclose the fallback. No guessed aliases or automatic provider substitutions.

Model and effort are separate settings. The skill checks the actual runtime's available subagent models, supported effort values, and call restrictions before selecting them. These model IDs are preferences, not a promise that every account or harness exposes them.

This configuration is an instruction-level policy, not technical enforcement. It does not override system instructions, platform capabilities, or permissions. It cannot switch an already-running main chat to Astra or change that chat's effort. Select the main model and effort in your harness when supported. The skill reports mismatches rather than claiming a switch occurred.

The default review panels use multiple Sol attempts. They are not cross-family reviews. Arena skips a cross-family judge when no configured eligible model exists and says so. The decision-trail review labels same-family or self-review honestly. Orchestrate keeps a required cross-family shipping gate unmet rather than treating fallback as approval.

## Portable setup

Copy the complete folders you need from `skills/` into your harness's skill directory. Keep required companions alongside them and always include the complete `model-configuration` folder with delegated workflows. Typical locations are `.agents/skills/` for Codex and compatible harnesses, `.claude/skills/` for Claude Code, or `.cursor/skills/` for Cursor. Use the path your harness actually supports.

No personal absolute paths or credentials are bundled. Defaults travel inside the configuration skill. To customize a project, copy `skills/model-configuration/references/pstack-models.md` to that project's `.agents/pstack-models.md` and edit the requested roles. To change all delegated roles, update all their model lines; `subagents` is the fallback for roles without a named entry. Keep the main `oversight` setting separate.

Resolution order is explicit task choices, then the portable project file, then the harness's existing pstack user file, then bundled defaults. Only the first existing override file is used, with absent roles filled from bundled defaults. Existing user paths are `~/.cursor/rules/pstack-models.mdc`, `~/.claude/rules/pstack-models.md`, and `~/.agents/pstack-models.md` in other harnesses. Claude Code also accepts the last path as a legacy fallback. The settings reuse pstack's role labels and list syntax, so there is no competing role system.

Ask `model-configuration` to inspect or change settings. Optional upstream `/setup-pstack` is not bundled; its writer does not know this collection's added oversight and separate effort fields. Installation and usage do not require running it. The [setup guide](docs/guide/01-setup.md) and [Claude Code adapter](docs/harness/claude-code.md) describe the local behavior.

## Where the pstack skills were changed

These imported skill entrypoints now link to the shared policy before delegation. Their model selectors use its role resolution instead of hard-coded provider defaults:

- [skills/architect/SKILL.md](skills/architect/SKILL.md)
- [skills/arena/SKILL.md](skills/arena/SKILL.md)
- [skills/blast-radius/SKILL.md](skills/blast-radius/SKILL.md)
- [skills/figure-it-out/SKILL.md](skills/figure-it-out/SKILL.md)
- [skills/how/SKILL.md](skills/how/SKILL.md)
- [skills/interrogate/SKILL.md](skills/interrogate/SKILL.md)
- [skills/no-comments/SKILL.md](skills/no-comments/SKILL.md)
- [skills/poteto-help/SKILL.md](skills/poteto-help/SKILL.md)
- [skills/poteto-mode/SKILL.md](skills/poteto-mode/SKILL.md)
- [skills/principle-build-the-lever/SKILL.md](skills/principle-build-the-lever/SKILL.md)
- [skills/principle-guard-the-context-window/SKILL.md](skills/principle-guard-the-context-window/SKILL.md)
- [skills/recall/SKILL.md](skills/recall/SKILL.md)
- [skills/reflect/SKILL.md](skills/reflect/SKILL.md)
- [skills/show-me-your-work/SKILL.md](skills/show-me-your-work/SKILL.md)
- [skills/swarm/SKILL.md](skills/swarm/SKILL.md)
- [skills/why/SKILL.md](skills/why/SKILL.md)

`poteto-mode` no longer rewrites model suffixes, effort, or speed automatically. `how`, `why`, `reflect`, `swarm`, `arena`, and `architect` resolve their named roles centrally. `interrogate` keeps its reviewer-role override when reusing Arena. `recall` no longer chooses an unspecified "fast, cheap" model. `blast-radius`, the architect runner prompt, and review workflows no longer assume every worker comes from a different model family.

Every bundled playbook has a direct configuration link, so reading one without `poteto-mode` still loads the policy. The feature, bug-fix, perf-issue, hillclimb, refactoring, and multi-phase playbooks also lost their hard-coded provider defaults. Exact playbook paths:

- [skills/poteto-mode/playbooks/authoring-a-skill.md](skills/poteto-mode/playbooks/authoring-a-skill.md)
- [skills/poteto-mode/playbooks/autonomous-run.md](skills/poteto-mode/playbooks/autonomous-run.md)
- [skills/poteto-mode/playbooks/autopilot-full.md](skills/poteto-mode/playbooks/autopilot-full.md)
- [skills/poteto-mode/playbooks/autopilot-stack.md](skills/poteto-mode/playbooks/autopilot-stack.md)
- [skills/poteto-mode/playbooks/babysit.md](skills/poteto-mode/playbooks/babysit.md)
- [skills/poteto-mode/playbooks/bug-fix.md](skills/poteto-mode/playbooks/bug-fix.md)
- [skills/poteto-mode/playbooks/eval.md](skills/poteto-mode/playbooks/eval.md)
- [skills/poteto-mode/playbooks/feature.md](skills/poteto-mode/playbooks/feature.md)
- [skills/poteto-mode/playbooks/hillclimb.md](skills/poteto-mode/playbooks/hillclimb.md)
- [skills/poteto-mode/playbooks/investigation.md](skills/poteto-mode/playbooks/investigation.md)
- [skills/poteto-mode/playbooks/multi-phase-plan.md](skills/poteto-mode/playbooks/multi-phase-plan.md)
- [skills/poteto-mode/playbooks/opening-a-pr.md](skills/poteto-mode/playbooks/opening-a-pr.md)
- [skills/poteto-mode/playbooks/orchestrate.md](skills/poteto-mode/playbooks/orchestrate.md)
- [skills/poteto-mode/playbooks/pause-safely.md](skills/poteto-mode/playbooks/pause-safely.md)
- [skills/poteto-mode/playbooks/perf-issue.md](skills/poteto-mode/playbooks/perf-issue.md)
- [skills/poteto-mode/playbooks/prototype.md](skills/poteto-mode/playbooks/prototype.md)
- [skills/poteto-mode/playbooks/refactoring.md](skills/poteto-mode/playbooks/refactoring.md)
- [skills/poteto-mode/playbooks/runtime-forensics.md](skills/poteto-mode/playbooks/runtime-forensics.md)
- [skills/poteto-mode/playbooks/session-pickup.md](skills/poteto-mode/playbooks/session-pickup.md)
- [skills/poteto-mode/playbooks/shipping.md](skills/poteto-mode/playbooks/shipping.md)
- [skills/poteto-mode/playbooks/trace-forensics.md](skills/poteto-mode/playbooks/trace-forensics.md)
- [skills/poteto-mode/playbooks/visual-parity.md](skills/poteto-mode/playbooks/visual-parity.md)
- [skills/poteto-mode/playbooks/worktree-cleanup.md](skills/poteto-mode/playbooks/worktree-cleanup.md)

Other imported files changed for nested delegation, setup guidance, and honest review claims:

- [agents/comment-sicko.md](agents/comment-sicko.md)
- [agents/poteto-agent.md](agents/poteto-agent.md)
- [docs/guide/01-setup.md](docs/guide/01-setup.md)
- [docs/guide/04-design.md](docs/guide/04-design.md)
- [docs/guide/07-overnight.md](docs/guide/07-overnight.md)
- [docs/harness/claude-code.md](docs/harness/claude-code.md)
- [skills/architect/references/runner-prompt.md](skills/architect/references/runner-prompt.md)

The new [AGENTS.md](AGENTS.md) applies the same policy to future repository work. The new configuration skill, its bundled settings, and its optional [resolver helper](skills/model-configuration/scripts/resolve_model.py) are local additions, not upstream pstack files.

## Verification

Run from the repository root:

```sh
python3 scripts/verify_pstack_import.py
python3 -m unittest discover -s tests -v
```

The verifier checks unchanged upstream hashes, explicitly recorded local modifications, additions, executable modes, and complete skill folders. Tests exercise exact model selection, unavailable-model fallback, effort handling, call restrictions, panels, family checks, and import-integrity failures. The helper consumes supplied runtime facts; it does not discover models, spawn workers, or prove a real harness executed a selection.

## Private ChatGPT/Codex plugin

This repository is also the source package for **Software Development Skills**. [PLUGIN.md](PLUGIN.md) explains installation, supported host behavior, the reproducible ZIP build, and updates to the saved private release. The package includes all 49 skills and their supporting files. Repository edits do not automatically update an installed plugin.
