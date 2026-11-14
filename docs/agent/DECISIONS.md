# Accepted architecture decisions — current

**Date:** 2026-11-14. This document supersedes earlier installer/release-artifact plans. Retained historical implementation IDs were migrated where still relevant.

- Repository `danangwijaya03/app-starter-kit`, development on `main`, preserve existing root Next.js 16.4.3/React 19.3 until P01 moves files by Git, not re-scaffolding.
- Reusable **single-tenant per clone**, MySQL 8.4 + Drizzle, Better Auth, database-driven app RBAC, standalone Hono API, Next.js public/admin, BullMQ worker + Redis; npm workspaces/Turborepo/one package lock, Node 26 baseline.
- **No installer**, no `apps/installer`, no project initializer/generator, portable release artifact, symlink switch manager, Docker requirement, or installer-specific metadata/secrets. New apps use clone + manual environment/database setup.
- Manual npm scripts for migration, permission sync, idempotent seed, first-super-admin bootstrap with non-echo secret, verification are **retained** and will be implemented through P03/P05/P16; no universal default password.
- Production deployment **manually from source** using npm build, PM2, aaPanel/Nginx, isolated MySQL/Redis and protected local storage. Live migration/backup/restore requires operator authorization.
- **Reference-driven implementation:** curated official libraries and examples (Celestia, Blur Stack, Hono Starter etc) with source pinning, license attribution, exclusions and testable invariants. See `docs/references/`. No wholesale template copying.
- **Single active coding agent per task/session (provider/model-agnostic)**. High Reasoning AI optional, not required. Keep actual high-risk independent security review and negative/concurrency tests; risk is not model-effort classification.
- Visual preview-first incremental workflow: RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT; visible UI fixture early, real auth/API/DB only once implemented.
- CMS block/revision/published-pointer, Salt & Pepper theme, Dashboard / Manage Content / Manage User / Setting main menu, private media, backup/restore, audit, worker and typed contracts remain MVP.
- Optional reference ideas (2FA, notifications, i18n, extra storage, monitoring) do **not** become MVP tasks without a later scoped decision.
