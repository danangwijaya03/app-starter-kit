# README-SERVER — Manual Clone/Build/Deploy ke aaPanel (Tanpa Docker)

**Ditujukan untuk: USER / ADMINISTRATOR SERVER.** Ini adalah prosedur target untuk aplikasi selesai; saat ini source baru berisi baseline Next.js. **Bukan installer otomatis.** Perintah workspace/migration/PM2 di sini adalah contoh target sampai script/konfigurasi yang bersangkutan dibuat dan diuji pada fase P16. Jangan mengeksekusi perintah yang belum ada atau pada production DB tanpa review.

## 1. Topologi deployment

- Node.js 26 (gunakan versi patch yang diuji dengan dependency), npm, PM2.
- MySQL 8.4 dan Redis tersedia sebagai layanan native/aaPanel (tanpa Docker).
- Next.js web di loopback `127.0.0.1:3000`, Hono API `127.0.0.1:4000`, BullMQ worker tanpa port publik.
- Nginx aaPanel: `/api/*` ke API dengan path tetap; selain itu ke web. HTTPS dan forwarded headers/cookie diuji.
- Aplikasi, `.env`, media, backup dan log **di luar public webroot**. User deploy non-root dengan permission minimum.

## 2. Folder manual — tanpa release directory/symlink manager

```text
/srv/apps/my-project/
├── apps/              # cloned source: web/api/worker after monorepo P01
├── packages/
├── infra/
├── package.json
├── package-lock.json
├── .env                # private, never committed
└── storage/            # private media, backups, logs, temp
```

Gunakan path terpisah per proyek; dapat memilih layout lain dengan prinsip same security. **Tidak perlu** `releases/`, `current` symlink, archive manifest, `apps/installer`, atau installer.env.

## 3. Clone dan konfigurasi pertama

```bash
# Run as unprivileged deployment user, in approved private directory:
git clone <authorized-project-repository-url> my-project
cd my-project
node --version
npm --version
npm ci
```

Set environment production secara manual dari `.env.example` (setelah file tersebut tersedia). Siapkan database MySQL dan user dengan grants minimum untuk runtime; kredensial migration dengan hak terbatas yang terpisah bila perlu. Set unique Redis prefix/queue, secret auth acak kuat, origin/hostname, private media and backup paths, restrictive file permissions. **Never copy** live users/sessions/media/backups/secrets from the starter.

**Jangan gunakan** `npm run db:push` ke production tanpa review; pakai migrasi versi yang telah diperiksa, bukan schema overwrite.

## 4. Initial database + admin setup — target npm scripts

**Planned (not yet executable on current root Next scaffold):**

```bash
npm run db:migrate:check
npm run db:migrate
npm run permissions:sync
npm run db:seed
npm run setup:admin
npm run setup:verify
```

Urutan: preflight DB/environment → reviewed migration → permission registry sync → idempotent roles/system seed → one-time admin setup with non-echo private password input → verify actual login and first-password-change. Never use plaintext credentials in arguments, logs, scripts or Git. Re-run must not reset existing password or duplicate privileged users.

If an operation fails, stop, inspect migration history and test fixtures; do not drop a schema, apply a guessed fix or re-seed blindly.

## 5. Build, PM2, Nginx

**Target** after P01/P16 scripts/PM2 config are implemented:

```bash
npm run build
pm2 start infra/pm2/ecosystem.config.cjs
pm2 status
pm2 logs --lines 50
```

PM2 must use the tested actual built entrypoints for Next.js, Hono and worker, private env, independent restart policies and graceful stop. Do **not** assume these commands work until scripts exist. Nginx template will be `infra/nginx/locations.conf` after P16; keep app ports loopback, enforce HTTPS, test `/api/auth/*` cookies, headers, timeout and upload limit.

Use a deployment-specific service user rather than `root`; configure startup/restart only after verifying the real service paths. Use local health checks and a login/RBAC smoke test to verify after deployment.

## 6. Manual update with recovery plan

1. Record currently running commit, modified/uncommitted files, exact service/environment versions and backup status.
2. Ensure an independently verified backup and recovery access before any incompatible schema change; plan safe maintenance/drain if writes/worker jobs would conflict.
3. Review migration SQL against a separate test MySQL DB, compatibility and potential irreversible data operations; **production approval is separate from code review**.
4. Pull/fetch a trusted target commit with `git pull --ff-only` only if branch has no conflicting local edits; never force-reset live source.
5. Run `npm ci` and actual production build; migrate only after approval, then restart/reload PM2 with checked entrypoints.
6. Verify auth, permissions, CMS, uploads, worker, backup health and logs. If code is bad, a Git checkout to the previous commit is a **manual source rollback**, not database rollback.

## 7. Backup, restore, observability

Backups must be protected, encrypted and regularly verified by importing into a **disposable isolated database**, not directly into a live instance. Restore requires re-auth, explicit approval, maintenance/lock, checked archive and an operator-managed recovery plan. Never auto-repeat a destructive restore.

Logs must redact tokens/passwords. Prefer structured logs with audit events for sensitive writes. Optional external observability should never be required for base installation.

## 8. Verify before calling this deployment production-ready

- [ ] Three processes start, stop and survive restart using tested build scripts.
- [ ] MySQL/Redis and storage are isolated per project.
- [ ] Login, logout, password reset, first-admin password change and 401/403 paths pass.
- [ ] CMS public renders only published revision; private media restricted.
- [ ] Negative tests for uploads, permissions, idempotent seed and migration drift pass.
- [ ] Verified encrypted backup, isolated restore test and manual recovery plan exist.
- [ ] Full HTTPS/Nginx /api proxy and cookies validated.
- [ ] No Docker, installer, archive version manager, secret in source or deployment by coding agent without approval.

Reference: [Manual Clone Setup](docs/MANUAL-CLONE-SETUP.md), [Operations Patterns](docs/references/OPERATIONS.md), [P16 Tasks](docs/agent/phases/P16-manual-clone-and-deployment.md) (phase filename retained for compatibility; its content now targets manual deployment).
