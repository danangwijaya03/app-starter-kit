# P10 — CMS editor and revisions

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Immutable draft revisions and atomic publish behavior verified.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P10-01](../tasks/P10-01.md) | Define typed CMS block schema and registry |
| [P10-02](../tasks/P10-02.md) | Implement CMS page/revision repository |
| [P10-03](../tasks/P10-03.md) | Implement CMS Pages CRUD and paginated routes |
| [P10-04](../tasks/P10-04.md) | Implement rich text Tiptap client editor |
| [P10-05A](../tasks/P10-05A.md) | Create block palette and add/remove actions |
| [P10-05B](../tasks/P10-05B.md) | Create properties panel with validated writes |
| [P10-05C](../tasks/P10-05C.md) | Create reorder and responsive canvas |
| [P10-05](../tasks/P10-05.md) | Implement block canvas and properties editor |
| [P10-06](../tasks/P10-06.md) | Implement revision save and conflicts |
| [P10-07](../tasks/P10-07.md) | Implement publish/unpublish transactions |
| [P10-08](../tasks/P10-08.md) | Implement revision restore as new draft |
| [P10-09](../tasks/P10-09.md) | Verify CMS editor/revision gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.
