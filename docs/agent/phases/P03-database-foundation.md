# P03 — Drizzle MySQL Foundation

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Versioned schema, reviewed migrations, read-only DB health. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [SECURITY](../../references/SECURITY.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (11)

| ID | Work unit |
|---|---|
| [P03-01](../tasks/P03-01.md) | Generate Better Auth Drizzle MySQL schema |
| [P03-02](../tasks/P03-02.md) | Define app user profile and RBAC tables |
| [P03-03A](../tasks/P03-03A.md) | Define CMS pages and revisions schema |
| [P03-03B](../tasks/P03-03B.md) | Define CMS menus and menu items schema |
| [P03-03](../tasks/P03-03.md) | Add CMS pages/revisions and navigation schema |
| [P03-04](../tasks/P03-04.md) | Add media, settings and user preferences schema |
| [P03-05](../tasks/P03-05.md) | Add audit, system jobs and backup tables |
| [P03-06](../tasks/P03-06.md) | Generate and review migration history |
| [P03-07](../tasks/P03-07.md) | Build transaction helper and repository abstractions |
| [P03-08](../tasks/P03-08.md) | Implement audit event service and seed base |
| [P03-09](../tasks/P03-09.md) | Connect safe DB readiness to development health diagnostic |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
