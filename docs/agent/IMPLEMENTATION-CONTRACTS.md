# Implementation Contracts — Architecture v2 Invariants for Any Coding Agent

**Status:** specification only; target paths and commands below become real as coding tasks implement them. Use `docs/BSD.md` for complete schema and APIs. If there is a conflict, **block the task, record the exact section/line and do not guess**.

## 1. Fixed technology decisions

- Monorepo: `npm` workspace + Turborepo, strictly TypeScript.
- Runtime: Node.js 26.x development baseline, pinned exact version after testing, no release archive manager. Core-only requires web/API; worker/Redis conditional.
- UI: Next.js **16.4.3 App Router**, React version compatible with the pinned Next release, Tailwind CSS 4, shadcn/ui and selected free Aceternity UI. Do not pick new major versions without explicit ADR.
- Backend: standalone Hono on Node.js, MySQL **8.4 LTS**, Drizzle ORM and generated Better Auth schema. No NestJS and no Next.js API business duplication.
- Background jobs: BullMQ + Redis **only when selected modules require jobs**. MySQL system_jobs holds durable intent; lease/replay and idempotent worker, Core-only must start without Redis.
- Production: approved Git SHA + CI, manual clone/npm build + PM2/Nginx/aaPanel, **NO Docker**. PM2 always runs web/API, worker only if jobs-enabled.
- Single tenant per project. Default theme Salt & Pepper; light/dark/system support; branding configurable in database.
- Primary public routes: `/`, CMS published slugs; admin `/admin/*`; Better Auth `/api/auth/*`; business `/api/v1/*`.
- Admin groups: Dashboard, Manage Content, Manage User, Setting, **show only nonempty authorized groups**. No Manage Content in Core-only; Media may appear independently of CMS.
- First administrator email and password are **operator-supplied via protected input**; never hardcoded or logged. Bootstrap `super_admin` active and enforce first-login password change.

## Local development contract

Lerd provides MySQL locally, Redis is used only for jobs-enabled modules. Do not create duplicate services or Docker infrastructure; Core-only has no REDIS_URL requirement. Validate actual MySQL version, host/container connection addresses, isolated dev/test schemas and Node 26. See [LOCAL-LERD-NODE26.md](LOCAL-LERD-NODE26.md). Do not change global Lerd routing, Nginx, or LAN exposure without approval.

## 2. Package ownership and imports

| Owner | Allowed responsibilities | Forbidden |
|---|---|---|
| `apps/web` | Next.js pages, client feature UI, typed API calls | Import API service, MySQL pool, Drizzle credentials |
| `apps/api` | Hono routes, auth, policies, service/repository | Import React frontend modules |
| `apps/worker` (optional) | Jobs-enabled BullMQ processors and durable dispatch | Public HTTP, required dependency for Core/offsite backup/recovery |
| `packages/database` | Schema, DB client, migration files | React UI |
| `packages/contracts` | Public request/response Zod schemas | Database connection or secrets |
| `packages/permissions` | Role permission codes, navigation manifest | User-specific UI state |
| `packages/ui` | UI primitives/components/tokens | Business DB operations |
| `packages/cms-blocks` | Separate schemas/renderer/editor for versioned CMS blocks | Arbitrary executable HTML/JS or server importing browser React |
| `packages/storage` | LocalFs-first safe storage; optional S3 adapter | Hardcoded deployment paths, public/private bypass |

Avoid circular dependencies. Only API/worker and explicit server-only manual setup scripts import server-only database modules. Never save credentials to web's public assets or `NEXT_PUBLIC_` variables.

## 3. Canonical module directory conventions

Backend business module files (only create the ones needed):

```text
apps/api/src/modules/<module>/
  <module>.routes.ts
  <module>.controller.ts
  <module>.service.ts
  <module>.repository.ts
  <module>.policy.ts
  <module>.test.ts
```

Request path: **Route → authentication → active-account/first-login guard → static module guard → RBAC → Zod → optional Controller → Service → Repository → MySQL**. Controller does not write SQL; repository does not decide role grants.

### Response envelopes (business API only)

```json
{"data":{"id":"example"},"meta":{"requestId":"example-id"}}
```

Error:

```json
{"error":{"code":"PERMISSION_DENIED","message":"You do not have permission.","details":null},"meta":{"requestId":"example-id"}}
```

`/api/auth/*` follows Better Auth native response format. Business lists use `page`, `limit`, `total`, `totalPages`, `requestId`. Always cap pagination and use stable sort.

## 4. Canonical RBAC and session invariants

- Permission source: `packages/permissions/src/registry.ts` contains all codes from `docs/BSD.md`. UI labels are derived from registry; do not hardcode a second permission list.
- Multi-role union, default deny. Each route must enforce permission on **server**; hiding a menu does not grant security.
- Canonical examples: `dashboard.view`, `users.view`, `users.create`, `users.roles.assign`, `roles.permissions.update`, `cms.pages.publish`, `settings.appearance.update`, `backups.restore`.
- `super_admin` protected. The system must prevent deleting/deactivating the **last active** one under concurrent requests. Use appropriate locking and transaction, not a count-then-update without a lock.
- Ordinary administrators cannot promote themselves or others to `super_admin`. Session permission changes take effect at the next protected API request.
- Public signup disabled. First-login change-password is server-enforced; user must not escape by calling APIs directly.
- Use Better Auth session/password/reset primitives; do not invent custom password hash algorithms. With Drizzle, use Better Auth CLI to **generate** compatible schema and Drizzle for migration; `auth migrate` is not the production Drizzle migration mechanism.

