## Implementation Contracts v2 — mandatory agent overrides

1. Do not hardcode initial admin email. Read it from protected setup input; password non-echo and force change, never reset existing account.
2. Core always on; `enabledModules` static map for media/cms/operations, validated at build/start. No dynamic dashboard toggle or conditional DB schema migration.
3. API and web always on; Redis/worker conditional. Never require `REDIS_URL` for Core-only or log missing Redis as Core failure.
4. Single Better Auth identity; application-only RBAC. Limited delegation with `delegable/sensitive`, no self elevation, protected last-active-superadmin transactional lock.
5. Hono `routes.ts` + `service.ts` + `repository.ts` generally; controller optional, not mandatory boilerplate. No Next business API duplication.
6. Media module permission prefix `media.*`; CMS depends on Media and uses immutable versioned blocks and revisions.
7. Admin and draft always no-store, public CMS SSR no persistent cache. Do not implement mandatory `revalidatePath` until future approved cache ADR.
8. `system_jobs` MySQL durable intent+dispatcher; BullMQ at-least-once, idempotent processing; no job loss on Redis outage.
9. LocalFs outside webroot; file state pending/ready/failed/deleted, public/private delivery, reference-preserving cleanup.
10. App settings typed; theme snapshots immutable, public/admin semantic theme same, media fallback when Media disabled.
11. Production restore independent CLI only, no POST restore API, no automatic retries. Offsite encrypted backup and drill required for Core release.
12. Pino redacted JSON, transactional audit, health endpoints and external uptime.
13. CI automatic, deployment manual from approved SHA, PM2 worker optional; no unconditional 3-process assumption.
14. Core-first release; module certifications independent; task IDs/status/evidence preserved and PRD ID mapping reviewed.

Tests and source code, not fixture pages or successful lint alone, prove implementation. Record actual dependency/library version and source license when adopting references.
