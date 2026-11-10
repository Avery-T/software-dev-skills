---
name: model-configuration
description: Configure or resolve model and reasoning-effort choices for this collection. Read before selecting a model or spawning any subagent, including when a pstack workflow is invoked directly. Also use for changing model preferences or checking portability to another harness.
---

# Model configuration

This is the collection's shared model-selection policy. It extends pstack's existing role names and `pstack-models` settings format. All skills that choose or delegate to a model consult it. Skills that only provide advice run in the current session and do not change models.

These are instructions, not a model router or technical enforcement. System instructions, permissions, platform constraints, and the user's current task instructions take precedence. Never change a platform setting, install software, or request credentials merely to satisfy a model preference.

## Resolve settings

Read [the bundled defaults](references/pstack-models.md). Then select the first existing override file below for the active project and harness. Apply its named roles over the defaults. Do not combine competing user files.

1. `<project-root>/.agents/pstack-models.md`, the portable project override.
2. The existing pstack user file for this harness: `~/.cursor/rules/pstack-models.mdc` in Cursor, `~/.claude/rules/pstack-models.md` in Claude Code, or `~/.agents/pstack-models.md` elsewhere. Claude Code may use `~/.agents/pstack-models.md` when its own file is missing.
3. No file means bundled defaults, not the original upstream provider defaults.

Explicit task-specific model choices override the corresponding role for that task only. Report the effective settings source. Re-read after a configuration change and before each new batch of agents. Respect filesystem access restrictions; if an override cannot be read, say so and use the readable defaults.

The default oversight preference is `gpt-6-astra` with `high` reasoning. Every delegated role, including reviewers, synthesizers, and nested coordinators, prefers `gpt-6.1-sol`. Its effort is `inherit-parent`, because no separate worker effort was requested. Panel lists contain one entry per seat and may repeat a model. Unknown delegated roles use `subagents`; never borrow `oversight` for a worker simply because it reviews other work.

## Select only supported models

Before spawning, inspect this session's tool schema or authoritative runtime model catalog. Check the exact ID, supported effort values, and whether overrides are allowed for this call and its context/fork mode. A model shown in a main-chat picker is not evidence it can run as a subagent. These bundled IDs are preferences, not a promise that another account or harness exposes them.

- Pass a configured model only if this session confirms the exact ID is available and the tool allows the override.
- `auto` and `inherit-parent` mean omit the model override. They are pstack inheritance aliases, not a request to select a product's Auto mode.
- If a model is unavailable, unverified, forbidden for this call, or explicitly rejected before execution, omit the override and inherit the current calling session's model. Do not invent aliases, append effort/speed suffixes, guess a nearest model, or retry upstream Grok/Claude defaults.
- Say which role requested which model and why it is falling back. Name the actual inherited model only if the runtime identifies it. Otherwise say "current session model; exact identity not exposed".
- If a failed spawn might have created a worker, inspect its outcome before retrying. Never retry a known rejected ID in that session.
- Confirm from the tool's contract that omission inherits the current model. If it does not, or no subagent tool exists, run that role in the current session and disclose that delegation was unavailable. Do not claim a separate review or parallel run occurred.

For file-capable harnesses, `scripts/resolve_model.py` implements the exact-ID and effort checks for a supplied runtime catalog. It does not discover models or launch agents. Use fresh runtime facts, not a guessed catalog. Its output is a proposal; map it to the actual tool schema and check the returned execution metadata before claiming what ran. Harnesses without shell access follow the same rules directly.

The helper accepts `--role`, `--runtime <json-file>`, optional `--settings <selected-override>`, and `--cross-family` for judge candidates. The runtime JSON has `can_spawn`, `can_select_model`, `can_select_effort`, `inherits_current_model`, `current_model`, `rejected_models`, and `models`. `models` maps exact available IDs to `efforts`, an authoritative `family`, and optional `effort_encoded`. Missing capability flags default to false. Only set flags that hold for the specific call, including fork-mode restrictions. `parameters.reasoning_effort` is normalized output; translate the field name only if the live tool schema supports it.

## Keep effort separate

Read `<role> effort`, or `subagent effort` for a delegated role. Only `oversight` reads `oversight effort`. `inherit-parent` omits the effort override. Some harnesses inherit the parent's level and others use a model default; report only what the runtime confirms. If the tool supports a separate effort field, pass the configured level only when that model supports it. Otherwise omit it and disclose the limitation. Do not silently raise, lower, or turn on fast mode based on old pstack budget heuristics.

Existing pstack files containing full provider-specific IDs remain usable only when those exact IDs are available. An old `# budget` comment documents how upstream setup chose those IDs; it does not independently rewrite them here. If a model ID already encodes effort, do not also send a conflicting effort field. Use only a confirmed provider mapping or omit the separate effort field and explain.

## Main-session oversight is different

A skill cannot switch the model or reasoning effort of an already-running chat. At task start, compare the oversight preference with runtime information if exposed. When it differs or cannot be verified, report the effective configured oversight model and effort, with Astra/high only as the bundled default, and say the current session remains unchanged. Point the user to their harness's model/effort picker only if they want to change it. Do not block otherwise permitted work or claim this file changed the session. Use a supported new-session selector only when the user asked for that new session.

## Preserve honest review claims

Resolve every panel entry separately. Repeated Sol seats produce independent attempts, not multiple model families. Preserve the requested number of candidates and their isolated workspaces.

For Arena's cross-family judge, use only a configured pool member that is available and demonstrably from a different family than the current parent. Use authoritative family metadata, not a distinction invented from model suffixes. Astra and Sol are both GPT-family choices in this default configuration, so they do not provide the upstream Claude/Grok family contrast. Unknown family or a fallback to the parent also fails the family check. If no eligible member remains, skip that judge, disclose the missing cross-family review, and continue parent synthesis. Do not silently introduce another provider to manufacture diversity. A user-requested model race may override the pool for that task.

## Change or carry the configuration

When asked to change preferences, inspect available IDs and show unsupported choices as unavailable. Keep existing unrelated role choices. Write the requested override to the portable project file, or the existing pstack user file when the user explicitly wants user-wide settings. Do not modify a managed skill cache. Read the saved file back and report its path, effective roles, and any fallback. Saving preferences does not change the running session or prove a model executed.

Keep this entire skill folder beside every installed workflow that links to it. The bundled defaults travel with it; the project override travels with the project. Existing `/setup-pstack` settings can be read, but that optional upstream writer does not know this collection's added `oversight`, `subagents`, or separate effort fields. Use this skill to edit this collection's configuration so those fields are preserved.