## 5. Canonical CMS invariants

- Versioned JSON blocks with Zod schema, no executable JSX/HTML/JS injected from database.
- Draft revisions immutable; published revision selected by pointer. Saving draft **never** changes the public page.
- Publishing switches published pointer and slug under DB transaction, handles uniqueness collision and invalidates old/new slug caches after commit.
- Public queries return published only. Preview requires login + authorized token; no-store.
- CMS navigation only manages **public site menus**, not admin sidebar. Menu depth max two levels.
- Storage key opaque and server-generated; media stored outside immutable release folder. Referenced published media cannot be physically deleted.

## 6. Manual migration, seeds and administrator setup

**New empty dedicated database, executed manually after reviewing .env and DB target:**

1. Validate Node/env/MySQL and optional Redis when jobs enabled and dedicated database target.
2. Apply reviewed Drizzle migrations with npm script (`db:migrate:check` then `db:migrate`).
3. Sync canonical permission registry (`permissions:sync`) and seed system roles + Salt & Pepper defaults (`db:seed`) idempotently.
4. Bootstrap operator-selected initial super admin via protected non-echo manual npm script (`setup:admin`) after roles exist. Never pass password as argument or commit it. First login must force a password change.
5. Verify private endpoints and identity via `setup:verify` and actual tests.

Repeated seed/bootstrap must **not** duplicate accounts/reset credentials; no destructive production migration without explicit operator authorization. No `apps/installer` or project initializer.

## 7. Deployment paths — clone based

Clone an authorized project repository to a private working directory such as `/srv/apps/<project>/` using separate private `.env`, `storage/media`, `storage/backups`, `storage/logs`. Build/run web, API and worker with PM2 and Nginx same-origin routing. Source may reside on the server; no portable release archive, `current` symlink manager, or release manifest is required. Validate secrets/storage outside public root.

Production migration/recovery performed manually from source with reviewed SQL; Git code rollback does not roll back schema state.

## 8. Version and file existence policy

As soon as P01 installs dependencies, commit a lockfile and write exact resolved versions into `docs/agent/DEPENDENCY-LOCK.md`. After that, Low agents use those versions and do not silently upgrade. If a cited package API differs from the exact installed version, record the mismatch and request a scoped update/review rather than inventing compatibility glue.

Any path described as a **target** may not exist until its task completes. Never report successful `npm` checks just because they are written in this document.
## 9. Single-model, reference-driven implementation contract

- Preserve static Next.js fixture until integrated paths exist; provide honest preview/diagnostic checkpoints.
- Use **selected coding agent for all bounded implementation tasks**. No High Reasoning model routing or mandatory model upgrade.
- Read per-task [Reference Map](../references/REFERENCE-MAP.md) and [Adoption Protocol](../references/ADOPTION-PROTOCOL.md): official libraries first; record version/license/source only when copying code; adapt MySQL/npm/single-tenant boundary.
- Keep independent qualified review for effective high-risk tasks. User UI feedback in REVIEW-QUEUE cannot substitute technical approval.
- Work on main; clone-based reuse and manual PM2/Nginx operations, no installer or Docker. See [Single Model](SINGLE-MODEL-WORKFLOW.md).


## 10. Architecture v2 — hard gates (accepted 2026-11-14)

The authoritative [v2 addendum](../revisions/IMPLEMENTATION-CONTRACTS-v2-ADDENDUM.md), [Module Boundaries](../architecture/MODULE-BOUNDARIES.md), [Auth/RBAC](../architecture/AUTH-RBAC-CONTRACT.md), [Database](../architecture/DATABASE-CONTRACT.md) and [Operations](../architecture/OPERATIONS-RUNBOOK.md) supersede any older unconditional worker or dashboard recovery examples.

1. **Core always on**; static Media/CMS/Operations map compiled/tested at startup. CMS→Media; Operations needing Jobs→Redis/worker. All optional tables still migrate centrally. Disabled module route/OpenAPI/nav/grants not exposed. Revoked disabled-module grants must not silently reappear on re-enable.
2. **Better Auth + one application permission authority**. `user_profiles.status = invited|active|disabled` and `must_change_password` guard; no parallel RBAC. `delegable`/`sensitive` grants and actor-owned delegation only; last-active-superadmin role row serialised and transactional audit.
3. **Hono sole business API**. Next SSR internal HTTP via `API_INTERNAL_ORIGIN` forwarding only chosen auth cookies; browser relative /api/v1 same-origin. Auth/admin/draft no-store. CMS public published-only SSR without persistent cache/revalidation MVP.
4. **Worker/Redis optional**, MySQL durable system_jobs dispatch, lease/idempotency and ACK crash reconciliation. A missing optional service never falsely fails Core-only readiness.
5. **Media LocalFs** ready/public gating and private RBAC, strict upload bytes+dimensions, reference-retaining cleanup; CMS save uses save_key/request_hash and 409 stale conflict.
6. **Immutable global semantic themes** with Core static branding fallback; per-user color mode. **Pino JSON redaction, transactional audit, external uptime and health endpoints** as Core.
7. **Production backup and recovery independent CLI** with encrypted offsite restic repository/staging rehearsal/operator cutover, never a BullMQ or HTTP restore or an installer. Automatic CI; manual approved SHA deployment. Core release gate [P16-11](tasks/P16-11.md) does not wait for optional module certification [P16-12](tasks/P16-12.md).
