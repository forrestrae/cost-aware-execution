---
name: cost-aware-execution
description: >-
  Use when an existing implementation plan needs an execution strategy that conserves usage credits, tokens, or model spend, including cheaper model tiers, selective subagents, or a host orchestration or workflow feature. Works in any coding agent that supports Agent Skills. Not for initial architecture planning or executing an approved strategy.
license: MIT
metadata:
  version: "0.4.0"
---

# Cost-aware execution strategy

Minimize expected total usage to reach a correct, verified result.
Produce a strategy for the existing plan, end with a handoff that a fresh session can execute, and stop.
This file is self-contained; it has no supporting files to read.
Host-specific names appear only in the Platform notes section; identify the host before using them.

## Planning boundary

Remain in the current planning workflow.
Use permitted read-only inspection and update only the authorized plan artifact; return the strategy in chat if that artifact is not writable.
Do not launch agents or workflows, implement tasks, run builds or tests, install dependencies, or change models, configuration, permissions, branches, or worktrees.
Do not create workflow or orchestration scripts or open the host's authoring reference during this planning step.
Do not call a plan-approval or exit-planning tool, request plan approval, offer a permission or mode switch, or offer to begin implementation in this session; execution starts in a new session from the handoff.
Preserve scope, architecture, acceptance criteria, repository instructions, and required reviews.
Flag plan defects separately and block affected units.

## Procedure

1. Ground the strategy in the current plan, task IDs, and progress evidence.
   A plan supplied in the invocation or the conversation is the plan; do not search the working tree for another copy of it, for its tasks, or for evidence it does not mention.
   Read a repository file only when the plan names it or an allocation decision depends on it.
   If no usable plan exists, ask for its content or path.
   Repeated invocation updates the existing strategy and retains completed work and evidence.

2. Identify available model controls and relevant constraints from session metadata, tool schemas, and narrow non-secret configuration inspection.
   Identify the host agent from session metadata, tool names, and system context, and record it as observed or unknown; the handoff uses that host's Platform notes row.
   Apply the Model routes and capability states section below.
   Describe model routes with its routing states and the presence of tools or features with its capability states; the two vocabularies are not interchangeable.
   Treat absent evidence as unknown.
   When a supplied fact conflicts with what the session shows, record both and allocate for each branch instead of discarding either.
   Avoid paid probes, broad documentation research, and credential or configuration dumps.

3. Group work into cohesive units with dependencies, write ownership, and acceptance checks.
   A unit is a batch, not a file, fixture, or item: fold similar mechanical items into as few units as their verification and write ownership allow, and keep coupled interfaces together.
   Every dispatch pays coordination, context, setup, worker calls, retries, review, and integration cost, so account for those per unit before choosing a unit count.

4. Select an execution mechanism for each unit.
   Use `direct` for small or tightly coupled work, `subagent` for justified bounded delegation, or `workflow` for repeatable orchestration across independent units.
   If workflows are requested or could materially reduce repeated coordination, apply the Orchestration and workflow selection and design section below and record a suitability decision.
   An all-direct strategy is valid.
   One dispatch per item is a design to justify, not a default: compare it against a batched alternative that covers several items per worker and record why the batch loses, if it does.
   More concurrency alone is not a usage saving.

5. Allocate the least expensive available model likely to finish each unit reliably, including the main execution session.
   Prefer the economical tier for fully specified low-risk work, the standard tier for ordinary implementation and integration, and deeper reasoning for a justified blocked decision or risk.
   Choose the execution session's model and effort level explicitly; the handoff restates them.
   Specify supported effort for workers when useful.
   Record actual selection mechanisms, relevant overrides, observation methods, and fallbacks.
   A prompt label or proposed definition is not configured or observed routing.

6. Define bounded delegation and verification.
   Start sequentially; parallelize only independent work with nonconflicting write ownership or explicit isolation and integration.
   State concurrency and total worker-launch limits separately.
   No default agent-per-file, agent-per-item, agent teams, nested delegation, or universal premium review.
   Use compact sufficient briefs and evidence-based handoffs, accounting for inherited context when applicable.
   Preserve deterministic checks, required independent reviews, and final integration verification.
   Allow one focused same-tier repair after a substantive failure, then diagnose context, environment, specification, or reasoning before a bounded reassessment or escalation.
   An environment or specification remedy does not restore the repair; after the remedy, the unit gets one bounded reassessed attempt.
   If that approach also fails, pause the affected unit for a decision.
   Carry failure evidence forward and return routine work to the economical route.

## Deliverable

