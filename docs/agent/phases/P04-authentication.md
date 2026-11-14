# P04 — Better Auth & Sessions

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Real login/logout/reset/first-login change, deny unauthorized access. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [AUTH](../../references/AUTH.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (7)

| ID | Work unit |
|---|---|
| [P04-01](../tasks/P04-01.md) | Configure Better Auth MySQL adapter |
| [P04-02](../tasks/P04-02.md) | Mount auth routes in Hono and session middleware |
| [P04-03](../tasks/P04-03.md) | Implement login/logout UI and auth client |
| [P04-04](../tasks/P04-04.md) | Implement password reset and activation flow |
| [P04-05](../tasks/P04-05.md) | Enforce user status and must-change-password guard |
| [P04-06](../tasks/P04-06.md) | Implement own profile/session termination |
| [P04-07](../tasks/P04-07.md) | Complete authentication security gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
