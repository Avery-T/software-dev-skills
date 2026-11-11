# Software development skills

Selected [pstack](https://github.com/backnotprop/pstack) skills for agent-assisted software development, with one shared model-configuration policy.

- 32 requested skills, 16 upstream companions, and the added `model-configuration` skill.
- Pinned to [pstack 08547969e1df](https://github.com/backnotprop/pstack/tree/08547969e1dffaa6457ea65141cc62c1d9a2eef1), version 0.15.36.
- Original [MIT license](LICENSE) and source hashes preserved. Deliberate local changes are recorded separately.

See [PSTACK_IMPORT.md](PSTACK_IMPORT.md) for the original selection, required companions, and update procedure. [pstack-import.json](pstack-import.json) preserves upstream provenance. [pstack-local-changes.json](pstack-local-changes.json) identifies customized files and their current hashes.

## Skills engineers invoke explicitly

For direct use, explicitly select the skill you want below. All **48 imported skills** have `disable-model-invocation: true` in their `SKILL.md` frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. These are invocation settings, including for the principle skills whose descriptions say "Apply when..."; those descriptions alone do not make them automatic.

Use your host's skill picker or name the skill in your prompt, for example, "Use architect to design this change" or "Use blast-radius to review this diff." Use `/skill-name` only where the host supports that syntax. See [plugin usage and host compatibility](PLUGIN.md#install-and-use).

You do **not** need to invoke all 48 individually for each task. Start with **poteto-mode** for a complete workflow, or **poteto-help** to choose one; a selected workflow can read its supporting skills as instructed, subject to the host's controls. The separate [model-configuration](skills/model-configuration/SKILL.md) skill is eligible for implicit selection and is read by workflows before model selection or delegation, so it is not in this explicit-only list. You can still request it directly to inspect or change model preferences.

### Plan and coordinate work

- [**poteto-help**](skills/poteto-help/SKILL.md): Explains setup and recommends the right skill, playbook, or principle for your task, with a prompt you can use to start it.
- [**poteto-mode**](skills/poteto-mode/SKILL.md): Routes a task to a playbook and coordinates planning, implementation, verification, and reporting using the relevant supporting skills.
- [**in-your-own-words**](skills/in-your-own-words/SKILL.md): Restates your goals and the problem the agent thinks you are trying to solve, so you can check its understanding before work proceeds.
- [**sharpen**](skills/sharpen/SKILL.md): Rewrites a task prompt for greater depth by identifying stronger methods, raw evidence, and independent checks without expanding its scope.
- [**architect**](skills/architect/SKILL.md): Sketches types, signatures, and module boundaries before implementation, then stays involved as the design becomes working code.
- [**figure-it-out**](skills/figure-it-out/SKILL.md): Builds an auditable, task-specific playbook for a large migration or complex change when a narrower workflow does not fit.
- [**arena**](skills/arena/SKILL.md): Produces several independent candidates for the same task, selects a base, and combines the strongest parts into one result.
- [**swarm**](skills/swarm/SKILL.md): Coordinates parallel workers for coverage, exploration, races, or adversarial checks and combines their findings into one report.
- [**show-me-your-work**](skills/show-me-your-work/SKILL.md): Keeps a reviewable decision log for long-running or unattended work, recording what changed, why, the evidence, and the result.

### Understand code and catch up

- [**how**](skills/how/SKILL.md): Explains current architecture and runtime behavior, including where code belongs and which module should own it.
- [**why**](skills/why/SKILL.md): Investigates the evidence behind design decisions, regressions, and thresholds, then explains the rationale and tradeoffs with citations.
- [**teach**](skills/teach/SKILL.md): Combines the relevant findings from how and why into a plain-language explanation of a change or subsystem at the reader's pace.
- [**recall**](skills/recall/SKILL.md): Reconstructs recent work from available conversation history, live state, and shared records to explain where you left off and what is current.
- [**ketchup**](skills/ketchup/SKILL.md): Summarizes what changed in the current chat since your last message and lists decisions or actions waiting on you with enough context to respond.
- [**bro**](skills/bro/SKILL.md): Restates the last message in plain language without jargon.

### Review, test, and improve

- [**interrogate**](skills/interrogate/SKILL.md): Uses adversarial reviewers to try to break a change or design and retains findings supported by executable evidence.
- [**blast-radius**](skills/blast-radius/SKILL.md): Looks beyond the diff for behavior a change could break and runs real checks of the assumptions that make it safe.
- [**benchmark-checklist**](skills/benchmark-checklist/SKILL.md): Checks whether a performance measurement is meaningful, repeatable, and measuring the intended work before you report or act on it.
- [**tdd**](skills/tdd/SKILL.md): Turns a bug into a focused failing test before the fix and verifies that it passes afterward, using a practical alternative when a new test would be costly or brittle.
- [**no-comments**](skills/no-comments/SKILL.md): Reviews comments and suppressions, removes accepted noise or workarounds within scope, and proposes enforceable checks for important constraints.
- [**correct**](skills/correct/SKILL.md): Converts recurring agent mistakes into structural safeguards, preferring architecture, types, lint rules, or tests over another written reminder.
- [**reflect**](skills/reflect/SKILL.md): Reviews the current session for durable lessons and proposes targeted skill improvements, waiting for approval before applying accepted skill edits.

### Write clearly

- [**technical-writing**](skills/technical-writing/SKILL.md): Applies a structured technical-writing standard to documentation, RFCs, READMEs, PR descriptions, and commit messages.
- [**unslop**](skills/unslop/SKILL.md): Removes formulaic AI phrasing, filler, and other writing habits that obscure the message.

### Apply a specific engineering principle

These 24 focused skills have the same explicit-selection settings as the workflows above. Select one directly when you want to emphasize it; a selected workflow may already read the relevant principles.

- [**principle-attack-the-premise**](skills/principle-attack-the-premise/SKILL.md): When repeated fixes fail the same check, identifies and tests their shared assumption before attempting another fix built on it.
- [**principle-boundary-discipline**](skills/principle-boundary-discipline/SKILL.md): Concentrates validation and error handling at external boundaries while keeping internal business logic simple and grounded in trusted types.
- [**principle-build-the-lever**](skills/principle-build-the-lever/SKILL.md): Builds a reusable script, codemod, generator, or workflow that performs or proves nontrivial work instead of relying on manual repetition.
- [**principle-encode-lessons-in-structure**](skills/principle-encode-lessons-in-structure/SKILL.md): Turns repeated instructions and corrections into enforceable lint rules, metadata, runtime checks, or scripts.
- [**principle-exhaust-the-design-space**](skills/principle-exhaust-the-design-space/SKILL.md): Compares two or three competing prototypes before committing to a novel interface or architectural decision.
- [**principle-experience-first**](skills/principle-experience-first/SKILL.md): Resolves product and UX tradeoffs around the user's experience, favoring fewer polished features over broader but rougher scope.
- [**principle-explain-the-number**](skills/principle-explain-the-number/SKILL.md): Identifies what limits a measured result and checks that it represents the intended work before trusting a speedup, regression, latency, or evaluation score.
- [**principle-fix-root-causes**](skills/principle-fix-root-causes/SKILL.md): Traces a symptom to the first point where the system went wrong and fixes that cause rather than hiding it behind extra guards.
- [**principle-foundational-thinking**](skills/principle-foundational-thinking/SKILL.md): Settles core data structures, shared state, and implementation order before adding logic so the rest of the design follows clearly.
- [**principle-guard-the-context-window**](skills/principle-guard-the-context-window/SKILL.md): Keeps the main conversation focused by delegating bulk inspection and retaining concise findings instead of large raw outputs.
- [**principle-laziness-protocol**](skills/principle-laziness-protocol/SKILL.md): Favors deletion and the smallest effective change over extra abstractions, layers, and plumbing.
- [**principle-make-operations-idempotent**](skills/principle-make-operations-idempotent/SKILL.md): Designs commands and processing steps to converge on the same end state after retries, restarts, or partially completed runs.
- [**principle-migrate-callers-then-delete-legacy-apis**](skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md): Moves callers to a new internal API and removes the old API in the same migration instead of leaving compatibility layers behind.
- [**principle-minimize-reader-load**](skills/principle-minimize-reader-load/SKILL.md): Reduces indirection and hidden state so another engineer can trace code with fewer layers and less mental bookkeeping.
- [**principle-model-the-domain**](skills/principle-model-the-domain/SKILL.md): Encodes domain rules in suitable types and data structures, such as state machines or registries, instead of scattering them across conditionals.
- [**principle-never-block-on-the-human**](skills/principle-never-block-on-the-human/SKILL.md): Encourages reasonable progress on reversible, authorized work rather than unnecessary clarification, while preserving required approvals and human product decisions.
- [**principle-outcome-oriented-execution**](skills/principle-outcome-oriented-execution/SKILL.md): Keeps phased migrations aimed at the target architecture instead of building temporary compatibility code solely to preserve intermediate states.
- [**principle-prove-it-works**](skills/principle-prove-it-works/SKILL.md): Checks the real behavior or artifact before declaring completion rather than relying only on compilation, summaries, or self-reports.
- [**principle-redesign-from-first-principles**](skills/principle-redesign-from-first-principles/SKILL.md): Reconsiders a design as if a new requirement had existed from the start, then carries the resulting changes through affected references incrementally.
- [**principle-separate-before-serializing-shared-state**](skills/principle-separate-before-serializing-shared-state/SKILL.md): Removes unnecessary shared state between concurrent workers before adding locks or serialization where a shared writer is truly required.
- [**principle-sequence-verifiable-units**](skills/principle-sequence-verifiable-units/SKILL.md): Breaks multi-step work, commits, and PRs into small units that each end in a checked, reviewable state.
- [**principle-subtract-before-you-add**](skills/principle-subtract-before-you-add/SKILL.md): Removes dead code, redundant validation, and stale references before building an addition or refactor on the simpler base.
- [**principle-test-behavior-not-implementation**](skills/principle-test-behavior-not-implementation/SKILL.md): Tests observable behavior so genuine regressions fail while internal refactoring can leave tests passing.
- [**principle-type-system-discipline**](skills/principle-type-system-discipline/SKILL.md): Uses types, validated boundaries, exhaustive variants, and authoritative schemas to make invalid states difficult or impossible to represent.

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
