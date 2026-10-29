# P05 — RBAC and bootstrap administrator

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
RBAC denies unauthorized requests; last active super admin protected; bootstrap idempotent.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P05-01](../tasks/P05-01.md) | Define canonical permission manifest and validation |
| [P05-02](../tasks/P05-02.md) | Build permission sync check/apply commands |
| [P05-03](../tasks/P05-03.md) | Seed default protected roles |
| [P05-04](../tasks/P05-04.md) | Implement authorization service and policies |
| [P05-05](../tasks/P05-05.md) | Implement route permission middleware |
| [P05-06](../tasks/P05-06.md) | Build role assignment concurrency invariants |
| [P05-07A](../tasks/P05-07A.md) | Create safe bootstrap credential input |
| [P05-07B](../tasks/P05-07B.md) | Provision first user and assign super_admin |
| [P05-07C](../tasks/P05-07C.md) | Verify first login bootstrap flow |
| [P05-07](../tasks/P05-07.md) | Implement secure idempotent first-admin bootstrap |
| [P05-08](../tasks/P05-08.md) | Implement authorization invalidation and module nav registry |
| [P05-09](../tasks/P05-09.md) | Verify comprehensive RBAC/security gate |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.
