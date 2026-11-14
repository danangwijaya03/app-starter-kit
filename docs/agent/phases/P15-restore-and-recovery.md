# P15 — Controlled Restore

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Staged restore/recovery, journal, explicit maintenance and manual approval. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [OPERATIONS](../../references/OPERATIONS.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (10)

| ID | Work unit |
|---|---|
| [P15-01](../tasks/P15-01.md) | Define restore workflow, policy and approval gates |
| [P15-02](../tasks/P15-02.md) | Implement restoration archive preflight |
| [P15-03](../tasks/P15-03.md) | Implement isolated staging restore and comparison |
| [P15-04](../tasks/P15-04.md) | Implement external journal and pre-restore backup |
| [P15-05A](../tasks/P15-05A.md) | Implement maintenance mode and queue draining |
| [P15-05B](../tasks/P15-05B.md) | Implement controlled import stage |
| [P15-05C](../tasks/P15-05C.md) | Implement restore failure hold and response |
| [P15-05](../tasks/P15-05.md) | Implement maintenance/drain/import orchestration |
| [P15-06](../tasks/P15-06.md) | Implement post-restore reconciliation and runbook |
| [P15-07](../tasks/P15-07.md) | Verify restore chaos and rollback gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
