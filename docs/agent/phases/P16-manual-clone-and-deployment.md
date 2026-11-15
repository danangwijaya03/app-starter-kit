# P16 — Manual Deploy and Certifications

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

P16-11 Core release without Redis/Media/CMS; P16-12 optional module matrix after Core. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** mixed.

The **Core release checkpoint P16-11** is cross-phase and does not wait for the optional Media/CMS/Jobs/Operations modules. The **module certification checkpoint P16-12** is separate. Phase ID does not mean the task must wait for all preceding phase numbers.

## Agent procedure

1. Run `python3 tools/bootstrap_agent.py`, inspect `git status`, `docs/agent/CHECKPOINT.md`, `.venv-agent/bin/python tools/agent_tasks.py next`.
2. Read one card, relevant `spec_refs`, [Reference Adoption Protocol](../../references/ADOPTION-PROTOCOL.md), and real source. Do not research every upstream repo or assume example source is trusted.
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
4. Test the last modified source against disposable database/storage with positive/negative assertions. For Core, verify module-disabled behavior; for optional modules, verify enablement dependencies and correct 404/permission behavior. No secrets or production mutations.
5. For effective high-risk tasks, an independently qualified reviewer must sign off before technical completion. This is **not** a mandate to use a specific model or High Reasoning effort level.
6. Record actual preview URL/mode or diagnostic (not verified if inaccessible), test evidence, reference URL/license and checkpoint.

## Tasks (21)

| ID | Delivery track | Planned work |
|---|---|---|
| [P16-01](../tasks/P16-01.md) | core | Document manual production runtime prerequisites |
| [P16-02A](../tasks/P16-02A.md) | core | Validate web production build from source |
| [P16-02B](../tasks/P16-02B.md) | core | Validate Hono API production build from source |
| [P16-02C](../tasks/P16-02C.md) | jobs | Validate conditional BullMQ worker build for jobs-enabled modules |
| [P16-02](../tasks/P16-02.md) | core | Integrate Core web+API and conditional worker npm build |
| [P16-03](../tasks/P16-03.md) | core | Create read-only manual production environment preflight |
| [P16-04A](../tasks/P16-04A.md) | core | Implement guarded manual Drizzle migration npm scripts |
| [P16-04B](../tasks/P16-04B.md) | core | Implement idempotent manual permission sync and seed |
| [P16-04C](../tasks/P16-04C.md) | core | Wire secure manual admin bootstrap npm command |
| [P16-04D](../tasks/P16-04D.md) | core | Implement read-only manual setup verification |
| [P16-04](../tasks/P16-04.md) | core | Gate manual npm setup commands on disposable clone |
| [P16-05](../tasks/P16-05.md) | core | Configure Core PM2 web/API and optional worker |
| [P16-06](../tasks/P16-06.md) | core | Verify aaPanel Nginx HTTPS same-origin proxy |
| [P16-07](../tasks/P16-07.md) | core | Rehearse manual Git update build and restart |
| [P16-08](../tasks/P16-08.md) | core | Document manual source rollback and database recovery |
| [P16-09A](../tasks/P16-09A.md) | core | Validate developer clone and npm script guide |
| [P16-09B](../tasks/P16-09B.md) | core | Validate manual aaPanel server documentation |
| [P16-09](../tasks/P16-09.md) | core | Gate manual user and operator documentation |
| [P16-10](../tasks/P16-10.md) | core | Verify new clone isolation without project initializer |
| [P16-11](../tasks/P16-11.md) | core-release | Certify Core-only production release gate |
| [P16-12](../tasks/P16-12.md) | full-matrix | Certify optional module matrix independently of Core release |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
