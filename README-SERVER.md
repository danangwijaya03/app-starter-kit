# README-SERVER — Manual aaPanel Deployment for Modular Core v2 (No Docker)

**Ditujukan untuk: USER / ADMINISTRATOR SERVER.** **Status:** approved target procedure; current Git source contains static Next.js preview only. Most workspace, migration, recovery and PM2 commands are **not yet executable** until corresponding tasks are implemented/tested. No project installer, archive release manager, versioned symlink switch or one-click recovery.

## 1. Core topology, optional runtimes

| Service | Core-only production | When optional module enabled |
|---|---|---|
| Node.js Next.js web | REQUIRED, private loopback :3000 | same |
| Node.js Hono API | REQUIRED, private loopback :4000 | same |
| MySQL 8.4/Drizzle | REQUIRED | one central schema/journal for all modules |
| Redis | NOT REQUIRED | required when `requiresJobs=true` |
| BullMQ worker via PM2 | NOT STARTED | only if enabled modules require jobs |
| LocalFs media | static fallback branding only | enable private/public media when Media selected |
| Independent encrypted offsite backup + CLI recovery | **REQUIRED before Core production** | same even if Operations UI absent |

Nginx aaPanel terminates HTTPS, forwards `/api/auth/*` and `/api/v1/*` to Hono without rewriting the route, sends `/*` to Next. Preserve trusted forwarded host/proto and secure same-origin cookies. Web/API and DB ports remain private. Core-only readiness must not fail because Redis is absent.

## 2. New project via manual clone

```bash
git clone <authorized-project-repo-url> my-project
cd my-project
node --version
npm --version
npm ci
```

Create private `.env` and project-unique DB user/name, media/backups/storage directory and optional Redis prefix if jobs selected. Choose operator-specific admin email and secret; do not use a universal address/password or copy old project data. Use an unprivileged deployment user, nonpublic root such as `/srv/apps/<project>/`.

Static `enabledModules` is source-controlled; validate module dependency closure and version hash parity between web/API on build/start. CMS requires Media. Disabled modules must have no route, menu, permission grant or OpenAPI entry; module selection **does not skip database migrations**.

## 3. Manual migration and bootstrap (target scripts only)

```bash
npm run db:migrate:check
npm run db:migrate
npm run permissions:sync
npm run db:seed
npm run setup:admin
npm run setup:verify
```

Review generated SQL/migration compatibility, use distinct privileged migration credentials, ensure separate test/prod targets. Seeds are idempotent and permission grants revoked on disable are not auto-restored when modules re-enabled. `setup:admin` uses secure non-echo operator input (email + password) and never resets existing admin.

## 4. Manual build and PM2/Nginx

```bash
# Commands become real only after P16 setup/build tasks:
npm run build
pm2 start infra/pm2/ecosystem.config.cjs
pm2 status
```

Start **web+API**, not three processes unconditionally. Start worker/Redis only for configured Jobs capability and verify queue health separately. Validate PM2 entrypoint paths against actual build output. Nginx and TLS run through aaPanel; test `/api/health/live`, `/api/health/ready`, `/api/health/subsystems` and actual login cookie/401/403. Never expose private env, backup, media or logs from webroot.

## 5. Independent backup + disaster recovery CLI

Production requires a separate, operator-controlled CLI (target implementation under `tools/recovery`), Linux timer, consistent MySQL + LocalFs snapshot, restic encrypted offsite repository, manifest/checksum and controlled retention/GC. Operator verifies backup age and performs **isolated staging restore drill** before declaring production ready.

A destroyed VPS or broken Hono/Redis must not prevent restoring from offsite backup. Production cutover is **manual only**, after staging validation, approval, external journal, maintenance and a pre-cutover recovery snapshot. No HTTP `POST /backups/:id/restore` endpoint, no BullMQ automatic restore, no user-facing one-click production restore.

RPO **target** 24 h and RTO **target** 8 h; do not claim achieved until an actual drill has measured them. Optional Operations UI may show status/freshness but is not the recovery authority.

## 6. CI, manual deploy and safe update

CI must automatically run scoped checks, Core-only no-Redis smoke, security negatives and dependency/license checks. Production deployment is **manual** from an approved commit SHA with proven CI result and migration plan. Verify offsite backup, stage migration in isolated MySQL, obtain operator approval, `git pull --ff-only` only on clean tree, run tested npm install/build/migrate commands, restart PM2, validate health/login/RBAC and monitor logs.

A manual Git checkout to an older code commit **cannot roll back the MySQL schema**. If incompatible migration/failed deploy, remain in maintenance and follow operator recovery journal; no blind reset/drop/auto retry.

## 7. Release gates

- **Core M2/P16-11**: Next+Hono+MySQL Auth/RBAC/dashboard/settings/theme/audit, independent encrypted offsite backup and recovery CLI, manual deploy/CI, security review. **Redis, Worker, Media, CMS, Operations disabled**.
- **Media M3/P09-07**: public/private file lifecycle + negative cases.
- **CMS M4/P11-07**: requires certified Media; SSR published-only and private preview.
- **Jobs/Operations M5/P13-06/P14-07**: Redis/BullMQ resilience and optional status UI.
- **Full module matrix M6/P16-12**: selected combinations, config hash, invalid dependencies and clean clone tests.

**Do not call the feature deployed** until real scripts, infrastructure, tests, and reviews are observed. See [Architecture Operations](docs/architecture/OPERATIONS-RUNBOOK.md), [Server v2 addendum](docs/revisions/README-SERVER-v2-ADDENDUM.md), [Manual Clone](docs/MANUAL-CLONE-SETUP.md).
