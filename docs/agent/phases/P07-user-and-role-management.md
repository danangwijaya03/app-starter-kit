# P07 — Users & Roles

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Typed CRUD user/role and permission matrix with server denial tests. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [RBAC](../../references/RBAC.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (7)

| ID | Work unit |
|---|---|
| [P07-01](../tasks/P07-01.md) | Implement user list and detail APIs |
| [P07-02](../tasks/P07-02.md) | Implement invitation and user updates |
| [P07-03](../tasks/P07-03.md) | Implement roles CRUD and policy APIs |
| [P07-04](../tasks/P07-04.md) | Build Users management UI |
| [P07-05](../tasks/P07-05.md) | Build Roles and grouped permissions editor |
| [P07-06](../tasks/P07-06.md) | Integrate multi-role assignment and audit |
| [P07-07](../tasks/P07-07.md) | Verify user and role management gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
