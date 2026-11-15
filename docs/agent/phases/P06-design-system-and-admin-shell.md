# P06 — Admin Design System

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

Authorized UI shell and semantic tokens. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** core.

The **Core release checkpoint P16-11** is cross-phase and does not wait for the optional Media/CMS/Jobs/Operations modules. The **module certification checkpoint P16-12** is separate. Phase ID does not mean the task must wait for all preceding phase numbers.

## Agent procedure

1. Run `python3 tools/bootstrap_agent.py`, inspect `git status`, `docs/agent/CHECKPOINT.md`, `.venv-agent/bin/python tools/agent_tasks.py next`.
2. Read one card, relevant `spec_refs`, [Reference Adoption Protocol](../../references/ADOPTION-PROTOCOL.md), and real source. Do not research every upstream repo or assume example source is trusted.
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
4. Test the last modified source against disposable database/storage with positive/negative assertions. For Core, verify module-disabled behavior; for optional modules, verify enablement dependencies and correct 404/permission behavior. No secrets or production mutations.
5. For effective high-risk tasks, an independently qualified reviewer must sign off before technical completion. This is **not** a mandate to use a specific model or High Reasoning effort level.
6. Record actual preview URL/mode or diagnostic (not verified if inaccessible), test evidence, reference URL/license and checkpoint.

## Tasks (9)

| ID | Delivery track | Planned work |
|---|---|---|
| [P06-01](../tasks/P06-01.md) | core | Implement Salt & Pepper semantic tokens |
| [P06-02A](../tasks/P06-02A.md) | core | Install and configure shadcn base components |
| [P06-02B](../tasks/P06-02B.md) | core | Integrate limited Aceternity components |
| [P06-02](../tasks/P06-02.md) | core | Set up shadcn UI, Aceternity and shared components |
| [P06-03](../tasks/P06-03.md) | core | Implement responsive admin shell |
| [P06-04](../tasks/P06-04.md) | core | Integrate dynamic navigation with RBAC |
| [P06-05](../tasks/P06-05.md) | core | Implement reusable table/form/dialog patterns |
| [P06-06](../tasks/P06-06.md) | core | Add theme mode and reduced motion handling |
| [P06-07](../tasks/P06-07.md) | core | Verify UI/admin shell quality gate |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
