# AGENTS.md

This file provides guidance to coding agents working in this repository.

## What this repository is

An Agent Skills repository with one skill, `cost-aware-execution`, installed with `npx skills add forrestrae/cost-aware-execution`. The skill is instruction-only: one `SKILL.md`, no hooks, no servers, no executable code. Python exists only for the offline packaging tests under `tests/`.

The tree originated as a ChatGPT Work export and is now this git repository. The skill is a best-effort token saver, not production software, so its behavior is spot-checked with three smoke cases rather than validated. Run transcripts, when kept, live under `development/results/`, which is gitignored and never published because the records carry local paths, settings values, and per-run costs.

## Commands

`CONTRIBUTING.md` is the single source for setup, the offline suite, the discovery check, trial installs, and the smoke-case procedure. Read it before running any of them. The full suite is `python3 -m unittest discover -s tests -v` inside the `.venv`.

Never run `npx skills add ... -a` inside this repository: it writes `.agents/skills/` into the tree and changes what the CLI discovers.

## Layout invariants

`tests/test_package.py` enforces nine checks:

1. Exactly one skill at `skills/cost-aware-execution/SKILL.md`; no root `SKILL.md`, `skills.sh.json`, `.claude-plugin`, `plugins`, `.agents`, or `.claude/skills` directory.
2. Frontmatter keys are a subset of the Agent Skills fields (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`); `name` equals the directory name; `metadata.version` is required.
3. `SKILL.md` is at most 500 lines.
4. The skill directory holds only `.md` or `.json` files and no symlinks.
5. Relative links in the skill resolve inside the skill directory. The skill has none; adding one reintroduces a permission prompt for every project the skill is used from.
6. Every relative Markdown link in the repository resolves.
7. Every Markdown file ends with a newline and has balanced code fences.
8. `development/scenarios.json` uses `schema_version` 1; each case has a unique `id`, a `platform` from the skills CLI agent ids or `any`, a boolean `should_trigger`, a `prompt`, and non-empty `must_observe` and `must_not_observe` lists; at least one case has `should_trigger` false.
9. Host product names, commands, variables, tool names, and documentation links appear only inside the `### Platform notes` subsection of `SKILL.md`. This is a layout invariant about where host names may live, not a behavioral check.

## How the skill is structured

`SKILL.md` is the whole skill and defines the one hard design rule: the skill plans, hands off, and stops. It must not launch agents or workflows, edit source, run tests, call a plan-approval tool, offer a mode switch, or change models, settings, permissions, branches, or worktrees. It updates only the authorized plan artifact, or returns the strategy in chat, and closes with a handoff (host, model, effort, start command or setting, prerequisites, kick-off prompt) for a new session with no context. The smoke cases in `development/scenarios.json` test this boundary, so any change to the skill has to preserve it.

The file is deliberately self-contained. Version 0.2.0 split the references and contracts into supporting files, but every scenario run read two to four of them anyway, and each read of a file outside the working directory prompts for permission with no way to pre-allow it. Keep everything in `SKILL.md`; do not reintroduce supporting files. Its sections are:

- Model routes and capability states, read on every invocation. It defines the routing-state vocabulary (`observed`, `configured-not-observed`, `requires-user-action`, `unavailable`) and the capability-state vocabulary (`available`, `needs-confirmation`, `unavailable`); the handoff smoke case checks for them, so keep both tables verbatim. An agent definition that does not yet exist is `requires-user-action`, never `configured-not-observed`. It uses tier vocabulary (economical, standard, premium) in place of model names, and ends with the Platform notes table, the only place host names may appear.
- Orchestration and workflow selection and design, applied only when the host's feature is requested or plausible. It turns host behavior into questions the planner answers, and records the design rules a future script must satisfy.
- Execution strategy output contract: the "Execution strategy" section appended to or updated in the plan, ending with the Handoff subsection. It is a format reference, not a file the skill creates.
- Workflow specification contract, nested inside that section only when a unit's mechanism is `workflow`. The skill never writes the script.

Model policy: economical tier for narrow mechanical work, standard tier for ordinary implementation, premium tier only with a stated justification, and the main execution session chosen explicitly. Attempt policy: one same-tier repair, then diagnosis, then one bounded reassessment, then pause the unit.

## Documentation conventions

The docs deliberately separate claims by evidence level. Keep that separation when editing:

- Offline tests verify packaging invariants only. A smoke case run shows the skill held the planning boundary on one sample. Neither establishes host discovery, effective model routing, or usage savings, and the docs must not say otherwise.
- `SOURCES.md` and the Platform notes subsection carry "checked on" dates. Update the date when re-verifying against the documentation. A Platform notes cell that was not confirmed says `verify`; never guess.
- The version lives only in `metadata.version` in `SKILL.md`. Do not add a version string to `README.md` or any other file.
- The Smoke cases section of `CONTRIBUTING.md` defines how to run the cases. Keep the set small: add a case only for a boundary regression actually observed, and do not reintroduce a validation ledger.

The Executive Technical writing style applies to prose in this repository: no em dashes, no bold in prose, no section symbols, headings in sentence case.
