# P02 — Local service infrastructure

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
MySQL and Redis development connectivity proven without assuming production Docker.

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
| [P02-02](../tasks/P02-02.md) | Provision disposable local MySQL 8.4 |
| [P02-03](../tasks/P02-03.md) | Provision local Redis and queue connectivity |
| [P02-04](../tasks/P02-04.md) | Build database pool and Redis clients |
| [P02-05](../tasks/P02-05.md) | Add local development orchestration |
| [P02-06](../tasks/P02-06.md) | Validate all environment isolation and secrets hygiene |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.
