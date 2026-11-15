# Accepted architecture decisions — proposed v2 replacement

**Date:** 2026-11-14 · **Status:** accepted architecture design, implementation not proven.

Source of detailed decisions: `docs/architecture/ADR/README.md`, consolidated SPEC at repository root `SPEC-001-app-starter-kit-modular-core.md`. If legacy docs conflict, block affected task until their clauses are rebased; do not silently guess.

- Single-tenant per clone; Core modular monolith; no project installer, generator, Docker requirement, dynamic module enable UI, or release archive manager.
- Static `packages/config` module map; Core always enabled; Media optional; CMS optional requires Media; Operations optional and jobs required if enabled; other background modules can opt in.
- Always-on runtimes: Next.js Web and standalone Hono API behind same-origin Nginx. MySQL 8.4/Drizzle centralized migrations for all tables; Redis and PM2 worker conditional.
- Better Auth for identity/session; application-managed single RBAC authority with multi-role union, default-deny, invitation-first and safe forced password change. Limited delegation and protected last-active-superadmin.
- API Hono `/api/v1`, native Better Auth `/api/auth`; Zod/OpenAPI contracts. Next App Router SSR internal API call forwards selected auth cookies only; admin/draft no-store. Public CMS SSR no persistent cache on MVP.
- Durable MySQL `system_jobs` intent + dispatcher to BullMQ; idempotent worker and recovery. Media LocalFs private with public/private delivery and S3-ready adapter.
- CMS structured versioned blocks + immutable revisions + atomic published pointer; no arbitrary executable content; CMS depends on Media.
- Global semantic theme snapshots immutable, per-user light/dark/system, Salt & Pepper default and Core fallback branding when Media disabled.
- Independent CLI backup, restic encrypted offsite repository and isolated production recovery with operator approval; Operations UI optional and cannot one-click restore production.
- Pino redacted JSON logging, transactional MySQL audit, health probes and external uptime monitoring.
- Automatic CI + manual deploy of approved commit; release Core first, certify optional modules independently.
- Preserve existing Next root scaffold until P01 moves it by Git, existing requirement IDs, 156 original task IDs, status/history/checkpoints and source attribution, unless an explicit reviewed rebase documents changes.
- Admin bootstrap email **operator supplied**, not hardcoded. No universal password.
- GPL-3.0 license compatibility with intended distribution remains separate legal/product decision; do not silently change license.
