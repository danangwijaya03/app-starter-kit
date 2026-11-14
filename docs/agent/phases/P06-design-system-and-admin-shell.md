# P06 — Authorized Admin UI Shell

**Ditujukan untuk: CODING AGENT.** This phase is a planned implementation, not evidence of completed functionality. **Provider/model agnostic:** use the active coding agent available (Codex/Claude Code/Antigravity/DeepSeek/etc.); risk gate is independent of model name.

## Reviewable outcome

Replace static fixture with authenticated, permission-aware responsive shell. A demo/fixture is labelled as such; do not claim a working API, RBAC or DB because a static page renders.

## Implementation flow

1. `python3 tools/bootstrap_agent.py`, check `git status --short`, `docs/agent/CHECKPOINT.md` and next ready task.
2. Read one task card and [Reference Map](../../references/REFERENCE-MAP.md); follow the [Adoption Protocol](../../references/ADOPTION-PROTOCOL.md) and focused playbook [UI-FORMS](../../references/UI-FORMS.md).
3. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
4. Follow the exact `depends_on` graph from TASKS.yaml rather than assuming list order is executable.
5. On security-sensitive work, run appropriate positive, negative and concurrency/recovery tests; an **independent qualified reviewer** must approve effective high-risk tasks, regardless of the implementer's model/provider. Production changes require separate operator approval.
6. Record actual source/test evidence, the verified preview route (or unavailable), feature mode and next task. Do not deploy automatically. All work targets clone-based setup; no installer, feature generator or Docker dependency.

## Tasks in this phase (9)

| ID | Work unit |
|---|---|
| [P06-01](../tasks/P06-01.md) | Implement Salt & Pepper semantic tokens |
| [P06-02A](../tasks/P06-02A.md) | Install and configure shadcn base components |
| [P06-02B](../tasks/P06-02B.md) | Integrate limited Aceternity components |
| [P06-02](../tasks/P06-02.md) | Set up shadcn UI, Aceternity and shared components |
| [P06-03](../tasks/P06-03.md) | Implement responsive admin shell |
| [P06-04](../tasks/P06-04.md) | Integrate dynamic navigation with RBAC |
| [P06-05](../tasks/P06-05.md) | Implement reusable table/form/dialog patterns |
| [P06-06](../tasks/P06-06.md) | Add theme mode and reduced motion handling |
| [P06-07](../tasks/P06-07.md) | Verify UI/admin shell quality gate |

## Gate before advancing

Every task in the phase must have current-source scoped test evidence, meet the reviewable outcome, and pass any independent high-risk review required by `agent_tasks.py`. Tests on disposable databases only. Do not claim documentation validation proves the runtime is implemented.

## Recovery

Inspect Git diff, current task/evidence and real DB migration state before resuming. Never blindly repeat bootstrap, migrations or restore. Manual clone/setup reference: [Manual Clone Setup](../../MANUAL-CLONE-SETUP.md).
