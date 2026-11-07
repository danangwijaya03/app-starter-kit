# Phase Roadmap — P00–P16 (incremental, preview-first)

**Status:** planning contract. Existing 157 task IDs are retained. Four added tasks (P01-08/09, P02-07, P03-09) front-load a visual preview and safe integration diagnostics. All task states remain `pending` until tests are performed; static root preview does not mark any task complete.

**Delivery-first interpretation:** the phase numbers remain technical workstreams to avoid breaking 157 old dependencies. **P01** now delivers an early UI shell fixture before the full authenticated shell in **P06**. Thus visual feedback arrives sooner without pretending production auth/RBAC exists. A phase with backend-only tasks must provide a safe diagnostic or reproducible technical preview, never a fake feature.

| Milestone | Phase | Tasks | Required reviewable result / gate |
|---|---|---:|---|
| A | [P00 — Specification and Agent Setup](phases/P00-specification-and-agent-setup.md) | 5 | Existing Next.js static preview at `/`; docs and task graph pass, all unfinished work labelled pending. |
| A | [P01 — Monorepo and Build Foundations](phases/P01-monorepo-and-build-foundations.md) | 15 | One workspace app plus API scaffold; early Salt & Pepper admin-shell **fixture**, documented startup and preview smoke test. |
| A | [P02 — Local Infrastructure](phases/P02-local-infrastructure.md) | 7 | Local Lerd services isolated; safe, dev-only service health preview or read-only diagnostic. |
| A | [P03 — Database Foundation](phases/P03-database-foundation.md) | 11 | Versioned Drizzle schema in disposable DB; safe DB health diagnostic and migration evidence, no secrets. |
| B | [P04 — Authentication](phases/P04-authentication.md) | 7 | Login/session and first-login enforcement flow ready for integrated review; no auth bypass by demo. |
| B | [P05 — RBAC and Initial Administrator](phases/P05-rbac-and-initial-administrator.md) | 12 | Permission registry, secure bootstrap, authorization checks and denied scenarios. |
| B | [P06 — Design System and Admin Shell](phases/P06-design-system-and-admin-shell.md) | 9 | Convert early fixture to authenticated, responsive, permission-controlled admin shell. |
| B | [P07 — User and Role Management](phases/P07-user-and-role-management.md) | 7 | Real user/role management and permissions matrix; positive/negative cases. |
| B | [P08 — Dashboard](phases/P08-dashboard.md) | 5 | Dashboard widgets backed by authorized API/database; demo fixture replaced. |
| C | [P09 — Storage and Media Library](phases/P09-storage-and-media-library.md) | 7 | Authenticated media upload/list/delete and persistence review. |
| C | [P10 — CMS Page Editor and Revisions](phases/P10-cms-page-editor-and-revisions.md) | 12 | Draft editing, revisions and publish flows tested with real API. |
| C | [P11 — Public CMS and Navigation](phases/P11-public-cms-and-navigation.md) | 7 | Published-only pages and navigation; protected draft previews. |
| C | [P12 — Settings and Appearance](phases/P12-settings-and-appearance.md) | 8 | App branding, logo and Salt & Pepper theme settings persisted. |
| D | [P13 — Background Worker and Queue](phases/P13-background-worker-and-queue.md) | 6 | Safe queue/job diagnostics and actual worker test. |
| D | [P14 — Backup](phases/P14-backup.md) | 9 | Encrypted backup test in disposable environment, verified manifest. |
| D | [P15 — Restore and Recovery](phases/P15-restore-and-recovery.md) | 10 | Isolated staged restore, safety/maintenance UI or documented operator diagnostics. |
| D | [P16 — Build, Artifact and Server Release](phases/P16-build-artifact-and-server-release.md) | 24 | Compose project initializer + app setup CLI + deployment manager, artifact-only server smoke, upgrade/rollback tests. |

## Preview gate and agent flow

1. Select the next **ready** task from `TASKS.yaml`; do not execute visually next phase if dependencies are missing.
2. Lifecycle: **RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**.
3. Preview record must state route and verified URL (or `not verified`), scope, **fixture/integrated/diagnostic**, tests/exit codes, review steps, pending blockers and source commit. See [preview contract](PREVIEW-AND-FEEDBACK.md).
4. Review user status is **not** CLI task status. Feedback is non-blocking unless a particular unsafe decision requires explicit approval.
5. Use [agent routing](AGENT-ROUTING.md). Low handles bounded implementation; High is recommended for architecture/security/migration/restore/installer and independent review is required for effective high-risk tasks.
6. Phase gate still requires all scoped tasks completed with real tests. Preview alone cannot make a phase verified.

**Total planned atomic tasks: 161 (157 retained + 4 preview/integration tasks).**