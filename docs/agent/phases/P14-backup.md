# P14 — Independent Backup & Operations UI

**Status:** planned implementation; no feature is complete based on architecture documentation alone. Coding-agent/provider neutral; one bounded task at a time.

## Accepted v2 outcome

P14-01..04 and P14-08 independent offsite backup for Core; P14-05..07 optional Operations UI. Review [Architecture v2 index](../../architecture/README.md), [ADR register](../../architecture/ADR/README.md), [v2 Reference Index](../../references/INDEX-V2.md) and the specific contract attached to the task. **Track:** mixed.

The **Core release checkpoint P16-11** is cross-phase and does not wait for the optional Media/CMS/Jobs/Operations modules. The **module certification checkpoint P16-12** is separate. Phase ID does not mean the task must wait for all preceding phase numbers.

## Agent procedure

1. Run `python3 tools/bootstrap_agent.py`, inspect `git status`, `docs/agent/CHECKPOINT.md`, `.venv-agent/bin/python tools/agent_tasks.py next`.
2. Read one card, relevant `spec_refs`, [Reference Adoption Protocol](../../references/ADOPTION-PROTOCOL.md), and real source. Do not research every upstream repo or assume example source is trusted.
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
4. Test the last modified source against disposable database/storage with positive/negative assertions. For Core, verify module-disabled behavior; for optional modules, verify enablement dependencies and correct 404/permission behavior. No secrets or production mutations.
5. For effective high-risk tasks, an independently qualified reviewer must sign off before technical completion. This is **not** a mandate to use a specific model or High Reasoning effort level.
6. Record actual preview URL/mode or diagnostic (not verified if inaccessible), test evidence, reference URL/license and checkpoint.

## Tasks (10)

| ID | Delivery track | Planned work |
|---|---|---|
| [P14-01](../tasks/P14-01.md) | core | Define independent encrypted offsite backup and recovery contract |
| [P14-02A](../tasks/P14-02A.md) | core | Prepare safe independent mysqldump command builder |
| [P14-02B](../tasks/P14-02B.md) | core | Stream and cancel independent backup CLI dump |
| [P14-02](../tasks/P14-02.md) | core | Integrate independent MySQL logical dump CLI |
| [P14-03](../tasks/P14-03.md) | core | Encrypt and verify offsite backup manifest |
| [P14-04](../tasks/P14-04.md) | core | Verify independent staging recovery from encrypted offsite backup |
| [P14-05](../tasks/P14-05.md) | operations | Optional Operations backup metadata API |
| [P14-06](../tasks/P14-06.md) | operations | Optional Operations backup status and verification UI |
| [P14-07](../tasks/P14-07.md) | operations | Certify optional Operations backup UI and protected metadata |
| [P14-08](../tasks/P14-08.md) | core | Certify Core independent offsite backup and staging restore |

## Phase gate

All phase tasks require real source tests, acceptance and any relevant independent review. **Do not treat the entire phase gate as a prerequisite for Core release when the phase contains optional tasks.** Source of truth for dependencies is `docs/agent/TASKS.yaml`; never manually bypass it. Server operations are clone/build/PM2/Nginx; worker/Redis only if the static module configuration requires background jobs.

## Recover

Review current task, source diff and migration history before retry. Do not repeat seed/bootstrap/restore blindly.
