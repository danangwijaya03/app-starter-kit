# P05 — RBAC and Admin Bootstrap

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

One server permission engine, limited delegation and locked last-admin invariant. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** core.

The **Core release checkpoint P16-11** is cross-phase and does not wait for the optional Media/CMS/Jobs/Operations modules. The **module certification checkpoint P16-12** is separate. Phase ID does not mean the task must wait for all preceding phase numbers.

## Agent procedure

1. Run `python3 tools/bootstrap_agent.py`, inspect `git status`, `docs/agent/CHECKPOINT.md`, `.venv-agent/bin/python tools/agent_tasks.py next`.
2. Read one card, relevant `spec_refs`, [Reference Adoption Protocol](../../references/ADOPTION-PROTOCOL.md), and real source. Do not research every upstream repo or assume example source is trusted.
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
4. Test the last modified source against disposable database/storage with positive/negative assertions. For Core, verify module-disabled behavior; for optional modules, verify enablement dependencies and correct 404/permission behavior. No secrets or production mutations.
5. For effective high-risk tasks, an independently qualified reviewer must sign off before technical completion. This is **not** a mandate to use a specific model or High Reasoning effort level.
6. Record actual preview URL/mode or diagnostic (not verified if inaccessible), test evidence, reference URL/license and checkpoint.

## Tasks (13)

| ID | Delivery track | Planned work |
|---|---|---|
| [P05-01](../tasks/P05-01.md) | core | Define canonical permission manifest and validation |
| [P05-02](../tasks/P05-02.md) | core | Build permission sync check/apply commands |
| [P05-03](../tasks/P05-03.md) | core | Seed default protected roles |
| [P05-04](../tasks/P05-04.md) | core | Implement authorization service and policies |
| [P05-05](../tasks/P05-05.md) | core | Implement route permission middleware |
| [P05-06](../tasks/P05-06.md) | core | Build role assignment concurrency invariants |
| [P05-07A](../tasks/P05-07A.md) | core | Create safe bootstrap credential input |
| [P05-07B](../tasks/P05-07B.md) | core | Provision first user and assign super_admin |
| [P05-07C](../tasks/P05-07C.md) | core | Verify first login bootstrap flow |
| [P05-07](../tasks/P05-07.md) | core | Implement secure idempotent first-admin bootstrap |
| [P05-08](../tasks/P05-08.md) | core | Implement authorization invalidation and module nav registry |
| [P05-09](../tasks/P05-09.md) | core | Verify comprehensive RBAC/security gate |
| [P05-10](../tasks/P05-10.md) | core | Certify limited RBAC delegation and transactional audit |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
