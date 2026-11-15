## TRD v2 Addendum — Runtime, modules, SSR and operations (supersedes TRD-01, 03, 06, 07, 09, 12 where inconsistent)

- **Runtimes:** required Web Next.js + Hono API; optional Redis and BullMQ worker depending on checked-in static modules. No automatic env requirement for REDIS_URL in Core-only.
- **Infrastructure:** Nginx same-origin `/api/*` proxy; Next SSR calls Hono via internal HTTP with selected Better Auth cookies; runtime services loopback; no Next business API duplication.
- **Module catalog:** source-controlled, verified dependency graph and activation; CMS→Media, Operations→Jobs. Sync of disabled permissions revokes grants with audit; modules don't create/destroy database tables.
- **Packages:** web cannot import database/server services; worker cannot import Hono routes; shared domain logic server-only; `cms-blocks/schemas` isolated from React.
- **Migration:** all tables from base BSD including disabled modules, one Drizzle journal; Better Auth schema generator uses installed version; `push` never production. Compatibility gate before release.
- **Private caching:** admin/auth/draft always no-store. Public CMS SSR without persistent cache MVP. Delete outdated mandatory cross-process `revalidatePath/Tag` requirement for MVP; preserve as deferred design.
- **Auth:** Better Auth identity only; app RBAC single authority with limited delegation, active account guard, disabled-module guard, audit transaction.
- **Jobs:** MySQL `system_jobs` intent/dispatcher + BullMQ at-least-once, idempotent processors and retry; optional Redis/worker.
- **Media:** LocalFs outside webroot, public/private delivery, pending→ready/failed lifecycle, strict file limits; optional S3 adapter later.
- **Backup:** Linux scheduler, restic encrypted offsite, CLI independent of app production; staging verification + operator cutover, no dashboard destructive restore.
- **Logging:** Pino JSON, transactional audit, liveness/readiness/subsystems and external uptime monitoring.
- **Deployment:** PM2 web+API, conditional worker, manual approved SHA, CI and independent offsite backup readiness.
