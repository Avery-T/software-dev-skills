# Software Development Skills plugin

This repository is the source package for the private **Software Development Skills** plugin. The root `plugin.json` is the portable Agent Plugins 1.0 manifest. It packages all 49 skill folders, their references and scripts, the shared model configuration, documentation, and MIT license. No MCP server, credential, external account connection, or new tool is bundled.

## Install and use

Open the private plugin link supplied after account creation and select **Install** if the host offers it. Then select **Software Development Skills** in a conversation or coding task. Ask for a skill by name, for example:

- "Use poteto-help to choose a workflow for my task."
- "Use poteto-mode to implement and verify this change."
- "Use model-configuration to inspect the configured models."

Slash commands and Cursor Custom Modes mentioned in upstream documentation are host-specific. Use the host's actual skill picker or name the skill in your prompt; do not assume a slash command, custom subagent type, or keyboard shortcut exists in ChatGPT or Codex. The plugin cannot change the model of an existing conversation. Bundled model choices remain preferences, not guarantees of model availability.

The 48 imported skill entrypoints retain `disable-model-invocation: true`. Each also has `agents/openai.yaml` with `policy.allow_implicit_invocation: false` for OpenAI hosts. This preserves explicit selection instead of silently making every skill automatic. The added `model-configuration` skill remains eligible for implicit selection. A selected workflow can read its bundled supporting skills as instructed, subject to the host's controls.

Some upstream guides describe optional skills and integrations outside this selected collection. Those are not installed by this plugin. Shell-based workflows need a file-capable execution environment, and integration-specific workflows need the corresponding tools and authorization already available in that task.

## Build and verify

With Python 3 and PyYAML available, run from the repository root:

```sh
python3 scripts/verify_pstack_import.py
python3 -m unittest discover -s tests -v
python3 scripts/build_plugin.py --output ../software-development-skills-0.1.0.zip
```

`requirements-packaging.txt` describes the Python packaging dependency. The builder validates JSON/YAML, skill identities, invocation policy, import hashes, regular files, required components, and safe archive paths. It writes a deterministic archive outside the source directory, preserves executable bits, and reads the resulting ZIP back to compare every file. Caches, dependencies, archives, credentials, and Git internals are excluded. The build does not run workflow scripts, install packages, or contact external services.

## Update the private copy

The private plugin is a saved release, not a live GitHub checkout. Pushing a change to this repository does **not** update the installed plugin automatically.

1. Change the source here. Update the semantic version in `plugin.json`.
2. Record changes to imported files and added skill files in `pstack-local-changes.json`, preserving original upstream hashes.
3. Run verification and tests, then rebuild the ZIP.
4. Update the existing private plugin through Plugin Creator using its exact plugin ID and current release ID. Do not create a second plugin. When removing files, explicitly delete the old paths as part of the update because an upload otherwise overlays the existing release.
5. Verify the saved release's manifest and all 49 expected skills before using it. Follow the host's refresh or new-task flow if needed.

The account's plugin and release IDs are deployment metadata, not secrets, but are intentionally kept out of this portable source package. The creator's existing private plugin is discoverable by its display name and its supplied account link. No public publication or workspace-wide sharing is required.
