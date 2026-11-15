# Low-Agent Implementation Recipes — Reference Patterns

These are **blueprints for future coding tasks**, not a working implementation. Verify exact APIs against the installed versions and source-specific task card. Never copy placeholders or claim commands succeeded merely because they appear here.

## Recipe A: P01 — migrate the EXISTING Next.js app to npm Workspaces

**Already present in repository:** `app/`, `public/`, `next.config.ts`, `eslint.config.mjs`, `tsconfig.json`, `package.json`, `package-lock.json`. Next.js **16.4.3**, React **19.3.0**, Tailwind v4. Do **not** create a fresh app.

1. Before modifying source, run `npm ci`, `npm run lint`, `npm run build` at the existing repository root. Record actual outcomes, including failures.
2. Prepare `apps/web/package.json` from the existing root package, preserving exact Next.js/React/Tailwind versions and all required scripts.
3. Plan a private npm workspace root using `workspaces` in `package.json`. The root `package-lock.json` is authoritative and must be regenerated with `npm install`, not edited manually.
4. Move **existing** app/public/config into `apps/web` with Git moves. Preserve Next 16 cacheComponents/partialPrefetching/agentFeedback/Turbopack settings; adapt file tracing only when build needs it.
5. Once the workspace is complete, run `npm install`, `npm ci`, `npm run lint -w @repo/web` and `npm run build -w @repo/web`.

**Root `package.json` target after P01 (illustrative, not currently installed):**

```json
{
  "name": "app-starter-kit",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "lint": "turbo run lint",
    "typecheck": "turbo run typecheck",
    "test": "turbo run test",
    "agent:next": "python3 tools/agent_tasks.py next",
    "agent:validate": "python3 tools/validate_plan.py"
  },
  "devDependencies": {
    "turbo": "PIN_VERIFIED_VERSION_DURING_P01"
  }
}
```

Do not literally install the placeholder. P01 pins the verified Turborepo version. npm CLI and Node runtime versions are captured from the environment; avoid inventing a `packageManager` version string. No `pnpm-workspace.yaml`, `pnpm-lock.yaml` or `workspace:*` dependencies.

## Recipe B: P01-02 TypeScript strict baseline

Create `tsconfig.base.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noImplicitAny": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "skipLibCheck": true,
    "noEmit": true
  }
}
```

This is a **server package baseline**. Next.js needs its own tsconfig extending the shared base and adjusting module/moduleResolution/JSX options according to the installed Next.js template. Do not assume this base `tsc -p` is a functional check for an empty root config. Run `tsc -p` against an **actual package** containing TypeScript sources and an appropriate tsconfig. Record exact version pins after compatibility checks.

## Recipe C: Hono route + response envelope

Use the `packages/contracts` owner for request/response schemas. Example structure (not copy-paste ready until imports are implemented):

```typescript
// apps/api/src/modules/users/users.routes.ts
import { Hono } from 'hono';

export const usersRouter = new Hono();
usersRouter.get('/', requireAuth(), requirePermission('users.view'), async (c) => {
  const query = parsePagination(c.req.query()); // Zod-backed helper from contracts
  const data = await usersService.list(query);
  return c.json({ data: data.items, meta: {
    page: query.page, limit: query.limit,
    total: data.total, totalPages: Math.ceil(data.total / query.limit),
    requestId: c.get('requestId')
  } });
});
```

The names `requireAuth`, `requirePermission`, `parsePagination`, `usersService` and request context bindings are **project-owned exports to implement in their own tasks**. Register requestId context type before using `c.get()`. Do not handwave missing imports: wait for relevant dependency tasks to complete.

**Tests required:** authenticated allowed user 200; missing session 401; session without permission 403; invalid paging 400/422; no sensitive user fields in response.

## Recipe D: Better Auth + Drizzle MySQL migration

1. Install the **pinned** Better Auth and adapter versions in their owner package.
2. Configure Better Auth `drizzleAdapter(db, { provider: 'mysql', schema })` using the exact adapter shape documented for the installed version.
3. Generate auth schema from that actual installed version: Better Auth CLI `generate` (target: Drizzle + MySQL; include configured auth plugins).
4. Review generated `user`, `session`, `account`, `verification` types and foreign keys.
5. Generate SQL with Drizzle migration tooling, inspect, apply to **disposable local MySQL**, and verify schema there. Do not use `auth migrate` for the Drizzle adapter; it is intended for the built-in adapter.
6. Never overwrite a previously applied migration just to silence a mismatch.

**Verify:** create a test user using Better Auth's supported API, login, use session, logout; confirm no public signup and inactive-user access denied. Do not directly create password hashes in migrations.

