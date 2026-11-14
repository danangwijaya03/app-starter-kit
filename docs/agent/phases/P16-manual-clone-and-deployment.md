# P16 — Manual Clone/Setup/Production Deployment

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Build three apps, manual npm migration/seed/admin scripts, PM2/Nginx, clean-clone smoke and recovery; no installer. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [OPERATIONS](../../references/OPERATIONS.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (20)

| ID | Work unit |
|---|---|
| [P16-01](../tasks/P16-01.md) | Document manual production runtime prerequisites |
| [P16-02A](../tasks/P16-02A.md) | Validate web production build from source |
| [P16-02B](../tasks/P16-02B.md) | Validate Hono API production build from source |
| [P16-02C](../tasks/P16-02C.md) | Validate BullMQ worker production build from source |
| [P16-02](../tasks/P16-02.md) | Integrate web API and worker npm build |
| [P16-03](../tasks/P16-03.md) | Create read-only manual production environment preflight |
| [P16-04A](../tasks/P16-04A.md) | Implement guarded manual Drizzle migration npm scripts |
| [P16-04B](../tasks/P16-04B.md) | Implement idempotent manual permission sync and seed |
| [P16-04C](../tasks/P16-04C.md) | Wire secure manual admin bootstrap npm command |
| [P16-04D](../tasks/P16-04D.md) | Implement read-only manual setup verification |
| [P16-04](../tasks/P16-04.md) | Gate manual npm setup commands on disposable clone |
| [P16-05](../tasks/P16-05.md) | Configure PM2 for three service runtimes |
| [P16-06](../tasks/P16-06.md) | Verify aaPanel Nginx HTTPS same-origin proxy |
| [P16-07](../tasks/P16-07.md) | Rehearse manual Git update build and restart |
| [P16-08](../tasks/P16-08.md) | Document manual source rollback and database recovery |
| [P16-09A](../tasks/P16-09A.md) | Validate developer clone and npm script guide |
| [P16-09B](../tasks/P16-09B.md) | Validate manual aaPanel server documentation |
| [P16-09](../tasks/P16-09.md) | Gate manual user and operator documentation |
| [P16-10](../tasks/P16-10.md) | Verify new clone isolation without project initializer |
| [P16-11](../tasks/P16-11.md) | Run manual deployment and security end-to-end gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
