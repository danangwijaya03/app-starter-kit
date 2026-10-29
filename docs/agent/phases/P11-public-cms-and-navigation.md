# P11 — Public CMS and navigation

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Public page renderer, SEO and menu invalidation pass tests.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P11-01](../tasks/P11-01.md) | Implement public published-only page service |
| [P11-02](../tasks/P11-02.md) | Implement Next.js public block renderer |
| [P11-03](../tasks/P11-03.md) | Implement navigation menus API with tree validation |
| [P11-04](../tasks/P11-04.md) | Implement public navigation and admin editor |
| [P11-05](../tasks/P11-05.md) | Implement secure preview and draft mode |
| [P11-06](../tasks/P11-06.md) | Implement SEO, sitemap and cache revalidation |
| [P11-07](../tasks/P11-07.md) | Verify public CMS gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.

## Complete task index from TASKS.yaml

The table above may summarize parent work units. **The authoritative task registry contains all units below, including microtasks.** Select next with `python3 tools/agent_tasks.py next`.

- [P11-01](../tasks/P11-01.md)
- [P11-02](../tasks/P11-02.md)
- [P11-03](../tasks/P11-03.md)
- [P11-04](../tasks/P11-04.md)
- [P11-05](../tasks/P11-05.md)
- [P11-06](../tasks/P11-06.md)
- [P11-07](../tasks/P11-07.md)
