# Low-Agent Implementation Recipes — Reference Patterns

These are **blueprints for future coding tasks**, not a working implementation. Verify exact APIs against the installed versions and source-specific task card. Never copy placeholders or claim commands succeeded merely because they appear here.

## Recipe A: P01-01A root workspace bootstrap

Create these files with no secrets.

**`package.json (workspaces)`:**

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

**Root `package.json` minimal target:**

```json
{
  "name": "codelight-nextjs-starter-kit",
  "private": true,
  "packageManager": "npm version determined during P01",
  "scripts": {
    "agent:next": "python3 tools/agent_tasks.py next",
    "agent:validate": "python3 tools/validate_plan.py"
  }
}
```

The `packageManager` value is the v1.1 reference; P01-02 verifies it on the chosen Node runtime, and normal build/test scripts are added by dependent tasks. Do not put `workspace:*` dependencies in root until the packages exist.

**Read-only validation:** `python3 tools/validate_plan.py`; verify `package.json (workspaces)` matches both patterns; when package files exist run the actual frozen install after a lockfile has been created. Do not run `--frozen-lockfile` before generating the initial lockfile.

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

## Recipe G: Backup/restore boundary

- Backup worker calls `mysqldump` with **argument array**, credentials from protected temporary file (never visible in process command-line arguments), and InnoDB-safe flags such as `--single-transaction --quick` as applicable.
- Streams to protected storage, encrypts, adds manifest/checksum. A backup is not `verified` until it restores into disposable MySQL.
- Restore uses a separate high-risk workflow: authorization and recent reauth → checksum + compatibility preflight → staging test restore → pre-restore recovery snapshot → maintenance/drain → controlled import → health/reconcile.
- **Never auto-retry restore** and never let SQL import failure clear maintenance automatically. Journal must live outside restored DB.

## Recipe H: Portable production artifact

Build separately:

1. Next.js standalone (`output: 'standalone'`, monorepo tracing root). Package `server.js`, `.next/static`, `public` and runtime dependencies.
2. Hono API, BullMQ worker and installer: build/bundle with runtime dependencies, using packaging supported by installed npm/TS toolchain.
3. Include Drizzle SQL migration files and manifest with target OS/arch/Node ABI and file checksums.
4. Perform smoke test **from extracted release directory without source monorepo** on a target-compatible Linux runtime.
5. Only then package `.tar.gz` and include tested `README-SERVER.md`.

**Deploy:** upload to non-public `releases/<version>`, checksum verify, configure `shared` paths, review migration safety, switch `current` symlink, restart PM2 and healthcheck. DB migration failure is not automatically reversible by a code symlink change.

## P01–P16 final rule

Use these recipes for shapes, but **the atomic task card defines the next permitted change**, and `docs/BSD.md` defines final fields, permission codes, indexes, and endpoints. Do not implement everything from a recipe in a single task.