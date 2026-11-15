# P09 — Media Module

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

Optional safe LocalFs media, public/private delivery and deletion protection. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** media.

The **Core release checkpoint P16-11** is cross-phase and does not wait for the optional Media/CMS/Jobs/Operations modules. The **module certification checkpoint P16-12** is separate. Phase ID does not mean the task must wait for all preceding phase numbers.

## Agent procedure

1. Run `python3 tools/bootstrap_agent.py`, inspect `git status`, `docs/agent/CHECKPOINT.md`, `.venv-agent/bin/python tools/agent_tasks.py next`.
2. Read one card, relevant `spec_refs`, [Reference Adoption Protocol](../../references/ADOPTION-PROTOCOL.md), and real source. Do not research every upstream repo or assume example source is trusted.
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
4. Test the last modified source against disposable database/storage with positive/negative assertions. For Core, verify module-disabled behavior; for optional modules, verify enablement dependencies and correct 404/permission behavior. No secrets or production mutations.
5. For effective high-risk tasks, an independently qualified reviewer must sign off before technical completion. This is **not** a mandate to use a specific model or High Reasoning effort level.
6. Record actual preview URL/mode or diagnostic (not verified if inaccessible), test evidence, reference URL/license and checkpoint.

## Tasks (7)

| ID | Delivery track | Planned work |
|---|---|---|
| [P09-01](../tasks/P09-01.md) | media | Define storage interface and filesystem adapter |
| [P09-02](../tasks/P09-02.md) | media | Implement media validation and temp upload pipeline |
| [P09-03](../tasks/P09-03.md) | media | Implement media metadata and usage repository |
| [P09-04](../tasks/P09-04.md) | media | Implement media CRUD and protected delivery API |
| [P09-05](../tasks/P09-05.md) | media | Build Media Library and file picker UI |
| [P09-06](../tasks/P09-06.md) | media | Add thumbnail/orphan reconciliation path |
| [P09-07](../tasks/P09-07.md) | media | Verify media security and persistence gate |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
