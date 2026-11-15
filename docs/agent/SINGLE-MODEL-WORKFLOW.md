# Single Active Coding Agent Workflow — Architecture v2, provider/model agnostic

**Audience: CODING AGENT / DEVELOPER.** The architecture and task system **do not depend on a model or provider**. The active coding agent may be Codex, Claude Code, Google Antigravity, DeepSeek, or another compatible tool. Use **one implementation agent/model per bounded task or session**, and allow switching between tasks/sessions after checkpoint. A model's branding or reasoning-effort tier must never be a prerequisite to do a task.

**Separate risk from model selection:** effective risk means how critical the feature is, not the class of AI model required. Technical tests and independent qualified review for high-risk changes remain mandatory.

## Single-task loop

RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.

1. Run `python3 tools/bootstrap_agent.py`, inspect Git status, CHECKPOINT, and select a ready task from `agent_tasks.py next`.
2. Read exactly one task and its `spec_refs`, plus one relevant domain document from `docs/references/` (prefer official libraries; at most one comparison starter).
3. Pin upstream URL/commit/version and verify license before copying third-party source. Adapt PostgreSQL/pnpm/multi-tenancy/Docker assumptions to MySQL/npm/single-tenant.
4. Work one bounded responsibility; split oversized pending tasks through the reviewed procedure.
5. Run real scoped lint/unit/integration/negative tests after final change, including concurrency or recovery when the modified behavior requires it.
6. Verify behavior against API, DB and authorization; preview real route when possible and mark fixture/integrated/diagnostic honestly.
7. If effective risk is `high`, **another qualified person or independent reviewer/agent** reviews diff, test assertions and security invariants before task is marked complete. A High Reasoning AI model is not mandatory, and a second session from the same implementer is not automatically independent.
8. Record evidence/review queue/checkpoint/commit and continue another independent ready task during the active session. Never promise asynchronous work.

## Mandatory evidence by domain

| Domain | Implementer | Required verification |
|---|---|---|
| UI/docs/components | Any selected coding agent | Scoped lint/build/unit and visual preview |
| CRUD and API | Any selected coding agent | Positive/invalid paths, server authorization |
| Auth/RBAC, migration, CMS private preview, media, backup/restore | Any selected coding agent | Positive/negative plus MySQL race/recovery when relevant **and independent security review** |
| Production deployment/destructive operation | Any selected coding agent can prepare and test scripts | Separate explicit operator approval **in addition** to independent code review |

Do not downgrade `agent_tasks.py` risk classification or fabricate review evidence. When a reviewer is unavailable, keep the high-risk task blocked and continue safe tasks whose dependencies are satisfied.

## Reference adoption checkpoint

```text
Task ID:
Active agent/provider (optional operational metadata, not a requirement):
Upstream URL + pinned version/commit:
Verified license and actual source adaptation:
Excluded incompatible assumptions:
Security and business invariants:
Tests executed and exit codes:
Preview URL/mode (if observed):
Independent reviewer status (if high risk):
Git commit/checkpoint / next safe task:
```

## Scope

Work incrementally in `main` as approved, without force resets. New projects clone the source and configure env/DB/Redis/storage manually. Production uses PM2/Nginx and native services, **no installer, project generator, portable release manager or Docker dependency**.
