# P03 — Database schemas and migrations

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Migration applies on clean disposable MySQL and referential constraints validated.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P03-01](../tasks/P03-01.md) | Generate Better Auth Drizzle MySQL schema |
| [P03-02](../tasks/P03-02.md) | Define app user profile and RBAC tables |
| [P03-03A](../tasks/P03-03A.md) | Define CMS pages and revisions schema |
| [P03-03B](../tasks/P03-03B.md) | Define CMS menus and menu items schema |
| [P03-03](../tasks/P03-03.md) | Add CMS pages/revisions and navigation schema |
| [P03-04](../tasks/P03-04.md) | Add media, settings and user preferences schema |
| [P03-05](../tasks/P03-05.md) | Add audit, system jobs and backup tables |
| [P03-06](../tasks/P03-06.md) | Generate and review migration history |
| [P03-07](../tasks/P03-07.md) | Build transaction helper and repository abstractions |
| [P03-08](../tasks/P03-08.md) | Implement audit event service and seed base |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains the full list below, including microtasks.** Always select the next ready task with `python3 tools/agent_tasks.py next`, not by visual order in this guide.

- [P03-01](../tasks/P03-01.md)
- [P03-02](../tasks/P03-02.md)
- [P03-03A](../tasks/P03-03A.md)
- [P03-03B](../tasks/P03-03B.md)
- [P03-03](../tasks/P03-03.md)
- [P03-04](../tasks/P03-04.md)
- [P03-05](../tasks/P03-05.md)
- [P03-06](../tasks/P03-06.md)
- [P03-07](../tasks/P03-07.md)
- [P03-08](../tasks/P03-08.md)
