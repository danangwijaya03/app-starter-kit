# P15 — Restore and recovery

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Incremental preview checkpoint and agent reasoning

Review staging restore/maintenance in an isolated test database only; High reasoning and independent review mandatory, no unattended production restore.

At each safe increment run **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. For UI tasks record fixture/integrated/diagnostic mode, actual URL only if verified, test evidence and user review state via [preview/feedback](../PREVIEW-AND-FEEDBACK.md) and [review queue](../REVIEW-QUEUE.md). Low reasoning may implement bounded work; [Agent Routing](../AGENT-ROUTING.md) identifies critical work recommended for High reasoning and any required independent review. User UI review is non-blocking for other safe ready tasks.

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

## Complete task index from TASKS.yaml

The table above may summarize parent units. The **complete authoritative list** includes microtasks below; always use `python3 tools/agent_tasks.py next` for execution order.

- [P15-01](../tasks/P15-01.md)
- [P15-02](../tasks/P15-02.md)
- [P15-03](../tasks/P15-03.md)
- [P15-04](../tasks/P15-04.md)
- [P15-05A](../tasks/P15-05A.md)
- [P15-05B](../tasks/P15-05B.md)
- [P15-05C](../tasks/P15-05C.md)
- [P15-05](../tasks/P15-05.md)
- [P15-06](../tasks/P15-06.md)
- [P15-07](../tasks/P15-07.md)
