# P14 — Backup operations

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Incremental preview checkpoint and agent reasoning

Review encrypted backup on disposable DB and restore verification; High reasoning and independent review mandatory.

At each safe increment run **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. For UI tasks record fixture/integrated/diagnostic mode, actual URL only if verified, test evidence and user review state via [preview/feedback](../PREVIEW-AND-FEEDBACK.md) and [review queue](../REVIEW-QUEUE.md). Low reasoning may implement bounded work; [Agent Routing](../AGENT-ROUTING.md) identifies critical work recommended for High reasoning and any required independent review. User UI review is non-blocking for other safe ready tasks.

## Gate before advancing
Backups encrypted, verified, consistent and safely stored off webroot.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P14-01](../tasks/P14-01.md) | Implement backup manifest and encryption interface |
| [P14-02A](../tasks/P14-02A.md) | Prepare safe mysqldump command builder |
| [P14-02B](../tasks/P14-02B.md) | Implement dump streaming and cancellation |
| [P14-02](../tasks/P14-02.md) | Implement safe MySQL logical dump |
| [P14-03](../tasks/P14-03.md) | Implement archive write/verify and metadata |
| [P14-04](../tasks/P14-04.md) | Implement isolated restore verification |
| [P14-05](../tasks/P14-05.md) | Implement backup API and protected download |
| [P14-06](../tasks/P14-06.md) | Build Backup UI and job progress |
| [P14-07](../tasks/P14-07.md) | Verify backup security and restorability gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent units. The **complete authoritative list** includes microtasks below; always use `python3 tools/agent_tasks.py next` for execution order.

- [P14-01](../tasks/P14-01.md)
- [P14-02A](../tasks/P14-02A.md)
- [P14-02B](../tasks/P14-02B.md)
- [P14-02](../tasks/P14-02.md)
- [P14-03](../tasks/P14-03.md)
- [P14-04](../tasks/P14-04.md)
- [P14-05](../tasks/P14-05.md)
- [P14-06](../tasks/P14-06.md)
- [P14-07](../tasks/P14-07.md)
