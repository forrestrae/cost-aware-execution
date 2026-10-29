# Cost-aware execution

An Agent Skills skill that adds a cost-aware execution strategy to an existing implementation plan.
It chooses between direct work, selective subagents, and the host's orchestration or workflow feature, with model routing by tier, bounded attempts, and verification requirements.
It plans, hands off, and stops: the strategy ends with a handoff for a new session, and the skill never starts the work.

## Install

```bash
npx skills add forrestrae/cost-aware-execution
```

Choose agents, scope, and copy mode with flags:

```bash
npx skills add forrestrae/cost-aware-execution -a claude-code
npx skills add forrestrae/cost-aware-execution -a codex -a cursor
npx skills add forrestrae/cost-aware-execution -g        # user-level install
npx skills add forrestrae/cost-aware-execution --copy    # copy files instead of symlinking
```

The CLI writes the real files to `.agents/skills/cost-aware-execution/` and links agent-specific directories, such as `.claude/skills/cost-aware-execution`, to it with relative symlinks.
Agents that read `.agents/skills/` directly, such as Codex, need no second directory.
Use `--copy` if a host does not follow symlinked skill folders.
Update with `npx skills update cost-aware-execution`.

## Invoke

| Host | Invocation |
| --- | --- |
| Claude Code | `/cost-aware-execution`, or automatically by description |
| Codex | `$cost-aware-execution` or the `/skills` picker |
| Cursor | the `/` picker, or automatically |
| GitHub Copilot CLI | automatically by relevance |
| OpenCode | the `skill` tool |
| Gemini CLI | automatically through `activate_skill`, after a confirmation prompt |

Run it after the implementation plan exists, in the conversation that contains the plan:

```text
/cost-aware-execution Minimize total allowance use. Use the host's orchestration feature only when it earns its setup cost. Preserve all required tests and reviews.
```

You may instead supply a plan path and preferences, such as a concurrency limit.
Running it again updates the strategy and preserves completed-work evidence.

## Use after planning

The result includes the execution model, task allocations, dependencies, write scopes, routing evidence, verification, bounded failures, and necessary setup.
A small plan can receive an all-direct strategy.

The strategy closes with a handoff: the host, the execution session's model and effort level, the start command or setting that selects them, the prerequisites you complete first, and a kick-off prompt to paste as the first message of that session.
The skill does not call a plan-approval tool or offer a mode switch, so the planning session never offers to start implementation.
Start the execution session from the handoff instead.

The skill is one self-contained `SKILL.md` with no supporting files, so invoking it from another project causes no permission prompts for files under the skill directory.

## Orchestration and workflow features

The skill evaluates whether the host's orchestration or workflow feature is appropriate and, when selected, includes a plan-specific workflow specification.
That specification covers stage models, finite worklists, launch and concurrency bounds, result accounting, dependency gates, progress receipts, and resume behavior.
Unknown controls remain explicit prerequisites with a usable fallback.

Claude Code Dynamic Workflows is the one host feature with a row in the skill's Platform notes.
On other hosts the capability is recorded as `unavailable` or `needs-confirmation`, and the strategy falls back to direct work or subagents.
This package ships no prebuilt workflow runner: after you authorize implementation, the execution session translates the specification into the host's native script format.

## Status

This is a best-effort planner, designed to reduce token use when implementing a plan.
Token savings are unmeasured.
Its behavior is spot-checked, not characterized: three [smoke cases](development/scenarios.json) confirm that it plans without starting work, ends with a handoff, and stays out of implementation requests.
It has been tried on Claude Code and Codex; other hosts are untried.

## Repository contents

| Path | Purpose |
| --- | --- |
| [skills/cost-aware-execution/SKILL.md](skills/cost-aware-execution/SKILL.md) | The skill: procedure, model routes, orchestration design, output contracts, and Platform notes, in one file. |
| [development/scenarios.json](development/scenarios.json) | Smoke cases for the planning boundary. |
| [SOURCES.md](SOURCES.md) | Documentation consulted, with checked-on dates. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development checks, trial installs, and smoke cases. |
| [LICENSE](LICENSE) | MIT license. |

The skill has no package dependencies, hooks, or executable code.
Only the development checks in [CONTRIBUTING.md](CONTRIBUTING.md) require Python and PyYAML.