Use the Execution strategy output contract section below, scaled to the actual plan.
A tiny plan needs a short recommendation, one allocation row, and the handoff.
Map every remaining task and acceptance requirement; preserve completed-task evidence without rescheduling finished work.
For workflow selections, include the Workflow specification contract inside the plan.
Define the later progress record, setup, checkpoints, and unresolved prerequisites without creating runtime artifacts now.
Keep estimates qualitative unless applicable measurements exist.
Separate API-equivalent estimates from subscription allowance and advisory targets from enforced limits.
End with the handoff: execution model, effort level, start command or setting, prerequisites, and a kick-off prompt complete enough for a session that has no context.
Repeat the handoff in the closing chat message even when the strategy was saved to the plan.
Stop after presenting or saving the strategy and its handoff; the user starts execution in a new session.

## Model routes and capability states

Host documentation dates are in Platform notes.
Use installed-version behavior and live tool schemas to resolve the actual session.
This section informs proposed setup; it does not authorize configuration changes.

### Allocation policy

Consider the economical tier for narrow mechanical work, the standard tier for normal implementation and integration, and the premium tier for justified difficult reasoning.
A tier is a role; resolve the host's and account's actual model names from session evidence, never from memory, and prefer aliases or release IDs the account exposes over hard-coded versions.
Small tasks can still require substantial judgment.
Choose the main execution-session model explicitly so a premium planning session does not become an unnecessarily expensive coordinator.
If cheap routing is unavailable, improve batching and context discipline.

### Selection and observation

Model selection can use a start-time flag, an in-session command, a configuration file or profile, an environment variable, or an agent definition; the host's precedence among these is in its documentation and its Platform notes row.
Overrides, model allowlists, and inheritance affect the result.
Inspect only relevant non-secret fields, such as worker-model override variables or agent definitions the host documents.

Record the selector, requested model, applicable override, fallback, and observation method for each route.
Use these states consistently:

| State | Evidence required |
| --- | --- |
| `observed` | Runtime evidence identifies the model that actually ran. |
| `configured-not-observed` | Existing effective configuration or a confirmed supported invocation selector establishes the route, but the worker has not run. |
| `requires-user-action` | A model switch, new definition, configuration change, or capability confirmation is still needed. State the exact dependency. |
| `unavailable` | The installed runtime or account cannot provide the route. Supply a fallback. |

These states describe model routes only.
Describe whether a tool or feature exists with the capability states below; a tool listed in the session is `available`, never `configured-not-observed`.

| Capability state | Evidence required |
| --- | --- |
| `available` | The tool or feature is listed in the session or confirmed by installed help. |
| `needs-confirmation` | The feature is claimed or plausible, but its presence, local API, or a setting that governs it has not been checked. State what to check. |
| `unavailable` | The installed runtime, account, or managed settings exclude it. Supply a fallback. |

Declining a workflow is a suitability decision; record it separately from the capability state.
An uncreated agent file belongs in `requires-user-action`.
A proposed workflow option whose local API signature is unknown is not confirmed configuration.
Do not label future workers observed because the main model is known.
After execution is authorized, use exposed metadata and warnings from the first necessary dispatch to check the route before repeating it.
If observation is unavailable, retain the uncertainty; do not dispatch a probe to fill the table.

### Execution-session choices

The execution session is a new session the user starts from the handoff, so its model and effort are start-time choices, not changes to make here.
Use the host's Platform notes row for the exact flag, command, or setting; prefer start-time controls because they need no in-session command.
Effort or reasoning levels and their names depend on the host and model; name the level the host documents.
A host mode that pairs a premium planning model with a cheaper execution model does not assign models to workers, and planning is already done when the handoff is used.

Prefer the smallest setup change and reuse appropriate existing agents.
Do not force every worker to a cheaper model when required work needs another route.

### Usage

Use the host's usage display when it exists and distinguish its accounting basis.
Do not infer a subscription-allowance saving from API-equivalent figures.
Budget checkpoints should interrupt additional spending decisions while preserving required verification, not weaken acceptance criteria.

### Platform notes

Checked on 2026-10-29 against each host's documentation; a cell marked verify has not been confirmed and is `needs-confirmation` until checked.
A host not in the table gets `needs-confirmation` for every control; ask the user for its model and effort selectors.

