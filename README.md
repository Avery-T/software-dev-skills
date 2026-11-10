# Software development skills

Selected [pstack](https://github.com/backnotprop/pstack) skills for agent-assisted software development.

- 32 requested skills, plus 16 required companions.
- Complete upstream skill folders under [skills/](skills/), with guides and agent prompts.
- Pinned to [pstack 08547969e1df](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1), version 0.15.36.
- Original [MIT license](LICENSE) preserved. Imported upstream files are unchanged.

The [pinned upstream README](https://github.com/backnotprop/pstack/blob/08547969e1dffaa6457ea65141cc62c1d9a2eef1/README.md) describes the full pstack project.

See [PSTACK_IMPORT.md](PSTACK_IMPORT.md) for the exact name mapping, duplicate handling, companion reasons, optional upstream tools, and update instructions. [pstack-import.json](pstack-import.json) records every imported file's source hash.

## Use the collection

Copy the complete folders you need from `skills/` into your harness's skill directory. Keep companion skills alongside them. The [setup guide](docs/guide/01-setup.md) describes upstream harness support; its commands target upstream pstack, not this curated repository. Optional catalog entries are listed in the import notes rather than silently included.

## Check the import

Run `python3 scripts/verify_pstack_import.py`. This verifies file integrity and folder completeness. It does not test whether your harness supports every upstream tool or model.
