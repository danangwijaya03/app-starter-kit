# P15 — Restore and recovery

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Restore dry-run on disposable DB, authorization, rollback and journaling demonstrated.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P15-01](../tasks/P15-01.md) | Define restore workflow, policy and approval gates |
| [P15-02](../tasks/P15-02.md) | Implement restoration archive preflight |
| [P15-03](../tasks/P15-03.md) | Implement isolated staging restore and comparison |
| [P15-04](../tasks/P15-04.md) | Implement external journal and pre-restore backup |
| [P15-05A](../tasks/P15-05A.md) | Implement maintenance mode and queue draining |
| [P15-05B](../tasks/P15-05B.md) | Implement controlled import stage |
| [P15-05C](../tasks/P15-05C.md) | Implement restore failure hold and response |
| [P15-05](../tasks/P15-05.md) | Implement maintenance/drain/import orchestration |
| [P15-06](../tasks/P15-06.md) | Implement post-restore reconciliation and runbook |
| [P15-07](../tasks/P15-07.md) | Verify restore chaos and rollback gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.
