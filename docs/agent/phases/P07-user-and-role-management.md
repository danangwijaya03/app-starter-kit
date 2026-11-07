# P07 — User and role management

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Incremental preview checkpoint and agent reasoning

Real user/role CRUD via typed API/MySQL and denied access cases. Medium reasoning for routine CRUD; High for authorization or concurrent role changes.

At each safe increment run **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. For UI tasks record fixture/integrated/diagnostic mode, actual URL only if verified, test evidence and user review state via [preview/feedback](../PREVIEW-AND-FEEDBACK.md) and [review queue](../REVIEW-QUEUE.md). Low reasoning may implement bounded work; [Agent Routing](../AGENT-ROUTING.md) identifies critical work recommended for High reasoning and any required independent review. User UI review is non-blocking for other safe ready tasks.

## Gate before advancing
User CRUD and permissions editor endpoints/forms pass scoped tests.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P07-01](../tasks/P07-01.md) | Implement user list and detail APIs |
| [P07-02](../tasks/P07-02.md) | Implement invitation and user updates |
| [P07-03](../tasks/P07-03.md) | Implement roles CRUD and policy APIs |
| [P07-04](../tasks/P07-04.md) | Build Users management UI |
| [P07-05](../tasks/P07-05.md) | Build Roles and grouped permissions editor |
| [P07-06](../tasks/P07-06.md) | Integrate multi-role assignment and audit |
| [P07-07](../tasks/P07-07.md) | Verify user and role management gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains the full list below, including microtasks.** Always select the next ready task with `python3 tools/agent_tasks.py next`, not by visual order in this guide.

- [P07-01](../tasks/P07-01.md)
- [P07-02](../tasks/P07-02.md)
- [P07-03](../tasks/P07-03.md)
- [P07-04](../tasks/P07-04.md)
- [P07-05](../tasks/P07-05.md)
- [P07-06](../tasks/P07-06.md)
- [P07-07](../tasks/P07-07.md)
