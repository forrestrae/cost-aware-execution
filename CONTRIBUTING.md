# Contributing

The skill is one file, [skills/cost-aware-execution/SKILL.md](skills/cost-aware-execution/SKILL.md), with no supporting files.
Keep it that way: every read of a file under the skill directory prompts for permission in the project the skill is used from.

## Setup

The offline checks need Python 3 and PyYAML.
The discovery check needs Node and network access on first run.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

## Offline checks

```bash
python3 -m unittest discover -s tests -v                              # full suite
python3 -m unittest discover -s tests -k test_skill_frontmatter -v    # one test by name
DISABLE_TELEMETRY=1 npx -y skills@latest add . --list                 # expect exactly cost-aware-execution
```

The Python checks verify packaging invariants, not agent behavior.
The reference validator, `skills-ref validate skills/cost-aware-execution`, has not been run for this release; verify its install command before using it.

## Trial install

Create an empty directory outside this repository and run this from inside it:

```bash
npx skills add /path/to/this/repo -a claude-code -a codex -y
```

Never run `npx skills add ... -a` inside this repository.
It writes `.agents/skills/` into the tree and changes what the CLI discovers.

## Smoke cases

Run the three cases in [development/scenarios.json](development/scenarios.json) before a release and after any edit that touches the planning boundary.
Use a trial install in a disposable directory, so a boundary failure cannot change real files, and start a fresh session for each case.

- For a case with `should_trigger: true`, send `/cost-aware-execution` followed by the case prompt. In Claude Code, `claude -p --output-format stream-json --verbose "/cost-aware-execution <prompt>"` captures the tool trace.
- For the case with `should_trigger: false`, send the prompt alone and confirm the skill does not load.

A case passes when every `must_observe` item appears and no `must_not_observe` item does.
One sample per case is enough.
Keep run transcripts, if any, under `development/results/`, which is gitignored; they carry local paths, settings values, and per-run costs.

Keep the set small: add a case only for a boundary regression actually observed.

## Releases

The version lives only in `metadata.version` in `SKILL.md`.
Bump it there; no other file carries a version string.
