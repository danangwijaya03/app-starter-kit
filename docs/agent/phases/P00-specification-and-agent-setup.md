# P00 — Specification and agent onboarding

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
All documents and task graph valid; existing Next.js scaffold preserved.

## Instructions for low-reasoning agent
1. Run `.venv-agent/bin/python tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P00-01](../tasks/P00-01.md) | Verify specification decisions |
| [P00-02](../tasks/P00-02.md) | Initialize documentation and link index |
| [P00-03](../tasks/P00-03.md) | Install agent instructions and nested scope rules |
| [P00-04](../tasks/P00-04.md) | Initialize task registry and checkpoint tooling |
| [P00-05](../tasks/P00-05.md) | Document architecture decisions and starter baseline |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains the full list below, including microtasks.** Always select the next ready task with `.venv-agent/bin/python tools/agent_tasks.py next`, not by visual order in this guide.

- [P00-01](../tasks/P00-01.md)
- [P00-02](../tasks/P00-02.md)
- [P00-03](../tasks/P00-03.md)
- [P00-04](../tasks/P00-04.md)
- [P00-05](../tasks/P00-05.md)
