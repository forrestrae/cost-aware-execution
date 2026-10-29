# Sources and compatibility

Installed behavior and account policy must be checked before relying on version-sensitive controls.
Each row records the day its pages were last read.

| Source | Used for | Checked on |
| --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | Frontmatter fields, name rules, size recommendation. | verify |
| [skills CLI repository](https://github.com/vercel-labs/skills) (`docs/creating-skills.md`, `docs/agents.md`, `docs/commands.md`) | Discovery layout, agent ids, install paths. | verify |
| [skills.sh](https://skills.sh) | Badge and listing. | verify |
| [Claude Code model configuration](https://code.claude.com/docs/en/model-config) | Start-time model and effort controls. | 2026-10-29 |
| [Claude Code sub-agents](https://code.claude.com/docs/en/sub-agents) | Per-worker model selection and overrides. | 2026-10-29 |
| [Claude Code workflows](https://code.claude.com/docs/en/workflows) | Dynamic Workflows behavior. | 2026-10-29 |
| [Claude Code costs](https://code.claude.com/docs/en/costs) | Usage display and accounting. | 2026-10-29 |
| [Claude Code permission modes](https://code.claude.com/docs/en/permission-modes) | Plan mode and approval controls. | 2026-10-29 |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | Skill layout and invocation. | verify |
| Codex: `learn.chatgpt.com/docs/build-skills`, `docs/config-file/config-basic`, `docs/agent-configuration/subagents`, slash commands | Skills, model and effort configuration, subagent models. | 2026-10-29 |
| [Cursor skills](https://cursor.com/docs/context/skills), subagents, CLI parameters, plan mode | Skills, subagent model field, model flag. | 2026-10-29 |
| GitHub Copilot: about agent skills, CLI command reference, custom agents configuration | Model flag, agent profiles, `/fleet`, `/usage`. | 2026-10-29 |
| OpenCode: `opencode.ai/docs/skills/`, `agents/`, `models/`, `config/`, `cli/` | Model setting, agent models, `opencode stats`. | 2026-10-29 |
| Gemini CLI: `geminicli.com/docs/cli/model`, skills, CLI reference, subagents | Model flag, subagents, replacement notice. | 2026-10-29 |
| Antigravity CLI: `antigravity.google/docs/cli/reference/`, `docs/cli/commands/usage/` | Model and effort flags, usage panel. | 2026-10-29 |

The Platform notes rows were compiled by a subagent that read these pages through a fetch tool that summarizes them, so quotes are secondhand.
Cells it could not source say `verify` in the skill.
The Agent Skills specification and skills CLI details came from the planning session's research on 2026-10-29 and were not re-read during implementation, so their rows say `verify`.

The choice policy, finite inventories, per-unit evidence, budget design, and output contracts are this skill's recommendations.
They do not represent undocumented native enforcement guarantees.
This package does not claim measured credit savings or verified live model routing.
