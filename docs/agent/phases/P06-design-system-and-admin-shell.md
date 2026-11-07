# P06 — Design system and admin shell

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Incremental preview checkpoint and agent reasoning

Upgrade early Salt & Pepper shell from demo to authenticated role-aware UI; remove fixture labels only for real features.

At each safe increment run **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. For UI tasks record fixture/integrated/diagnostic mode, actual URL only if verified, test evidence and user review state via [preview/feedback](../PREVIEW-AND-FEEDBACK.md) and [review queue](../REVIEW-QUEUE.md). Low reasoning may implement bounded work; [Agent Routing](../AGENT-ROUTING.md) identifies critical work recommended for High reasoning and any required independent review. User UI review is non-blocking for other safe ready tasks.

## Gate before advancing
Admin shell renders four menu groups with RBAC filtered navigation and Salt & Pepper tokens.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P06-01](../tasks/P06-01.md) | Implement Salt & Pepper semantic tokens |
| [P06-02A](../tasks/P06-02A.md) | Install and configure shadcn base components |
| [P06-02B](../tasks/P06-02B.md) | Integrate limited Aceternity components |
| [P06-02](../tasks/P06-02.md) | Set up shadcn UI, Aceternity and shared components |
| [P06-03](../tasks/P06-03.md) | Implement responsive admin shell |
| [P06-04](../tasks/P06-04.md) | Integrate dynamic navigation with RBAC |
| [P06-05](../tasks/P06-05.md) | Implement reusable table/form/dialog patterns |
| [P06-06](../tasks/P06-06.md) | Add theme mode and reduced motion handling |
| [P06-07](../tasks/P06-07.md) | Verify UI/admin shell quality gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains the full list below, including microtasks.** Always select the next ready task with `python3 tools/agent_tasks.py next`, not by visual order in this guide.

- [P06-01](../tasks/P06-01.md)
- [P06-02A](../tasks/P06-02A.md)
- [P06-02B](../tasks/P06-02B.md)
- [P06-02](../tasks/P06-02.md)
- [P06-03](../tasks/P06-03.md)
- [P06-04](../tasks/P06-04.md)
- [P06-05](../tasks/P06-05.md)
- [P06-06](../tasks/P06-06.md)
- [P06-07](../tasks/P06-07.md)
