# P14 — Encrypted Backup

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Verified backup, checksum, permissions and isolated restore validation. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [OPERATIONS](../../references/OPERATIONS.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (9)

| ID | Work unit |
|---|---|
| [P14-01](../tasks/P14-01.md) | Implement backup manifest and encryption interface |
| [P14-02A](../tasks/P14-02A.md) | Prepare safe mysqldump command builder |
| [P14-02B](../tasks/P14-02B.md) | Implement dump streaming and cancellation |
| [P14-02](../tasks/P14-02.md) | Implement safe MySQL logical dump |
| [P14-03](../tasks/P14-03.md) | Implement archive write/verify and metadata |
| [P14-04](../tasks/P14-04.md) | Implement isolated restore verification |
| [P14-05](../tasks/P14-05.md) | Implement backup API and protected download |
| [P14-06](../tasks/P14-06.md) | Build Backup UI and job progress |
| [P14-07](../tasks/P14-07.md) | Verify backup security and restorability gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
