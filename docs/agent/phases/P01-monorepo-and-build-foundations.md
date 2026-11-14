# P01 — npm Monorepo & Early Preview

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Move existing Next.js, build Hono API and BullMQ worker only, show honest UI fixture and preview smoke. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [REFERENCE-MAP](../../references/REFERENCE-MAP.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (14)

| ID | Work unit |
|---|---|
| [P01-01A](../tasks/P01-01A.md) | Prepare npm workspace root from existing Next.js project |
| [P01-01B](../tasks/P01-01B.md) | Create three application package identities |
| [P01-01C](../tasks/P01-01C.md) | Create shared package identities |
| [P01-01](../tasks/P01-01.md) | Create npm workspace and package identities |
| [P01-02](../tasks/P01-02.md) | Pin Node, npm and TypeScript strict configuration |
| [P01-03](../tasks/P01-03.md) | Define Turborepo task graph and package exports |
| [P01-04A](../tasks/P01-04A.md) | Relocate existing root Next.js into apps/web |
| [P01-04B](../tasks/P01-04B.md) | Create minimal Hono API runtime |
| [P01-04C](../tasks/P01-04C.md) | Create minimal BullMQ worker runtime |
| [P01-04](../tasks/P01-04.md) | Scaffold independent Next.js, Hono and worker entrypoints |
| [P01-08](../tasks/P01-08.md) | Deliver early Salt & Pepper shell as explicit UI fixture |
| [P01-06](../tasks/P01-06.md) | Verify web API worker dev build targets |
| [P01-07](../tasks/P01-07.md) | Create CI checks and secret scanning baseline |
| [P01-09](../tasks/P01-09.md) | Add repeatable development preview smoke and review handoff |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
