# pstack import

Imported from [backnotprop/pstack](https://github.com/backnotprop/pstack) at commit [08547969e1dffaa6457ea65141cc62c1d9a2eef1](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1). The upstream plugin version is 0.15.36. The source is a harness-adapted mirror of [Cursor's pstack](https://github.com/cursor/plugins/tree/main/pstack).

## Scope

The 34 requested entries resolve to 32 distinct skills. All matched. “design space” and “exhause the design space” select the same principle. “fix root cause” appears twice.

This import contains 48 complete skill folders: the 32 selected skills and 16 companions. The original import was byte-for-byte unchanged. This collection now has deliberate model-configuration edits recorded separately in `pstack-local-changes.json`; the source hashes in `pstack-import.json` remain unchanged. The MIT license, bundled TypeScript scripts, and lockfile remain intact. Supporting guide pages, images, and agent prompts are included.

## Name mapping

| # | Requested name | Upstream folder | Notes |
|---|---|---|---|
| 1 | blast radius | `blast-radius` |
| 2 | bro | `bro` |
| 3 | correct fixed mistake | `correct` |
| 4 | figure it out | `figure-it-out` |
| 5 | how does it work | `how` |
| 6 | in your own words | `in-your-own-words` |
| 7 | inteorgate | `interrogate` |
| 8 | patotohelp | `poteto-help` |
| 9 | design space | `principle-exhaust-the-design-space` |
| 10 | fix root cause | `principle-fix-root-causes` |
| 11 | foundation thinking | `principle-foundational-thinking` |
| 12 | encode lessons in strucutre | `principle-encode-lessons-in-structure` |
| 13 | exhause the design space | `principle-exhaust-the-design-space` | Duplicate of 9.
| 14 | fix root cause | `principle-fix-root-causes` | Duplicate of 10.
| 15 | laziness protocol | `principle-laziness-protocol` |
| 16 | migrate callers | `principle-migrate-callers-then-delete-legacy-apis` |
| 17 | minimize reader load | `principle-minimize-reader-load` |
| 18 | model the domain | `principle-model-the-domain` |
| 19 | never block on human | `principle-never-block-on-the-human` |
| 20 | outcome oriented execution | `principle-outcome-oriented-execution` |
| 21 | prove it works | `principle-prove-it-works` |
| 22 | resign thoruugh first princples | `principle-redesign-from-first-principles` |
| 23 | sperate before seializing shared sites | `principle-separate-before-serializing-shared-state` |
| 24 | sequence work in to verifiable units | `principle-sequence-verifiable-units` |
| 25 | subtract before you add | `principle-subtract-before-you-add` |
| 26 | test behavior not implementation | `principle-test-behavior-not-implementation` |
| 27 | type system dicisiple | `principle-type-system-discipline` |
| 28 | recall | `recall` |
| 29 | reflect for skills | `reflect` |
| 30 | sharpen for rewritting prompts | `sharpen` |
| 31 | show me your work | `show-me-your-work` |
| 32 | teach | `teach` |
| 33 | why | `why` |
| 34 | unlsop | `unslop` |

## Why the companions are included

- `interrogate` reuses `arena`. `figure-it-out` invokes `architect`, which also uses `arena`.
- `figure-it-out`, `how`, `why`, `recall`, `reflect`, `show-me-your-work`, and `arena` use `poteto-mode`'s shared instructions. Its full folder includes 23 playbooks and its scripts.
- Those mode workflows invoke `swarm`, `technical-writing`, `no-comments`, `benchmark-checklist`, `tdd`, and `ketchup`.
- The mode also requires seven principle leaves not in the selection: `principle-attack-the-premise`, `principle-boundary-discipline`, `principle-build-the-lever`, `principle-experience-first`, `principle-explain-the-number`, `principle-guard-the-context-window`, and `principle-make-operations-idempotent`.

## Optional upstream skills

The help catalog and guide also describe optional skills that are not included here. Their relative links can point outside this selected collection. They are not missing requested skills or mandatory workflow dependencies. Use their pinned source links when reading about them:

- [automate-me](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/automate-me)
- [create-formal-verification-skill](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/create-formal-verification-skill)
- [create-verification-skill](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/create-verification-skill)
- [ketchup-video](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/ketchup-video)
- [maintain-formal-verification-skill](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/maintain-formal-verification-skill)
- [maintain-verification-skill](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/maintain-verification-skill)
- [make-bot-ui](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/make-bot-ui)
- [setup-pstack](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/setup-pstack)
- [statechart](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/statechart)
- [typescript-best-practices](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1/skills/typescript-best-practices)

The added `model-configuration` skill owns model preferences in this collection and reads the same role settings format. Optional upstream `setup-pstack` is not bundled and does not preserve this collection's oversight or separate effort fields. `typescript-best-practices` is supplementary syntax guidance linked by the type-system principle. The remaining skills are optional help routes. External `cursor-team-kit` skills and harness-specific commands are not bundled; upstream documents fallbacks.

## Runtime boundaries

Importing these files does not run or install their scripts, register a plugin, change model settings, or grant permissions. Model names and tools still depend on the consuming harness. Host access restrictions, confirmation rules, and user instructions take precedence over upstream autonomy or transcript-path guidance.

## Verify or update

Run `python3 scripts/verify_pstack_import.py` from the repository. It checks unchanged source files against upstream hashes and deliberately modified files against their recorded local hashes, plus additions, modes, complete skill folders, and unique skill names. Run `python3 -m unittest discover -s tests -v` for resolver and verification behavior.

`pstack-import.json` records every source file's Git blob SHA and the source commit. To update, audit the next source commit and its dependency graph, copy the same selected folders plus any required companions, preserve the license, and update the upstream manifest only for the new source. Reapply and review the model-configuration changes, then regenerate their local hashes in `pstack-local-changes.json` and run the verifier and tests. Do not replace this selected collection with all upstream files without reviewing the scope.

## Local model-configuration changes

See [the README change map](README.md#where-the-pstack-skills-were-changed) for exact paths and behavior. `pstack-local-changes.json` records the original and current Git blob SHA, size, mode, and reason for each imported file changed locally. New skill files are listed separately. Upstream content policy in the original manifest describes the import baseline, not the current customized files.
