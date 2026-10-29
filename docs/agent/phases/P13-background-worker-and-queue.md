# P13 — Background workers and queues

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Redis job processing, retry and shutdown tests pass.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P13-01](../tasks/P13-01.md) | Initialize BullMQ worker and Redis queues |
| [P13-02](../tasks/P13-02.md) | Implement job metadata, status and owner security |
| [P13-03](../tasks/P13-03.md) | Implement retry/idempotency and reconciliation |
| [P13-04](../tasks/P13-04.md) | Implement job locks and concurrency policy |
| [P13-05](../tasks/P13-05.md) | Implement operational health and request IDs |
| [P13-06](../tasks/P13-06.md) | Verify worker resilience gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.
