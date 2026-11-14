# Manual Clone Setup — reusable starter kit, no installer

**Status:** approved target procedure; only the root Next.js scaffold currently exists. Many workspace/npm scripts named below **do not yet exist** and must be implemented under their task IDs before running. No installer CLI, generator, release archive, version symlink or Docker dependency is planned.

## 1. Start a separate project from a template clone

```bash
# Example: clone the starter as a new project directory
git clone <authorized-starter-repository-url> my-new-project
cd my-new-project
```

Choose how to retain Git history:

- If maintaining upstream updates: keep `origin` and add the new app repository as a separate remote with explicit naming, after checking permissions.
- If creating an independent project: initialize the new repository's history intentionally (e.g. GitHub's **Use this template** workflow when available), not by deleting a working tree blindly. Do not accidentally push project secrets or unrelated project data to the starter remote.

## 2. Local environment (Lerd preferred)

Baseline: Node 26, npm, existing local Lerd MySQL and Redis, one root npm lockfile. Verify versions and current services without installing duplicates. Copy `.env.example` to private `.env` once the template exists; set a **new** unique database/schema, Redis prefix, media path, session secret, canonical origin and project branding. **Never copy another project's .env/data**.

```bash
npm ci
# Create dedicated MySQL DB/user and isolated Redis prefix manually.
# Configure .env privately; do not commit it.
```

## 3. Database, roles and initial administrator

**Target scripts (to be built and verified during P03/P05/P16; not available on today's root scaffold):**

```bash
npm run db:migrate:check
npm run db:migrate
npm run permissions:sync
npm run db:seed
npm run setup:admin
npm run setup:verify
```

Migrations must reject wrong environment and incompatible history, fail closed on destructive changes, and protect production writes. Seeds/permission sync are idempotent and must not overwrite an existing administrator credential. Admin bootstrap consumes a protected interactive prompt or private secret input, **never a password argument/committed secret**. Verify first login forced password change and account/session/role guards.

## 4. Development, verification and review

Current root scaffold:

```bash
npm run lint
npm run build
npm run dev
```

After P01 moves the app to `apps/web`, use only the workspace scripts actually added and tested. Start web/API/worker separately or via a verified npm workspace dev orchestration. The UI is initially a clearly labeled static demo; never infer that API, auth, RBAC or MySQL already works from the page.

## 5. Manual deployment to aaPanel/VPS (no Docker)

See [README-SERVER](../README-SERVER.md). Prepare Node/PM2/Nginx/MySQL/Redis on the target, clone/pull source into a nonpublic directory, create production-only env and storage, `npm ci`, run review-gated migration/seed/admin commands, build and run three PM2 services, connect Nginx/HTTPS, smoke test and configure protected backups. **Manual steps require operator approval**, particularly live migrations and restore.

## 6. What must never be inherited by a new clone

Sessions, users, hashed passwords, secrets, reset links, uploaded media, backup archives, audit events, job queues, cache prefixes or production database dumps. A clone contains only code and safe default templates. Reusing admin email identifier is allowed by policy; reusing initial password is not.

## 7. Acceptance

Fresh clone into distinct project name and DB/Redis/storage, repeat migrations/seed without duplicates, first-admin secure setup, valid login, protected API deny tests, working web/API/worker under tested local configuration and documented PM2/Nginx deployment. Failure must be explicit and resumable, no destructive reinitialization.
