# P02 — Local Lerd Infrastructure

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Isolate MySQL/Redis dev/test, expose safe dev-only readiness diagnostic. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [OPERATIONS](../../references/OPERATIONS.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (7)

| ID | Work unit |
|---|---|
| [P02-01](../tasks/P02-01.md) | Create typed environment validation and examples |
| [P02-02](../tasks/P02-02.md) | Reuse existing Lerd MySQL with isolated dev/test schemas |
| [P02-03](../tasks/P02-03.md) | Reuse existing Lerd Redis and isolate queue connectivity |
| [P02-04](../tasks/P02-04.md) | Build database pool and Redis clients |
| [P02-05](../tasks/P02-05.md) | Add local development orchestration |
| [P02-06](../tasks/P02-06.md) | Validate all environment isolation and secrets hygiene |
| [P02-07](../tasks/P02-07.md) | Expose safe dev-only health diagnostics for API and local services |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
