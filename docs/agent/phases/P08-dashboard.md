# P08 — Dashboard

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Dashboard displays allowed widgets and correct empty/error state.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P08-01](../tasks/P08-01.md) | Define dashboard widget registry and contracts |
| [P08-02](../tasks/P08-02.md) | Implement permission-scoped dashboard APIs |
| [P08-03](../tasks/P08-03.md) | Build dashboard responsive widgets |
| [P08-04](../tasks/P08-04.md) | Add widget composition and error isolation |
| [P08-05](../tasks/P08-05.md) | Verify dashboard permission gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.
