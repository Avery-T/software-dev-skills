# Repository instructions

Before choosing a model or spawning a subagent for work using this collection, read `skills/model-configuration/SKILL.md`. Use it for every delegated role, including nested work and skills added later. Advice-only skills run in the current session. This policy cannot override system instructions, user authorization, or platform capabilities.

Preserve upstream provenance in `pstack-import.json`. Record deliberate edits to imported files in `pstack-local-changes.json`, with original and current hashes and a reason. Register added skill files there too. After changes, run `python3 scripts/verify_pstack_import.py` and `python3 -m unittest discover -s tests -v`.
