# Roadmap P00–P16 — incremental clone-based development

**Status:** planning contract; no task is completed merely by updating docs. `TASKS.yaml` remains authoritative. **156 pending tasks** after removing five installer/archive-only tasks. Existing P00–P16 IDs are preserved where work remains useful. Current root Next.js preview remains a fixture.

**Strategy:** Clone-Based Reusable Starter Kit + Reference-Driven Development + Single Coding Agent **per task/session**. **Provider neutral**: Codex, Claude Code, Antigravity, DeepSeek, or another capable agent. One model active at a time; the model may change between tasks/sessions. No High Reasoning model is required as a product dependency. Security risk never downgraded and independent review required for effective high-risk tasks.

| Milestone | Phase | Tasks | Review checkpoint |
|---|---|---:|---|
| A | [P00 — Specification & Agent Foundation](phases/P00-specification-and-agent-setup.md) | 5 | Static Next.js demo, reference/catalog decisions, task graph and docs consistency |
| A | [P01 — npm Monorepo & Early Preview](phases/P01-monorepo-and-build-foundations.md) | 14 | Move existing Next.js, build Hono API and BullMQ worker only, show honest UI fixture and preview smoke |
| A | [P02 — Local Lerd Infrastructure](phases/P02-local-infrastructure.md) | 7 | Isolate MySQL/Redis dev/test, expose safe dev-only readiness diagnostic |
| A | [P03 — Drizzle MySQL Foundation](phases/P03-database-foundation.md) | 11 | Versioned schema, reviewed migrations, read-only DB health |
| B | [P04 — Better Auth & Sessions](phases/P04-authentication.md) | 7 | Real login/logout/reset/first-login change, deny unauthorized access |
| B | [P05 — Database RBAC & Manual Admin Bootstrap](phases/P05-rbac-and-initial-administrator.md) | 12 | Secure permission registry, server checks and manual first-admin bootstrap, race denial |
| B | [P06 — Authorized Admin UI Shell](phases/P06-design-system-and-admin-shell.md) | 9 | Replace static fixture with authenticated, permission-aware responsive shell |
| B | [P07 — Users & Roles](phases/P07-user-and-role-management.md) | 7 | Typed CRUD user/role and permission matrix with server denial tests |
| B | [P08 — Authorized Dashboard](phases/P08-dashboard.md) | 5 | Real widgets and statistics from permission-limited Hono/MySQL |
| C | [P09 — Private Media](phases/P09-storage-and-media-library.md) | 7 | Safe upload/list/delete, opaque storage keys and reference integrity |
| C | [P10 — CMS Editor & Revisions](phases/P10-cms-page-editor-and-revisions.md) | 12 | Drafts, immutable revisions, typed blocks, publish with conflicts handled |
| C | [P11 — Public CMS & Navigation](phases/P11-public-cms-and-navigation.md) | 7 | Published-only public routing, SEO, protected preview |
| C | [P12 — Settings, Branding & Theme](phases/P12-settings-and-appearance.md) | 8 | Real persisted settings, Salt & Pepper UI tokens and appearance |
| D | [P13 — BullMQ Worker](phases/P13-background-worker-and-queue.md) | 6 | Isolated queue, retry/idempotency and worker restart evidence |
| D | [P14 — Encrypted Backup](phases/P14-backup.md) | 9 | Verified backup, checksum, permissions and isolated restore validation |
| D | [P15 — Controlled Restore](phases/P15-restore-and-recovery.md) | 10 | Staged restore/recovery, journal, explicit maintenance and manual approval |
| D | [P16 — Manual Clone/Setup/Production Deployment](phases/P16-manual-clone-and-deployment.md) | 20 | Build three apps, manual npm migration/seed/admin scripts, PM2/Nginx, clean-clone smoke and recovery; no installer |

## Flow and reviewer boundaries

1. **RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**
2. Select next ready task by CLI dependency graph; read relevant single reference playbook and version/license if borrowing code.
3. Preview may be static fixture or verified actual API/DB feature; always label. Infrastructure tasks may use read-only diagnostic in place of UI.
4. One coding agent/model performs an implementation task at a time; independent qualified reviewer signs high-risk approvals. No vendor/model-tier lock-in.
5. CI/docs checks do not equal real security/functional tests. User UI feedback is recorded separately from technical task statuses.
6. New apps use clone + manual npm env/DB/seed/admin setup, build and PM2/Nginx; **no installer/project generator/release archive/symlink manager**.

See [Reference Map](../references/REFERENCE-MAP.md), [Manual Setup](../MANUAL-CLONE-SETUP.md), [Single Agent Workflow](SINGLE-MODEL-WORKFLOW.md).
