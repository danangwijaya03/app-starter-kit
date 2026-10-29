# P12 — Settings and appearance

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Theme/global settings persist, validators and audit views tested.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P12-01](../tasks/P12-01.md) | Define typed settings registry and service |
| [P12-02](../tasks/P12-02.md) | Implement general settings API and audit |
| [P12-03](../tasks/P12-03.md) | Build branding upload and General UI |
| [P12-04](../tasks/P12-04.md) | Implement theme configuration schema and contrast gate |
| [P12-05](../tasks/P12-05.md) | Implement Appearance UI global theme preview |
| [P12-06](../tasks/P12-06.md) | Implement audit logs query and page |
| [P12-07](../tasks/P12-07.md) | Implement runtime branding revalidation |
| [P12-08](../tasks/P12-08.md) | Verify settings/accessibility gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains all units below, including microtasks.** Select next with `python3 tools/agent_tasks.py next`.

- [P12-01](../tasks/P12-01.md)
- [P12-02](../tasks/P12-02.md)
- [P12-03](../tasks/P12-03.md)
- [P12-04](../tasks/P12-04.md)
- [P12-05](../tasks/P12-05.md)
- [P12-06](../tasks/P12-06.md)
- [P12-07](../tasks/P12-07.md)
- [P12-08](../tasks/P12-08.md)
