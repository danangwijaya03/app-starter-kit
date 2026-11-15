# P03 — Central MySQL Database

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

Drizzle single migration journal, 21 logical tables and Better Auth-generated schema. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** core.

The **Core release checkpoint P16-11** is cross-phase and does not wait for the optional Media/CMS/Jobs/Operations modules. The **module certification checkpoint P16-12** is separate. Phase ID does not mean the task must wait for all preceding phase numbers.

## Agent procedure

1. Run `python3 tools/bootstrap_agent.py`, inspect `git status`, `docs/agent/CHECKPOINT.md`, `.venv-agent/bin/python tools/agent_tasks.py next`.
2. Read one card, relevant `spec_refs`, [Reference Adoption Protocol](../../references/ADOPTION-PROTOCOL.md), and real source. Do not research every upstream repo or assume example source is trusted.
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
4. Test the last modified source against disposable database/storage with positive/negative assertions. For Core, verify module-disabled behavior; for optional modules, verify enablement dependencies and correct 404/permission behavior. No secrets or production mutations.
5. For effective high-risk tasks, an independently qualified reviewer must sign off before technical completion. This is **not** a mandate to use a specific model or High Reasoning effort level.
6. Record actual preview URL/mode or diagnostic (not verified if inaccessible), test evidence, reference URL/license and checkpoint.

## Tasks (12)

| ID | Delivery track | Planned work |
|---|---|---|
| [P03-01](../tasks/P03-01.md) | core | Generate Better Auth Drizzle MySQL schema |
| [P03-02](../tasks/P03-02.md) | core | Define app user profile and RBAC tables |
| [P03-03A](../tasks/P03-03A.md) | core | Define CMS pages and revisions schema |
| [P03-03B](../tasks/P03-03B.md) | core | Define CMS menus and menu items schema |
| [P03-03](../tasks/P03-03.md) | core | Add CMS pages/revisions and navigation schema |
| [P03-04](../tasks/P03-04.md) | core | Add media, settings and user preferences schema |
| [P03-05](../tasks/P03-05.md) | core | Add audit, system jobs and backup tables |
| [P03-06](../tasks/P03-06.md) | core | Generate and review migration history |
| [P03-07](../tasks/P03-07.md) | core | Build transaction helper and repository abstractions |
| [P03-08](../tasks/P03-08.md) | core | Implement audit event service and seed base |
| [P03-09](../tasks/P03-09.md) | core | Connect safe DB readiness to development health diagnostic |
| [P03-10](../tasks/P03-10.md) | core | Verify centralized MySQL migrations and v2 schema deltas |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
