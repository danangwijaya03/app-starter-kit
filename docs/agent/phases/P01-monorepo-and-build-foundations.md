# P01 — npm Workspaces and existing Next.js migration

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Incremental preview checkpoint and agent reasoning

Front-load Salt & Pepper UI shell **fixture** using P01-08 after migration and add verified preview smoke/handoff with P01-09. The real authorized shell still belongs to P06.

At each safe increment run **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. For UI tasks record fixture/integrated/diagnostic mode, actual URL only if verified, test evidence and user review state via [preview/feedback](../PREVIEW-AND-FEEDBACK.md) and [review queue](../REVIEW-QUEUE.md). Low reasoning may implement bounded work; [Agent Routing](../AGENT-ROUTING.md) identifies critical work recommended for High reasoning and any required independent review. User UI review is non-blocking for other safe ready tasks.

## Gate before advancing
Existing Next.js moved into apps/web without recreation; npm ci/lint/build work; root npm lockfile consistent.

## Instructions for low-reasoning agent
1. Run `.venv-agent/bin/python tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P01-01A](../tasks/P01-01A.md) | Create root workspace files |
| [P01-01B](../tasks/P01-01B.md) | Create four application package identities |
| [P01-01C](../tasks/P01-01C.md) | Create shared package identities |
| [P01-01](../tasks/P01-01.md) | Create npm workspace and package identities |
| [P01-02](../tasks/P01-02.md) | Pin Node, npm and TypeScript strict configuration |
| [P01-03](../tasks/P01-03.md) | Define Turborepo task graph and package exports |
| [P01-04A](../tasks/P01-04A.md) | Migrate existing root Next.js app into apps/web |
| [P01-04B](../tasks/P01-04B.md) | Create minimal Hono API runtime |
| [P01-04C](../tasks/P01-04C.md) | Create minimal BullMQ worker runtime |
| [P01-04](../tasks/P01-04.md) | Scaffold independent Next.js, Hono and worker entrypoints |
| [P01-05](../tasks/P01-05.md) | Add installer CLI shell and command registry |
| [P01-06](../tasks/P01-06.md) | Proof of Next standalone and API/worker package output |
| [P01-07](../tasks/P01-07.md) | Create CI checks and secret scanning baseline |
| [P01-08](../tasks/P01-08.md) | Early Salt & Pepper shell fixture |
| [P01-09](../tasks/P01-09.md) | Repeatable preview smoke and handoff |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Existing scaffold migration — mandatory

- Do not run `npx create-next-app` again. Root Next.js v16.4.3 app, public/, next config, TypeScript and Tailwind already exist.
- Capture npm ci/npm run lint/npm run build baseline first; preserve errors honestly.
- Create npm workspace root and apps/web package identity in task order; **move existing files** using Git moves, not recreated scaffolds.
- Regenerate single root package-lock using npm install, then verify npm ci and scoped web build/lint.
- Keep cacheComponents, partialPrefetching, experimental.agentFeedback and Turbopack loader config unless explicitly tested incompatible.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains the full list below, including microtasks.** Always select the next ready task with `.venv-agent/bin/python tools/agent_tasks.py next`, not by visual order in this guide.

- [P01-01A](../tasks/P01-01A.md)
- [P01-01B](../tasks/P01-01B.md)
- [P01-01C](../tasks/P01-01C.md)
- [P01-01](../tasks/P01-01.md)
- [P01-02](../tasks/P01-02.md)
- [P01-03](../tasks/P01-03.md)
- [P01-04A](../tasks/P01-04A.md)
- [P01-04B](../tasks/P01-04B.md)
- [P01-04C](../tasks/P01-04C.md)
- [P01-04](../tasks/P01-04.md)
- [P01-05](../tasks/P01-05.md)
- [P01-06](../tasks/P01-06.md)
- [P01-07](../tasks/P01-07.md)
- [P01-08](../tasks/P01-08.md)
- [P01-09](../tasks/P01-09.md)
