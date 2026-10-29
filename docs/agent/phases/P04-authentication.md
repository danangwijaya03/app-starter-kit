# P04 — Better Auth integration

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Better Auth login/logout/session tests pass; no custom hashing.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P04-01](../tasks/P04-01.md) | Configure Better Auth MySQL adapter |
| [P04-02](../tasks/P04-02.md) | Mount auth routes in Hono and session middleware |
| [P04-03](../tasks/P04-03.md) | Implement login/logout UI and auth client |
| [P04-04](../tasks/P04-04.md) | Implement password reset and activation flow |
| [P04-05](../tasks/P04-05.md) | Enforce user status and must-change-password guard |
| [P04-06](../tasks/P04-06.md) | Implement own profile/session termination |
| [P04-07](../tasks/P04-07.md) | Complete authentication security gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains the full list below, including microtasks.** Always select the next ready task with `python3 tools/agent_tasks.py next`, not by visual order in this guide.

- [P04-01](../tasks/P04-01.md)
- [P04-02](../tasks/P04-02.md)
- [P04-03](../tasks/P04-03.md)
- [P04-04](../tasks/P04-04.md)
- [P04-05](../tasks/P04-05.md)
- [P04-06](../tasks/P04-06.md)
- [P04-07](../tasks/P04-07.md)
