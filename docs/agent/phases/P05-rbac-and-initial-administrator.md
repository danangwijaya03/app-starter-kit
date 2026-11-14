# P05 — Database RBAC & Manual Admin Bootstrap

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Secure permission registry, server checks and manual first-admin bootstrap, race denial. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [RBAC](../../references/RBAC.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (12)

| ID | Work unit |
|---|---|
| [P05-01](../tasks/P05-01.md) | Define canonical permission manifest and validation |
| [P05-02](../tasks/P05-02.md) | Build permission sync check/apply commands |
| [P05-03](../tasks/P05-03.md) | Seed default protected roles |
| [P05-04](../tasks/P05-04.md) | Implement authorization service and policies |
| [P05-05](../tasks/P05-05.md) | Implement route permission middleware |
| [P05-06](../tasks/P05-06.md) | Build role assignment concurrency invariants |
| [P05-07A](../tasks/P05-07A.md) | Create safe bootstrap credential input |
| [P05-07B](../tasks/P05-07B.md) | Provision first user and assign super_admin |
| [P05-07C](../tasks/P05-07C.md) | Verify first login bootstrap flow |
| [P05-07](../tasks/P05-07.md) | Implement secure idempotent first-admin bootstrap |
| [P05-08](../tasks/P05-08.md) | Implement authorization invalidation and module nav registry |
| [P05-09](../tasks/P05-09.md) | Verify comprehensive RBAC/security gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
