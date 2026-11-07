# P02 — Local service infrastructure

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Incremental preview checkpoint and agent reasoning

Provide dev-only read-only Hono/MySQL/Redis diagnostics through P02-07 after infrastructure is verified; never expose service credentials or dev route in production.

At each safe increment run **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. For UI tasks record fixture/integrated/diagnostic mode, actual URL only if verified, test evidence and user review state via [preview/feedback](../PREVIEW-AND-FEEDBACK.md) and [review queue](../REVIEW-QUEUE.md). Low reasoning may implement bounded work; [Agent Routing](../AGENT-ROUTING.md) identifies critical work recommended for High reasoning and any required independent review. User UI review is non-blocking for other safe ready tasks.

## Gate before advancing
Use existing **Lerd** MySQL and Redis, prove Node.js 26 runtime connectivity, isolated dev/test schemas, and no duplicate daemon. Do not modify global Lerd proxy/LAN exposure.

**Mandatory local contract:** [Lerd + Node 26 + MySQL](../LOCAL-LERD-NODE26.md). Do not install a new MySQL/Redis service; validate the existing Lerd services before coding.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P02-01](../tasks/P02-01.md) | Create typed environment validation and examples |
| [P02-02](../tasks/P02-02.md) | Reuse existing Lerd MySQL with isolated dev/test schemas |
| [P02-03](../tasks/P02-03.md) | Reuse existing Lerd Redis and isolate queue connectivity |
| [P02-04](../tasks/P02-04.md) | Build database pool and Redis clients |
| [P02-05](../tasks/P02-05.md) | Add local development orchestration |
| [P02-06](../tasks/P02-06.md) | Validate all environment isolation and secrets hygiene |
| [P02-07](../tasks/P02-07.md) | Dev-only Hono / Lerd health view |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains the full list below, including microtasks.** Always select the next ready task with `python3 tools/agent_tasks.py next`, not by visual order in this guide.

- [P02-01](../tasks/P02-01.md)
- [P02-02](../tasks/P02-02.md)
- [P02-03](../tasks/P02-03.md)
- [P02-04](../tasks/P02-04.md)
- [P02-05](../tasks/P02-05.md)
- [P02-06](../tasks/P02-06.md)
- [P02-07](../tasks/P02-07.md)
