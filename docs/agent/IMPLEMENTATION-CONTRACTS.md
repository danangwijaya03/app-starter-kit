# Implementation Contracts — Decisions Low Agents Must Not Re-Decide

**Status:** specification only; target paths and commands below become real as coding tasks implement them. Use `docs/BSD.md` for complete schema and APIs. If there is a conflict, **block the task, record the exact section/line and do not guess**.

## 1. Fixed technology decisions

- Monorepo: `npm` workspace + Turborepo, strictly TypeScript.
- Runtime: Node.js **26.x LTS** (development baseline; pin exact tested version for release). Target major version fixed, exact tested patch recorded during P01 and release manifest.
- UI: Next.js **16.4.3 App Router**, React version compatible with the pinned Next release, Tailwind CSS 4, shadcn/ui and selected free Aceternity UI. Do not pick new major versions without explicit ADR.
- Backend: standalone Hono on Node.js, MySQL **8.4 LTS**, Drizzle ORM and generated Better Auth schema. No NestJS and no Next.js API business duplication.
- Background work: BullMQ + Redis; worker process separate from API.
- Production: Linux Node.js build artifact uploaded to aaPanel/Nginx; **NO production Docker**. PM2 manages web, API, worker.
- Single tenant per project. Default theme Salt & Pepper; light/dark/system support; branding configurable in database.
- Primary public routes: `/`, CMS published slugs; admin `/admin/*`; Better Auth `/api/auth/*`; business `/api/v1/*`.
- Admin main menu **exactly** Dashboard, Manage Content, Manage User, Setting. Do not add other top-level menus in MVP.
- First admin email `admin@codelight.id`, role `super_admin`; **password comes from protected install-time secret, never committed, and user must change it at first login.**

## Local development contract

Lerd provides MySQL and Redis locally. Do not create duplicate services or Docker development infrastructure. Validate actual MySQL version, host/container connection addresses, isolated dev/test schemas and Node 26. See [LOCAL-LERD-NODE26.md](LOCAL-LERD-NODE26.md). Do not change global Lerd routing, Nginx, or LAN exposure without approval.

## 2. Package ownership and imports

| Owner | Allowed responsibilities | Forbidden |
|---|---|---|
| `apps/web` | Next.js pages, client feature UI, typed API calls | Import API service, MySQL pool, Drizzle credentials |
| `apps/api` | Hono routes, auth, policies, service/repository | Import React frontend modules |
| `apps/worker` | Queue consumers, backup/restore/media jobs | Public HTTP listener unless separately specified |
| `apps/installer` | CLI preflight, migration, seeds, bootstrap, verify | Background public server, embedding secrets |
| `packages/database` | Schema, DB client, migration files | React UI |
| `packages/contracts` | Public request/response Zod schemas | Database connection or secrets |
| `packages/permissions` | Role permission codes, navigation manifest | User-specific UI state |
| `packages/ui` | UI primitives/components/tokens | Business DB operations |
| `packages/cms-blocks` | Versioned block schema and public renderer components | Arbitrary executable content from database |
| `packages/storage` | Safe local/S3 adapters | Hardcoded deployment paths |

Avoid circular dependencies. Only API/worker/installer import server-only database modules. Never save credentials to web's public assets or `NEXT_PUBLIC_` variables.

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

Request path: **Route → requireAuth → requirePermission → Zod validation → Controller → Service → Repository → MySQL**. Controller does not write SQL; repository does not decide role grants.

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

## 6. Seed and installer order

**Order on a new empty disposable environment:**

1. Validate Node/platform/URLs and MySQL/Redis readiness.
2. Apply **reviewed** Drizzle migrations to the intended empty database.
3. Sync permissions idempotently.
4. Seed system roles and Salt & Pepper general/theme configuration.
5. Bootstrap initial administrator from secret prompt/file, assign protected `super_admin`, enforce password change.
6. Verify login, database connectivity and permission-protected endpoints.

Rerunning seeds/installer must not duplicate users or reset existing passwords. Never run destructive migration on shared/production DB without authorization.

## 7. Deployment & artifact paths

The release archive must include `web`, `api`, `worker`, `cli`, `database/migrations`, manifest/checksums, config templates, and `README-SERVER.md`. After upload, install under a **non-public** base such as `/srv/apps/<project>/` with `releases/`, `current` symlink, `shared/env`, `shared/media`, `shared/backups`, and `shared/logs`.

Production uses Node.js standalone web, compiled API + worker, MySQL/Redis services, PM2 and Nginx path proxy (`/api/*` to 127.0.0.1:4000, everything else to 127.0.0.1:3000). Do not package `.env`, secrets, logs, media, database data or actual backup archives. A failed DB migration is **not** solved by a blind symlink rollback.

## 8. Version and file existence policy

As soon as P01 installs dependencies, commit a lockfile and write exact resolved versions into `docs/agent/DEPENDENCY-LOCK.md`. After that, Low agents use those versions and do not silently upgrade. If a cited package API differs from the exact installed version, record the mismatch and request a scoped update/review rather than inventing compatibility glue.

Any path described as a **target** may not exist until its task completes. Never report successful `npm` checks just because they are written in this document.
## 9. Incremental source and review contract (2026-11-07)

- Keep a runnable local Next.js preview at each safe milestone. The initial root page is static **fixture**, not real admin functionality; phase P01 refines it after monorepo migration, P06 integrates authenticated/authorized shell.
- For every meaningful slice, record actual route/verified preview URL or failure, fixture/integrated/diagnostic mode, tests and observations in CHECKPOINT / REVIEW-QUEUE. Do not invent running servers.
- Low reasoning is default for explicit bounded modules. High reasoning is recommended for security/architecture/migration/restore/release/installer. Independent high-risk review is mandatory regardless of coding agent reasoning.
- `main` remains canonical; preview reviews must not force branch changes or dangerous repository resets.
- Installers are distinct: project initialization, application setup CLI, deployment manager. Bootstrap uses P05 service and cold release setup uses extracted version path before current symlink.
- Details in [Preview & Feedback](PREVIEW-AND-FEEDBACK.md), [Agent Routing](AGENT-ROUTING.md) and [Installer Boundaries](INSTALLER-BOUNDARIES.md).
