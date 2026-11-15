# P10 — CMS Editor

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

Optional CMS after Media, immutable revisions and idempotent save. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** cms.

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
| [P10-01](../tasks/P10-01.md) | cms | Define typed CMS block schema and registry |
| [P10-02](../tasks/P10-02.md) | cms | Implement CMS page/revision repository |
| [P10-03](../tasks/P10-03.md) | cms | Implement CMS Pages CRUD and paginated routes |
| [P10-04](../tasks/P10-04.md) | cms | Implement rich text Tiptap client editor |
| [P10-05A](../tasks/P10-05A.md) | cms | Create block palette and add/remove actions |
| [P10-05B](../tasks/P10-05B.md) | cms | Create properties panel with validated writes |
| [P10-05C](../tasks/P10-05C.md) | cms | Create reorder and responsive canvas |
| [P10-05](../tasks/P10-05.md) | cms | Implement block canvas and properties editor |
| [P10-06](../tasks/P10-06.md) | cms | Implement revision save and conflicts |
| [P10-07](../tasks/P10-07.md) | cms | Implement publish/unpublish transactions |
| [P10-08](../tasks/P10-08.md) | cms | Implement revision restore as new draft |
| [P10-09](../tasks/P10-09.md) | cms | Verify CMS editor/revision gate |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
