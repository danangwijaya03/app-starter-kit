# Accepted Architecture Decisions — v2 Modular Core

**Accepted design:** 2026-11-14. **Implementation:** pending code/tests. Supersedes previous "three required Node runtimes, CMS in every MVP, backup via worker, default admin email and all-or-nothing P16 release" assumptions. Full [ADR register](../architecture/ADR/README.md), [Unified SPEC](../../SPEC-001-app-starter-kit-modular-core.md), [Proposed v2 source](DECISIONS.v2-PROPOSED.md).

- Clone-based reusable **single-tenant Modular Core**, npm workspaces/Turborepo, Next.js web + standalone Hono API + MySQL/Drizzle; NO installer, Docker or auto-deploy.
- **Core MUST:** Better Auth, application-only RBAC (one effective grants source), user invites/status/first-password-change, limited delegation, Core dashboard, typed settings + immutable semantic theme snapshots, audit, Pino/health/external monitoring, offsite encrypted backups, **independent operator CLI recovery**, automatic CI and manual production deployment.
- **Optional SHOULD:** Media LocalFs (independent), CMS (requires Media) published-only SSR, Jobs (durable MySQL intent + BullMQ/Redis worker only when needed), optional Operations status UI. Core can deploy with Redis/worker/Media/CMS/Operations all disabled.
- Static source-controlled `enabledModules` validated at build/start, unknown/dependency cycle/config hash mismatches rejected; no dynamic UI toggles or conditional database migrations. Disabled modules have no route/permissions/nav/OpenAPI/worker processors.
- All **21 logical tables** centrally versioned via Drizzle; generated Better Auth tables not manually assumed. Schema delta: invited, delegable/sensitive, media ready/public lifecycle, CMS save idempotency, jobs lease fields, offsite backup verification; history preserved.
- Server route architecture: Better Auth `/api/auth/*`, Hono business `/api/v1/*`; Next SSR internal Hono HTTP with selected auth cookies; auth/admin/draft no-store. Public CMS SSR no persistent cache in MVP.
- Auth and RBAC: no hardcoded initial admin email/password; operator-supplied secure inputs; permissions `media.*`, limited delegation, active account state, consistent MySQL last-superadmin lock and transactional audit.
- Production recovery **never** `POST /backups/:id/restore`, never one-click dashboard, worker auto-retry or app-coupled service. Linux CLI/restic encrypted offsite + isolated staging + operator-approved cutover and external journal.
- Observability: lightweight Core Pino JSON redacted logs + transactional audit, live/ready/subsystems health, external uptime.
- Core-first release [P16-11](tasks/P16-11.md), optional module certifications independently and all-module matrix [P16-12](tasks/P16-12.md). Phase IDs remain historical workstreams, not strict release order.
- Coding-agent workflow is model/provider-neutral: one active agent/model per bounded task or session. Independent security review mandatory for effective high risk; a High Reasoning model is **not** a product requirement.
- Existing root Next.js preview is demo only; no code feature is marked complete by adopting these documents.

**Explicit legal item still pending:** review GPL-3.0 distribution/compatibility implications before incorporating external licensed source or distributing a derivative. [Library Reference Checks](../architecture/LIBRARY-REFERENCE-CHECKS.md) and [Source Attribution](../references/SOURCE-ATTRIBUTION.md) are research records, not license approval.
