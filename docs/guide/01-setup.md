# Set up this collection

Copy the complete skill folders you need into your harness's skill directory. Keep `model-configuration` beside the workflows, together with the companions listed in [the import notes](../../PSTACK_IMPORT.md). Copying this repository does not install upstream's full pstack plugin or its optional tools. See [the README](../../README.md) for the portable paths.

## Pick your models

Use [`model-configuration`](../../skills/model-configuration/SKILL.md). It reads pstack's existing role settings and adds a portable project override at `.agents/pstack-models.md`. The bundled preferences are Astra/high for main-session oversight and Sol 6.1 for every subagent role. Worker effort is left to the harness unless separately configured. Omitting the effort override inherits the parent's level only where the harness supports that.

The skill checks the current runtime's supported model IDs and effort options before spawning. An unavailable choice falls back to the current model with a disclosure. Model names are not portable availability guarantees. The main chat must be selected through your harness; editing these files cannot switch it.

The project file takes precedence over the harness's existing user-level pstack settings file. Missing roles use bundled defaults. `auto` and `inherit-parent` omit a model override. Panel lists keep one seat per entry, including repeated models. Repeated Sol workers provide independent attempts, not different model families. Arena skips an unavailable cross-family judge and says so. Other workflows may keep a cross-family review as an unmet shipping gate.

## Change cost and effort

Ask `model-configuration` to change the relevant roles, effort settings, or panel sizes. It preserves unrelated choices. Effort is a separate field, never an invented suffix. Optional upstream `/setup-pstack` is not bundled and should not overwrite these extended settings.

Verification-generation skills described elsewhere in the upstream guide are optional and are not installed by this collection's configuration skill.

## Run your first task

Pick something real but small, and describe it the way you'd describe it to a colleague:

```text
/poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

Watch the todo list. Its first items are the matched playbook's steps copied in, the Feature playbook for this prompt. If `/poteto-mode` skips a step, the step stays in the list with `skip: <reason>`, so you can see what it chose not to do.

From here you can type normal follow-ups. To keep `/poteto-mode` on for the whole chat, pick it from the `/` menu with Option+Enter (Mac) or Alt+Enter (Windows) instead of Enter. That makes it a [Custom Mode](https://cursor.com/docs/skills#using-a-skill-as-a-custom-mode), which stays in context on every turn until you exit it. Custom Modes are available in the Agents Window and the CLI. Plain Enter attaches the skill to one message, and it fades as the chat moves on.

Next: [Route work through `/poteto-mode`](./02-poteto-mode.md).
