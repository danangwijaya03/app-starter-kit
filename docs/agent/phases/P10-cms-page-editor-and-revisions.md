# P10 — CMS Editor & Revisions

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Drafts, immutable revisions, typed blocks, publish with conflicts handled. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [CMS](../../references/CMS.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (12)

| ID | Work unit |
|---|---|
| [P10-01](../tasks/P10-01.md) | Define typed CMS block schema and registry |
| [P10-02](../tasks/P10-02.md) | Implement CMS page/revision repository |
| [P10-03](../tasks/P10-03.md) | Implement CMS Pages CRUD and paginated routes |
| [P10-04](../tasks/P10-04.md) | Implement rich text Tiptap client editor |
| [P10-05A](../tasks/P10-05A.md) | Create block palette and add/remove actions |
| [P10-05B](../tasks/P10-05B.md) | Create properties panel with validated writes |
| [P10-05C](../tasks/P10-05C.md) | Create reorder and responsive canvas |
| [P10-05](../tasks/P10-05.md) | Implement block canvas and properties editor |
| [P10-06](../tasks/P10-06.md) | Implement revision save and conflicts |
| [P10-07](../tasks/P10-07.md) | Implement publish/unpublish transactions |
| [P10-08](../tasks/P10-08.md) | Implement revision restore as new draft |
| [P10-09](../tasks/P10-09.md) | Verify CMS editor/revision gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
