# P16 — Non-Docker build artifacts and server release

> This phase is an implementation target; it is **not** completed by this documentation commit.

## Gate before advancing
Offline artifact boot without source workspace, aaPanel README, update/rollback and full regression verified.

## Instructions for low-reasoning agent
1. Run `python3 tools/agent_tasks.py doctor` then `next`; do not manually skip dependencies.
2. Read and execute **one** [task card](../tasks/) at a time. Use npm/npx only.
3. Keep scope narrow, record real test evidence, update checkpoint; stop on ambiguous or unsafe operations.
4. Run the real integration/phase test before marking phase verified. Documentation validation alone is not an implementation test.
5. Follow [Repository Baseline](../REPOSITORY-BASELINE.md) and [Implementation Contracts](../IMPLEMENTATION-CONTRACTS.md). Preserve preexisting Next.js until P01 performs Git moves.

## Tasks in this phase

| ID | Work unit |
|---|---|
| [P16-01](../tasks/P16-01.md) | Freeze release target matrix and runtime ABI |
| [P16-02A](../tasks/P16-02A.md) | Build standalone web artifact |
| [P16-02B](../tasks/P16-02B.md) | Build portable Hono API artifact |
| [P16-02C](../tasks/P16-02C.md) | Build portable BullMQ worker artifact |
| [P16-02D](../tasks/P16-02D.md) | Build portable installer artifact |
| [P16-02](../tasks/P16-02.md) | Build standalone web and portable API/worker/CLI |
| [P16-03](../tasks/P16-03.md) | Implement release layout, manifest and checksums |
| [P16-04A](../tasks/P16-04A.md) | Implement installer preflight and migrate |
| [P16-04B](../tasks/P16-04B.md) | Implement permission and system seed |
| [P16-04C](../tasks/P16-04C.md) | Wire secure bootstrap command |
| [P16-04D](../tasks/P16-04D.md) | Implement installer verify command |
| [P16-04](../tasks/P16-04.md) | Implement installer CLI migrate/seed/bootstrap/verify |
| [P16-05](../tasks/P16-05.md) | Implement PM2 ecosystem and safe env loading |
| [P16-06](../tasks/P16-06.md) | Implement aaPanel Nginx config and HTTPS guide |
| [P16-07A](../tasks/P16-07A.md) | Verify uploaded archive and extract versioned release |
| [P16-07B](../tasks/P16-07B.md) | Implement guarded current symlink switch |
| [P16-07C](../tasks/P16-07C.md) | Implement safe update orchestration |
| [P16-07](../tasks/P16-07.md) | Implement upload install/version-switch/upgrade script |
| [P16-08](../tasks/P16-08.md) | Implement rollback and recovery controls |
| [P16-09A](../tasks/P16-09A.md) | Write and verify developer README |
| [P16-09B](../tasks/P16-09B.md) | Write and verify production upload README |
| [P16-09](../tasks/P16-09.md) | Write and test developer README and server README |
| [P16-10](../tasks/P16-10.md) | Implement new-project initializer and isolation test |
| [P16-11](../tasks/P16-11.md) | Run full security and release verification |

## Recovery
Inspect `docs/agent/CHECKPOINT.md`, `git status`, and the active task before resuming. Never blindly repeat DB migrations, bootstrap, restore, or deployment.