## Recipe E: Permission registry + protected route

Registry owns exact canonical code strings in `packages/permissions/src/registry.ts`:

```typescript
export const permissionCodes = [
  'dashboard.view',
  'users.view',
  'users.create',
  'users.roles.assign',
  'roles.permissions.update',
  'cms.pages.publish',
  'settings.appearance.update',
  'backups.restore'
] as const;
```

This is **illustrative, incomplete**; use the full canonical list from BSD and include all required codes before sync. The permission registry must be idempotently synchronized with MySQL. A code removed from source is marked inactive, not simply deleted with FK damage.

For a Hono business endpoint, middleware order is auth → RBAC → request validation. Test direct API access with 401/403, not only hidden frontend menu. Super Admin last-active protection requires a database lock and concurrency test; do not implement it using an unprotected count check.

## Recipe F: CMS published revision

- `cms_pages` stores published pointer and published slug; `cms_page_revisions` stores immutable revisions.
- Draft-save **inserts** a new revision (does not update old revision, does not change published slug or pointer).
- Publish validates revision's `page_id` matches page, ensures reserved slug restrictions, applies pointer/slug change in a DB transaction, emits audit, then invalidates old/new slug cache after commit.
- Preview queries draft only for authorized authenticated user. Public route queries published pointer only.

**Tests:** draft changes do not appear publicly, invalid block props rejected, published slug collisions return 409, preview token cannot be reused as a public link, old/new slugs handled on publish.

## Recipe G: Independent encrypted offsite backup / recovery CLI

- Backup worker calls `mysqldump` with **argument array**, credentials from protected temporary file (never visible in process command-line arguments), and InnoDB-safe flags such as `--single-transaction --quick` as applicable.
- Streams to protected storage, encrypts, adds manifest/checksum. A backup is not `verified` until it restores into disposable MySQL.
- Operator-only CLI restore uses a separate high-risk workflow: authorization and recent reauth → checksum + compatibility preflight → staging test restore → pre-restore recovery snapshot → maintenance/drain → controlled import → health/reconcile.
- **Never auto-retry restore** and never let SQL import failure clear maintenance automatically. Journal must live outside restored DB.

## Recipe H: Clone-based production build and manual operations

1. Clone authorized project Git repository into a private server directory; create project-specific environment/DB/Redis/storage. Never inherit starter sessions/secrets/media.
2. Run `npm ci` and verified scripts for migration check/apply, permission sync, idempotent seed, secure admin setup. Review SQL and back up before live database modifications.
3. Build the three apps using npm workspace scripts actually implemented: Next.js web (optional standalone output), Hono API, BullMQ worker. PM2 starts three independent processes.
4. Configure aaPanel Nginx `/api/*` to Hono and `/*` to Next.js, HTTPS, same-origin secure session cookies; test real login/denials.
5. For update/recovery, record current commit, rehearse migrations in disposable DB, backup, pull/build/restart, smoke test. A Git checkout does not roll back the DB. **No installer CLI, tar artifact, archive manifest, versioned symlink or automated rollout manager.**

## P01–P16 final rule

Read the matching [Reference Map](../references/REFERENCE-MAP.md) and [Adoption Protocol](../references/ADOPTION-PROTOCOL.md) first. Use these recipes for shapes, but **the atomic task card defines the next permitted change**, and `docs/BSD.md` defines final fields, permission codes, indexes, and endpoints. Do not implement everything from a recipe in a single task.
## Recipe I: Modular Core v2 and conditional jobs

- [Module catalog](../architecture/MODULE-BOUNDARIES.md): Core always on; static Media/CMS/Operations selection with strict dependency closure; CMS→Media, Jobs capability→conditional Redis/worker. Disabled modules have no route/grants/OpenAPI/menu; centrally migrate all 21 tables.
- [RBAC](../architecture/AUTH-RBAC-CONTRACT.md): Better Auth owns identity, app RBAC owns permissions; invited status, no self-elevation, limited delegation, consistent last-admin MySQL lock/audit.
- [CMS](../architecture/MEDIA-CMS-CONTRACT.md): save_key/request_hash/expectedRevisionNo, immutable revision, published-only SSR without persistent cache; Media independent.
- [Jobs](../architecture/JOBS-CONTRACT.md): transactional MySQL intent, lease dispatcher, replay-safe deterministic BullMQ IDs; Core operates when Redis unavailable.
- [Recovery](../architecture/OPERATIONS-RUNBOOK.md): offsite restic/encrypted CLI independent of Hono/Redis; no POST production restore endpoint. Core [P16-11](tasks/P16-11.md) does not wait for selected-module gate [P16-12](tasks/P16-12.md).
