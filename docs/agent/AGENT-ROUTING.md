# Agent Routing — recommended reasoning and required review

**Audience: CODING AGENT / OPERATOR.** Recommendations are **not** a way to bypass the existing effective-risk gate. A low-reasoning agent can implement narrow, explicit work, but independent review requirements still apply.

## Default assignment

- **Low reasoning (default for routine units):** static UI, navigation layout, theme tokens, scoped CRUD forms from stable API contracts, docs, fixtures, test wiring, simple type-safe functions, existing script integration. One task card at a time; verify outcomes rather than speculate.
- **Medium reasoning (recommended when coordination grows):** cross-package typed contracts, nontrivial MySQL CRUD, CMS editor revision flows, worker scheduling and idempotency, Nginx/development orchestration, multi-module dependency changes.
- **High reasoning (recommended implementer or design reviewer):** authentication/security/session, Better Auth schema generation, RBAC elevation and last-super-admin races, migrations on existing data, initial administrator bootstrap, secret handling, file/media access controls, backup encryption, database restore/recovery, artifact integrity, release upgrade/rollback and any architectural replan or dependency graph rewrite. High can design/review a bounded contract while Low implements a safe subset; if no independent reviewer is available, block high-risk completion.

| Area | Task families to flag | Reason high reasoning helps |
|---|---|---|
| Auth & sessions | P04; critical Better Auth schema generation in P03 | Session revocation, forced password reset, credential lifecycle |
| RBAC and bootstrap | P05, especially P05-07A/B/C | Self-escalation, concurrent super-admin protection, safe idempotency |
| Data migration | P03 migration tasks; P16-04A | Compatibility, failed DDL and history consistency |
| CMS security | P10 publish revisions, P11 private preview; P09 private media | No unpublished data leaks, authorization and reference integrity |
| Background & backups | P13 retry rules, P14–P15 | Durable jobs, secret/key safety, controlled restore |
| Installer & deployment | P16 including P16-10 initializer | Idempotence, isolation, checksum, ABI compatibility and rollback |
| Agent task graph | TASKS.yaml / dependency changes / task splitting | Prevent broken DAG, unreachable work and false completion |

## Low agent operating rules

1. Read only the active card, its `spec_refs`, implementation contracts, and this routing guide when triggered.
2. Keep one bounded responsibility per task; add test evidence after last edit, preview when meaningful, checkpoint and continue to the next independent ready task.
3. If security, schema, integration design, cross-module invariants or destructive operations are ambiguous: write options and tradeoffs to a decision log; **request high-reasoning review before implementation** rather than guessing.
4. A high-reasoning recommendation is not automatically a prohibition on Low creating source files. But Low **must not self-approve** a high-risk task, forge review evidence, silently bypass denial tests or perform an unapproved production operation.
5. Independent reviewer (different agent or person) checks diff, test assertions, negative cases, source fingerprint and security invariants; explicit recorded approval is required by the existing `agent_tasks.py review` gate for effective high-risk tasks.
6. Reviewer availability must not block unrelated ready tasks; record blocked task and advance elsewhere. Never claim ongoing background work or automatic future action beyond the active session.

## High-reasoning handoff template

- Task ID / exact base commit / modified files / unchanged contracts.
- Decision required, alternatives, recommended change, rollback/failure risk.
- Positive and negative tests (including concurrency/recovery if relevant).
- Outcome: `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED` with reasons.
- Operator approval is **separate** for production DB, deployment, or destructive actions.