| Host | Start-time model and effort | Delegation and per-worker model | Workflow or orchestration feature | Usage visibility |
| --- | --- | --- | --- | --- |
| Claude Code | `claude --model <alias> --effort <level>`; `/model`, `/effort`; `ANTHROPIC_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`; `model`, `effortLevel` settings | Agent tool `model` parameter; `model` in agent frontmatter; `CLAUDE_CODE_SUBAGENT_MODEL` is a default, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` forces it | Dynamic Workflows: Workflow tool, `/workflow-authoring`, JavaScript scripts | `/usage` |
| Codex CLI | `codex -m <model>`; `/model`; `model`, `model_reasoning_effort` in `config.toml`; `--profile <name>`; `-c key=value` | `.codex/agents/*.toml` with `model`, `model_reasoning_effort`; `agents.default_subagent_model`; `/subagents`; unset workers inherit | none documented | `/status`; `/usage` |
| Cursor | `--model <model>` (CLI); `/model`; effort control: verify | `.cursor/agents/*.md` with `model` frontmatter (default `inherit`) | verify | verify |
| GitHub Copilot CLI | `--model=<model>`; `/model`; effort flag and environment variable: verify | `--agent`, `/agent`; `model` in agent profile frontmatter, inherited if unset | `/fleet` for parallel subagents; further orchestration: verify | `/usage` |
| OpenCode | `--model provider/model-id`; `model` in `opencode.json`; `/models`; provider options such as `reasoningEffort`: verify | `agent.<name>.model`; Task tool; subagents inherit the invoking agent's model | none documented | `opencode stats` |
| Gemini CLI | `--model <name>`; `/model`; effort control: verify; docs state Antigravity CLI replaced it on 2026-06-18 | `.gemini/agents/*.md` with `model`; `/model` and `--model` do not change sub-agent models | verify | `/stats` |
| Antigravity CLI | `--model`; `--effort`; `/model`; `/effort` | `--agent`; per-worker model selector: verify | verify | `/usage` |

Plan-approval and mode-switch controls the planning boundary forbids: Claude Code `ExitPlanMode` and permission modes; Codex `/plan`; Cursor `/plan` and `--plan`; Copilot CLI `/plan`; OpenCode Plan agent switch; Gemini CLI `/plan` and `--approval-mode`; Antigravity CLI `/plan`.

Claude Code orchestration answers, checked 2026-09-17 and not re-verified in full: JavaScript coordinates agents and keeps intermediate values outside the conversation; script-selected models use subagent routing precedence; `workflowSizeGuideline=small` is advice, not a cap; normal user input cannot be collected mid-run; failed, stopped, or blocked calls can produce `null` and schema validation can retry internally; relaunch can rerun completed agents; scripts do not touch files, shell, or modules directly, workers do; `/workflow-authoring` is the installed authoring reference.

## Orchestration and workflow selection and design

Apply this section only when the host's orchestration or workflow feature is requested or plausible for the plan.
Treat a workflow as one execution mechanism under the same cost and quality policy.

### Suitability decision

Prefer a workflow when a reusable pattern across independent units avoids repeated coordination and its implementation cost is proportionate.
Consider direct execution for a short dependency chain, ambiguous interfaces, or many shared writes.
Ordinary subagents remain useful for a few isolated units.
Record the expected source of savings and the simpler fallback; task count alone does not establish value.

### Host behavior to establish

Answer these from the host's documentation or the feature's tool description before relying on the feature:

- Where does orchestration state live, and does it persist outside the conversation?
- How do scripts select worker models, and do the host's overrides and inheritance rules apply?
- Are size or budget settings advisory or enforced?
- Can a run collect user input mid-run? If not, split runs at human decisions.
- What does a failed, stopped, or blocked worker return, and does the runtime retry internally?
- Does relaunch rerun completed workers?
- Can the script touch files, shell, or modules, or only workers can?
- Where does the installed authoring reference live?

The answers for a host whose feature is documented are summarized in Platform notes.
A host with no such feature gets `unavailable` and a direct or subagent strategy.

A tool description in the session describes the happy path; the relaunch question above still applies.

### Capability decision during planning

Check supplied session evidence for the orchestration feature, model selectors, authoring support, relevant settings, and available observation.
Record `available`, `needs-confirmation`, or `unavailable`, as defined above, with evidence.
Do not enable features, change effort, author scripts, or launch a trial while preparing the strategy.
If the API is unknown, produce a specification and defer executable syntax to installed authoring guidance during authorized execution.
Do not invent orchestration API options or promise concurrency, cancellation, or spending controls that have not been established.
Declining a workflow must leave a usable direct or subagent strategy.

### Cost-aware workflow contract

Use the Workflow specification contract section as the required output structure.
Its constraints are design requirements for a later implementation, not claims about native defaults.

1. Freeze a finite worklist from actual remaining plan IDs.
   Batch related units, name dependency barriers, and give shared outputs one integration owner.
   Any discovery stage must return a bounded list before additional work starts.
2. Assign a model to every model-using stage, including discovery, repair, review, and synthesis.
   Keep mechanical enumeration and checks in deterministic tools where possible.
   Specify how the installed interface selects and exposes each route.
3. Set separate maximums for concurrent workers, total launches, and attempts per unit.
   Include review, repair, escalation, relaunch, and known internal retries in the accounting.
   Charge every new dispatch before it starts and halt scheduling at the agreed boundary.
   If nested delegation is unnecessary, prohibit it in worker briefs so it cannot expand the intended workload.
   A launch cap is not a hard token, credit, or subscription-allowance cap.
4. Require an explicit result for every expected unit: state, changed files, verification evidence, attempts, routing evidence, and blocker.
   Record `null`, missing, duplicate, malformed, or unverified results as unresolved.
   Never filter failed results out of the completion accounting.
   Downstream integration requires all necessary predecessor checks to pass.
5. Keep a durable execution record outside script variables.
   Reuse an existing record and designate one writer, or separate per-unit receipts with one consolidator.
   Identify inputs and verification definitions so completed evidence can be checked for freshness.
   On resume, reconcile actual files and evidence before trusting cached outputs.
   Design repeated edits to be safe or guarded by verified completion receipts.
   Propose separate bounded workflow runs when that would contain replay cost or create a needed decision point.
6. Use the single-repair and bounded-reassessment policy from the procedure.
   Record environment and specification failures before changing models.
   Escalate only the blocked unit; stop it if the reassessed approach fails.
   Preserve final verification and required independent review.

### Handoff after execution authorization

The plan should direct the execution session to check the host's installed authoring reference, then translate the approved specification into native syntax.
Confirm selectors and implemented bounds before the first necessary dispatch.
Keep the workflow script reviewable alongside its plan revision and progress evidence.
Honor existing authorization and host permissions; a runtime launch prompt is not guaranteed to appear.
Do not raise effort to its maximum level or enable orchestration features as an automatic setup step.

For unfamiliar workloads, propose a small representative pilot within the authorized scope, then decide whether to continue using observed attempts, quality, and usage.
Compare complete verified results against ordinary execution, with coordinator and worker usage included.
Report time, tokens, allowance measurements, and estimates separately.

## Execution strategy output contract

Append or update one section titled "Execution strategy" inside the authorized plan, with the subsections below.
Use actual tasks and evidence; scale the structure to the plan.
This is a format reference, not another file to create during planning.

### Recommendation and known state

Identify the plan revision, completed task IDs, evidence, runtime constraints, and the host agent and version as observed, and the recommended execution-session model and supported effort.
Distinguish observed facts, proposed configuration, and unknowns.
Explain the chosen mix of execution mechanisms and the expected savings mechanism.
When a request mentions speed or parallelism, say separately what it buys in elapsed time and what it buys in usage.
When workflows are considered, record their capability state (`available`, `needs-confirmation`, or `unavailable`), suitability decision, and fallback.

### Allocation

| Plan IDs | Unit and dependencies | Mechanism: direct, subagent, workflow | Owner and write scope | Model | Effort | Rationale | Selector and routing status | Acceptance and required review | Escalation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Model, Effort, and Rationale are each required in every row: the model alias or ID, the effort level, and the reason that pairing fits the unit's risk and specification.
Every remaining task and acceptance requirement must map to a unit or integration checkpoint.
Where a row covers many similar items, state the batch size per dispatch and why one dispatch per item was rejected or chosen.
Identify which workflow stage implements a workflow-owned row.
Name selectors and applicable setup dependencies, not only model labels; state the model as the alias or ID the host selects it by.
Use `observed`, `configured-not-observed`, `requires-user-action`, or `unavailable` as defined in the Model routes and capability states section.
Preserve completed work without allocating it again.

### Waves and completion evidence

State dependency order, maximum concurrent workers, total launch limit, shared-resource ownership, and the integration owner.
Specify targeted checks, required independent reviews, and final integration verification.
Name when effective routing will be observed and how a mismatch changes subsequent dispatch.
If a control is only a planning target, label it accordingly.

### Dispatch brief

For justified delegation, populate the first real unit and provide the reusable fields below.
An all-direct strategy needs no worker brief.

```text
Unit and plan IDs; dependencies:
Objective and minimum sufficient references:
Relevant repository instructions and interface constraints:
Allowed write scope and integration owner:
Requested model, effort, selector, known overrides, fallback:
Acceptance checks and required review:
Attempt allowance, reassessment/escalation trigger, stopping condition:
Nested delegation: disabled unless explicitly budgeted in the approved plan.
Return: unit state; changed files; concise result; checks and outcomes;
        evidence references; attempts used; blockers;
        actual routing evidence when exposed.
```

### Workflow specification, when selected

Include the Workflow specification contract, filled with actual plan IDs and bounds.
Describe the future native implementation and its setup prerequisites without writing or launching it now.

### Progress, setup, and usage checkpoints

Reuse or propose one progress record containing task state, input/check identity, decisions, requested/observed route, attempts, verification evidence, and next action.
Identify necessary setup, user-issued commands, unknowns, and fallback behavior.
Separate enforced controls from advisory settings and desired budgets.
Keep usage estimates qualitative without relevant measurements.
Name checkpoints for exhausted attempts, routing mismatches, unexpected cost, and blocked work.

### Handoff

Close with everything a new session with no context needs to execute the strategy.
The reader is the user, who will paste the kick-off prompt into that session, so the block must not depend on this conversation.

1. Execution session: the host, the model alias or ID, the effort or reasoning level, and the start command or setting from that host's Platform notes row, run from the project directory.
   If the host could not be determined, say so and give the model and effort as names the user applies in their host's settings.
   State how the session reaches a plan stored outside the project, and name any in-session command that must run instead of a start-time control.
2. Prerequisites the user completes first, each with its routing or capability state: agent definitions to create, environment variables or settings to set, approvals to grant, and facts still to confirm.
   Write "none" when nothing is required.
3. Kick-off prompt, in one fenced text block, to paste as the first message.
   It states the absolute plan path and tells the session to read the plan and its Execution strategy section first, then the task IDs already complete and their evidence, the first unit or wave to start, the progress record location and fields, the attempt, concurrency, and launch limits, the checks and required reviews that gate completion, and what to report at each checkpoint or when a unit pauses.
   Name the plan path even when the tasks are short enough to restate; the saved strategy is the record the execution session updates.
   When the strategy was returned in chat rather than saved, include the full strategy inside the block instead.

End with the handoff; do not imply execution has begun, and do not ask the user to approve the plan or change modes here.

## Workflow specification contract

Fill these fields within the execution strategy only when a workflow is selected.
Use concrete plan values; mark unresolved facts explicitly.
This contract describes what a future script must implement and how it will be checked.
It is not executable JavaScript or a fixed orchestration template.

### Workflow identity and suitability

- Plan revision and workflow-owned task IDs.
- Benefit over direct work or ordinary subagents; expected reuse.
- Capability evidence and unresolved native API questions.
- Simpler fallback and the condition that selects it.

### Inputs and stages

- Finite unit inventory, stable IDs, completed exclusions, and relevant input/check identities.
- Stage order, dependency barriers, batch boundaries, integration owner, and human decision boundaries.
- Per-stage model, supported effort, selector, routing state, observation method, and fallback.
- Minimal context, allowed files, shared-resource ownership, and isolated workspaces if necessary.

### Bounds and attempts

- Maximum concurrent workers and total worker launches, including review and escalation.
- Per-unit initial attempt, one focused same-tier repair, and one bounded reassessed attempt when justified.
- How runtime schema retries, API failures, and interrupted-run relaunch affect accounting.
- Where the launch counter is checked; what stops when a limit is reached.
- Which controls can be enforced by the chosen API and which remain advisory or unknown.
- Usage checkpoints, including any pilot; no unverified hard spending cap.

### Results and completion

Require one accountable result per expected unit:

```text
unit_id:
state: pending | running | verified | failed | blocked
input_and_check_identity:
changed_files:
verification: command or check ID; outcome; evidence reference
attempts_and_launches_used:
requested_model_and_effort:
observed_routing_or_unknown:
blocker_and_next_action:
```

- Null, absent, duplicate, invalid, and unverified outputs stay unresolved.
- All required predecessor results must be verified before downstream integration.
- Final completion also requires the plan's integration checks and required independent review.

### Persistence and resume

- Durable record location and its writer; per-unit receipts if concurrent workers need them.
- How a resumed run reconciles current files with recorded input and check identity.
- How unchanged verified units are preserved and stale evidence is invalidated.
- How repeat edits are made safe or skipped based on verified receipts.
- Replay risk, restart cost, remaining launch allowance, and criteria for starting a new bounded stage.

### Implementation handoff

- Authorization still needed, honoring decisions already made by the user.
- Installed authoring reference to consult, per the host's Platform notes row.
- Native syntax and bounds to validate before dispatch.
- Proposed script location and how it will be reviewed against this specification.
- First necessary dispatch used to check routing, with mismatch behavior.
