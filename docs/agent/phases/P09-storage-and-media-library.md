# P09 — Media storage and uploads

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Incremental preview checkpoint and agent reasoning

Media review must exercise real upload/list/remove, persistence, MIME verification and private access; High reasoning for authorization/storage trust boundaries.

At each safe increment run **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. For UI tasks record fixture/integrated/diagnostic mode, actual URL only if verified, test evidence and user review state via [preview/feedback](../PREVIEW-AND-FEEDBACK.md) and [review queue](../REVIEW-QUEUE.md). Low reasoning may implement bounded work; [Agent Routing](../AGENT-ROUTING.md) identifies critical work recommended for High reasoning and any required independent review. User UI review is non-blocking for other safe ready tasks.

## Gate before advancing
Upload/download/usage constraints and traversal prevention pass tests.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P09-01](../tasks/P09-01.md) | Define storage interface and filesystem adapter |
| [P09-02](../tasks/P09-02.md) | Implement media validation and temp upload pipeline |
| [P09-03](../tasks/P09-03.md) | Implement media metadata and usage repository |
| [P09-04](../tasks/P09-04.md) | Implement media CRUD and protected delivery API |
| [P09-05](../tasks/P09-05.md) | Build Media Library and file picker UI |
| [P09-06](../tasks/P09-06.md) | Add thumbnail/orphan reconciliation path |
| [P09-07](../tasks/P09-07.md) | Verify media security and persistence gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains all units below, including microtasks.** Select next with `python3 tools/agent_tasks.py next`.

- [P09-01](../tasks/P09-01.md)
- [P09-02](../tasks/P09-02.md)
- [P09-03](../tasks/P09-03.md)
- [P09-04](../tasks/P09-04.md)
- [P09-05](../tasks/P09-05.md)
- [P09-06](../tasks/P09-06.md)
- [P09-07](../tasks/P09-07.md)
