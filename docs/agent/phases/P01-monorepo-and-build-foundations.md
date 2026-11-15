# P01 — npm Monorepo Foundations

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

Keep existing Next scaffold, add Next+Hono with worker scaffold optional; static modules config. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** core.

The **Core release checkpoint P16-11** is cross-phase and does not wait for the optional Media/CMS/Jobs/Operations modules. The **module certification checkpoint P16-12** is separate. Phase ID does not mean the task must wait for all preceding phase numbers.

## Agent procedure

1. Run `python3 tools/bootstrap_agent.py`, inspect `git status`, `docs/agent/CHECKPOINT.md`, `.venv-agent/bin/python tools/agent_tasks.py next`.
2. Read one card, relevant `spec_refs`, [Reference Adoption Protocol](../../references/ADOPTION-PROTOCOL.md), and real source. Do not research every upstream repo or assume example source is trusted.
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
4. Test the last modified source against disposable database/storage with positive/negative assertions. For Core, verify module-disabled behavior; for optional modules, verify enablement dependencies and correct 404/permission behavior. No secrets or production mutations.
5. For effective high-risk tasks, an independently qualified reviewer must sign off before technical completion. This is **not** a mandate to use a specific model or High Reasoning effort level.
6. Record actual preview URL/mode or diagnostic (not verified if inaccessible), test evidence, reference URL/license and checkpoint.

## Tasks (15)

| ID | Delivery track | Planned work |
|---|---|---|
| [P01-01A](../tasks/P01-01A.md) | core | Prepare npm workspace root from existing Next.js project |
| [P01-01B](../tasks/P01-01B.md) | core | Create three application package identities |
| [P01-01C](../tasks/P01-01C.md) | core | Create shared package identities |
| [P01-01](../tasks/P01-01.md) | core | Create npm workspace and package identities |
| [P01-02](../tasks/P01-02.md) | core | Pin Node, npm and TypeScript strict configuration |
| [P01-03](../tasks/P01-03.md) | core | Define Turborepo task graph and package exports |
| [P01-04A](../tasks/P01-04A.md) | core | Relocate existing root Next.js into apps/web |
| [P01-04B](../tasks/P01-04B.md) | core | Create minimal Hono API runtime |
| [P01-04C](../tasks/P01-04C.md) | core | Create minimal BullMQ worker runtime |
| [P01-04](../tasks/P01-04.md) | core | Scaffold independent Next.js, Hono and worker entrypoints |
| [P01-08](../tasks/P01-08.md) | core | Deliver early Salt & Pepper shell as explicit UI fixture |
| [P01-06](../tasks/P01-06.md) | core | Verify web API worker dev build targets |
| [P01-07](../tasks/P01-07.md) | core | Create CI checks and secret scanning baseline |
| [P01-09](../tasks/P01-09.md) | core | Add repeatable development preview smoke and review handoff |
| [P01-10](../tasks/P01-10.md) | core | Define static module catalog and cross-runtime validation |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
