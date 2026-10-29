# README-SERVER — Instalasi Hasil Build di Server aaPanel (Tanpa Docker)

**Dokumen kontrak untuk release yang akan diimplementasikan pada P16.** Dokumentasi ini disertakan sekarang agar coding agent mengetahui persis installer apa yang harus dibuat. **Belum ada release archive/source code aplikasi yang dihasilkan dalam paket dokumentasi ini.** Perintah `cli/cli.js` dan script release di bawah adalah **target implementasi**; agent wajib memperbarui dan menguji setiap perintah/struktur saat P16 selesai, sebelum menyatakan manual siap dipakai.

## 0. Model operasi

- Server menjalankan **Node.js runtime** untuk Next.js standalone, Hono API dan BullMQ worker; tidak perlu Docker, npm, Turborepo atau TypeScript untuk menjalankan hasil build.
- MySQL dan Redis adalah service server (misalnya instalasi aaPanel atau paket sistem) dengan user dan kontrol akses yang tepat.
- aaPanel/Nginx menangani domain, SSL, dan reverse proxy dari satu origin.
- PM2 mengelola **tepat satu set proses** (`starter-web`, `starter-api`, `starter-worker`). Jangan menambahkan instance kedua melalui aaPanel Node Project jika menyebabkan dua process manager mengontrol port yang sama.
- Aplikasi/secret/media/backup berada di luar public document root. Pengguna Linux yang menjalankan service tidak boleh `root`.
- Guide ini berlaku untuk sistem Linux kompatibel dengan manifest artifact. Untuk server ARM64, pilih artifact `linux-arm64` yang benar-benar dibangun/diuji untuk target; tidak bisa menggunakan binary native `linux-x64` begitu saja.

## 1. Persyaratan dan pemeriksaan sebelum upload

| Requirement | Minimal validasi |
|---|---|
| Node.js | Node 24 LTS, patch/ABI sesuai release manifest |
| MySQL | 8.4 LTS, InnoDB, charset utf8mb4 |
| Redis | Versi kompatibel dengan BullMQ yang dipin dan diuji |
| PM2 | Installed under deployment user; startup on reboot |
| Nginx & SSL | aaPanel website configuration, HTTPS valid |
| Disk/RAM | Cukup untuk archive, extract, migrations, media, backup + staging restore |
| DNS | Domain mengarah ke IP server |
| User | Deployment/service user non-root dengan permission least privilege |
| Archive | `.tar.gz`, detached SHA256, release manifest, server README |

Target preflight commands (read-only):

```bash
node --version
npm --version
uname -s
uname -m
mysql --version
redis-cli --version
pm2 --version
nginx -v
```

Jika command tidak tersedia, pasang komponen tersebut melalui aaPanel atau package manager sesuai distribusi Linux. Jangan menginstal komponen duplikat bila aaPanel sudah mengelolanya. Pastikan Node yang dipakai PM2 sama dengan Node yang kompatibel dengan release.

## 2. Layout final di server

Contoh lokasi **di luar public document root**:

```text
/srv/apps/codelight-starter/
├── releases/
│   ├── v1.0.0/
│   │   ├── web/
│   │   ├── api/
│   │   ├── worker/
│   │   ├── cli/
│   │   ├── database/migrations/
│   │   ├── config/
│   │   ├── release-manifest.json
│   │   └── README-SERVER.md
│   └── v1.0.1/
├── current -> releases/v1.0.1
└── shared/
    ├── env/{web.env,api.env,worker.env,installer.env}
    ├── media/
    ├── backups/
    ├── logs/
    └── runtime/
```

`current` is a symlink; `shared` persists across releases. The production service must never serve files inside `shared/env` or `shared/backups` to web users. Dedicated backup encryption keys remain outside archive and preferably outside same server (secret manager), and external backup copy is recommended.

Create top-level directories under a dedicated app user after reviewing local policy. **Example only; replace username/group and use `sudo` with appropriate operator permission:**

```bash
sudo install -d -m 750 -o appuser -g appuser /srv/apps/codelight-starter
sudo install -d -m 750 -o appuser -g appuser /srv/apps/codelight-starter/releases
sudo install -d -m 700 -o appuser -g appuser /srv/apps/codelight-starter/shared/env
sudo install -d -m 750 -o appuser -g appuser /srv/apps/codelight-starter/shared/media
sudo install -d -m 700 -o appuser -g appuser /srv/apps/codelight-starter/shared/backups
sudo install -d -m 750 -o appuser -g appuser /srv/apps/codelight-starter/shared/logs
sudo install -d -m 700 -o appuser -g appuser /srv/apps/codelight-starter/shared/runtime
```

The exact required write permissions of API and worker should be tested; do not grant blanket `777`.

## 3. Upload dan validasi artifact

1. Upload archive and `.sha256` through aaPanel File Manager, SFTP or SCP to an operator-controlled staging directory outside the public web root.
2. Verify archive SHA256 against a **trusted release checksum received through a separate/approved channel**. A checksum alongside an untrusted archive does not establish authenticity by itself.
3. Inspect `release-manifest.json`: version, git commit, OS, arch, Node major, expected SQL schema version, component checksums; reject mismatch.
4. Extract into *new* directory `releases/vX.Y.Z` with no overwrite of an existing release. Before extraction, validate archive contents against path traversal and symlink escapes. The release installer must implement this check.
5. Verify component checksums. Only then create/update `current` via controlled installation command.

Illustrative manual commands after archive verification (use correct names and do not overwrite):

```bash
cd /srv/apps/codelight-starter
sha256sum -c /path/to/release.sha256
mkdir releases/v1.0.0
# Only after reviewing archive contents and secure extraction policy:
tar -xzf /path/to/codelight-starter-v1.0.0-linux-x64.tar.gz -C releases/v1.0.0
```

A production installer should verify safe extraction and file counts automatically. A release archive is not assumed trustworthy just because `tar` can open it.

## 4. MySQL setup (aaPanel)

In aaPanel: **Databases → MySQL → Add Database** (labels may change with aaPanel version). Create a unique database and application user for this project, `utf8mb4`, localhost-only access if on the same server. Use a privileged migration user only for installer migrations, not general API runtime.

Recommended distinct DB roles:
- Runtime DB user: minimum CRUD permissions required, no schema/admin privileges.
- Migration DB user: narrowly scoped DDL/migration privileges, used only for deliberate upgrades.
- Backup service user: minimum read/dump privileges and consistent snapshot requirements.

Avoid public exposure of port 3306. Confirm DB version, connectivity and migrations journal before seed/restore.

## 5. Redis setup

Install/enable Redis using the server's package or aaPanel facility. Bind to loopback/private interface; configure authentication if appropriate, persistence/restart, and restrict filesystem/network access. Do **not** expose port 6379 on public internet.

```bash
redis-cli -h 127.0.0.1 PING
# expected: PONG (if auth is configured, use a secure private client config)
```

Queue health is verified by installer/worker, not merely by seeing `PONG`.

## 6. Runtime environment and private secrets

After upload, create service-specific `.env`-format files owned by service account. **Never place real values in Git or artifact.** Example paths:

```text
shared/env/web.env
shared/env/api.env
shared/env/worker.env
shared/env/installer.env
```

Illustrative `web.env`:

```dotenv
NODE_ENV=production
HOSTNAME=127.0.0.1
PORT=3000
API_INTERNAL_BASE_URL=http://127.0.0.1:4000
```

Illustrative `api.env`:

```dotenv
NODE_ENV=production
HOST=127.0.0.1
PORT=4000
APP_PUBLIC_URL=https://app.example.com
BETTER_AUTH_URL=https://app.example.com
BETTER_AUTH_SECRET=REPLACE_WITH_UNIQUE_PRIVATE_SECRET
DATABASE_URL=mysql://APP_RUNTIME_USER:PRIVATE_PASSWORD@127.0.0.1:3306/APP_DB
REDIS_URL=redis://127.0.0.1:6379
MEDIA_STORAGE_PATH=/srv/apps/codelight-starter/shared/media
BACKUP_STORAGE_PATH=/srv/apps/codelight-starter/shared/backups
```

`worker.env` has only the DB/Redis/storage/backup key identifiers needed for worker; `installer.env` includes migration credentials used temporarily under appropriate file access.

Do not leave placeholder values in live server. Configure proper file permissions (e.g. `chmod 600`) and ensure shell commands/process lists/logs do not expose secret strings. For passwords containing `@`, `#`, `:` or `/`, encode them correctly within URI fields or use separated DB connection variables; never concatenate unescaped password into a URL. A better alternative is an application config object built from environment fields.

### Bootstrap secret

Initial email: **`admin@codelight.id`**, role **`super_admin`**. Supply the user-chosen initial password through a secure non-echo terminal prompt or protected one-time secret file used by installer. **Do not store the actual initial password in `README-SERVER.md`, package, code or logs.** For production, use a newly generated unique password instead of a reused development password. Require password change on the first login and remove the temporary installer secret after successful onboarding. The bootstrap action is idempotent and must not reset an existing admin password.

## 7. First-time installation order (CRITICAL DEPENDENCY)

Do not create admin before schema, roles and permissions are present.

```text
Preflight MySQL and Redis
   ↓
Verify release manifest / runtime / writable storage
   ↓
Apply versioned Drizzle migrations
   ↓
Sync permission registry
   ↓
Seed system roles + Salt & Pepper + safe default settings/menus
   ↓
Bootstrap first administrator
   ↓
Start Hono API, worker, Next.js
   ↓
Nginx + HTTPS and installation smoke tests
```

**Target CLI contract to be implemented and tested by P16** (run under deployment user from project directory; not executable now):

```bash
cd /srv/apps/codelight-starter
node --env-file=shared/env/installer.env current/cli/cli.js preflight
node --env-file=shared/env/installer.env current/cli/cli.js migrate --check
node --env-file=shared/env/installer.env current/cli/cli.js migrate --apply
node --env-file=shared/env/installer.env current/cli/cli.js permissions:sync --apply
node --env-file=shared/env/installer.env current/cli/cli.js seed
node --env-file=shared/env/installer.env current/cli/cli.js bootstrap-admin
node --env-file=shared/env/installer.env current/cli/cli.js verify
```

Commands must use installation lock and failure exit codes. On production, destructive or incompatible migration requires explicit deployment approval; installer must not assume consent. `bootstrap-admin` must read protected secret/prompt, use Better Auth-compatible credential creation, set user `active`, `must_change_password=true`, and assign protected `super_admin` role; second run must leave existing credentials unchanged.

## 8. Start the three Node services with PM2

Only after CLI is implemented and runtime entrypoints verified. Target PM2 ecosystem config is packaged with artifact; an illustrative non-secret scaffold is in `templates/ecosystem.config.cjs.example`.

```bash
cd /srv/apps/codelight-starter
pm2 start current/config/ecosystem.config.cjs
pm2 status
pm2 logs starter-api --lines 100
pm2 logs starter-web --lines 100
pm2 logs starter-worker --lines 100
pm2 save
```

Configure `pm2 startup` for deployment user after inspecting output and distro-specific startup instructions. Set `cwd`/interpreter/`--env-file` per process. Worker does not listen on HTTP port. Bind web/API to loopback addresses; ensure processes are not also launched independently through aaPanel Node.js Project. For all process definitions use versioned release `current` with reload/restart behavior tested after symlink change.

## 9. Nginx reverse proxy in aaPanel

1. In aaPanel create website/domain (e.g., `app.example.com`) with Nginx; enable SSL certificate and force HTTPS.
2. Configure route `/api/` to `http://127.0.0.1:4000` **without stripping the `/api` path**.
3. Configure remaining `/` to `http://127.0.0.1:3000`.
4. Pass `Host`, `X-Real-IP`, `X-Forwarded-For` and `X-Forwarded-Proto`. Set reasonable upload/timeouts; do not expose `.env`/backups.
5. Test `nginx -t` and reload only after syntax passes. Do not blindly overwrite aaPanel-generated SSL directives.

An **illustrative fragment**, not full aaPanel site config:

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:4000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    client_max_body_size 20m;
}
location / {
    proxy_pass http://127.0.0.1:3000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

The path behavior is important: `proxy_pass http://127.0.0.1:4000;` keeps `/api/...`, while adding a trailing slash can rewrite the prefix depending on location. Let aaPanel manage TLS/security settings; use an inclusion mechanism that doesn't duplicate other `location /` blocks. Test auth cookies with HTTPS to verify trusted origins and secure cookie flags.

## 10. Installation verification

After all services start, validate:

```bash
curl --fail --silent http://127.0.0.1:4000/api/health/live
curl --fail --silent http://127.0.0.1:3000/health
curl -I https://app.example.com/login
pm2 status
```

The `/health` routes must be implemented before those checks become operational; optional ready checks should be restricted if exposing database status. Manual smoke checklist:

1. Open `/login` on HTTPS domain; sign in as initial admin.
2. First login **must force password change**, no access to CMS/User/Settings before completion.
3. Verify Dashboard, Manage Content, Manage User, Setting sidebar order.
4. Create role with a subset of CMS permissions; log in as role user; direct forbidden API returns 403.
5. Create draft → verify not visible public → publish → verify live route and SEO.
6. Upload media → restart API → verify file persists.
7. Update application name/logo/theme → refresh website, confirm new runtime branding.
8. Verify worker can enqueue and process a harmless test job; backups work to protected storage.
9. Ensure no private `.env` or backup accessible over HTTP.

On failure, capture request ID and redact secrets from logs. Do not continue to announce deployment as successful.

## 11. Backup setup and recovery policy

Configure protected local backup directory, encryption key reference, retention, external copy destination and storage alerting. MySQL logical dump is performed by worker with safe private credentials (not command-line plaintext). For a truly recoverable app snapshot, include media or explicitly label database-only coverage. Never schedule unattended restoration. Before first production launch, **test a managed backup by restoring to an isolated test database**. Store restore journal outside database; repair/recovery steps in `docs/agent/RUNBOOK.md` and live version of this server guide.

## 12. Application update (not initial install)

1. Produce a new release archive with frozen compatible dependencies and passing artifact-isolated smoke tests.
2. Upload to new `releases/vX.Y.Z` directory; checksum and compatibility verification.
3. Review migration compatibility with current app; create verified pre-update backup where warranted; avoid DDL during traffic/backup.
4. Pause writes/worker if migration requires maintenance; apply reviewed migrations with installer lock.
5. Atomically switch `current` symlink to new version, update/reload PM2 service processes.
6. Check web/API/worker health, auth cookie, key user flows, job queue and published content.
7. If checks fail: do not blindly roll back database. Revert **code only when schema backward-compatible**; otherwise remain in maintenance and follow operator-directed recovery using verified snapshot.
8. Keep at least one known-good release, rotate old releases after recovery policy allows.

**Do not rerun bootstrap admin during routine updates unless an explicit check requires it**; even if invoked, code must be idempotent and cannot reset credentials.

## 13. Rollback troubleshooting

| Symptom | Inspect first | Safe recovery |
|---|---|---|
| 502 on website | PM2 web, port 3000, Nginx logs | Restart correct process after identifying issue |
| 502 on API | PM2 API, port 4000, `api/health/live` | Check runtime env/entrypoint; no DB reset |
| CSS/JS 404 | `.next/static` packaged path | Rebuild/repackage correct Next tracing/assets |
| Login loop / failed cookie | BETTER_AUTH_URL/trusted origin, SSL, forwarded headers | Fix configuration; test auth from same origin |
| DB refused | MySQL service, hostname/user grants, UTC setting | Fix private connection; no schema recreation |
| Migration failed | Migration journal and exact SQL error | Pause deploy; review and repair, do not auto-drop |
| Media 404 | `shared/media` path, ACL, storage key | Restore missing files only from verified media backup |
| Queue stuck | Redis, worker PM2, job status | Reconcile idempotent jobs; never auto-retry restore |
| Theme old after save | Settings version, revalidation/cache | Invalidate allowed cache and inspect server logs |
| 403 role grant | Registry sync, DB grants, session status | Diagnose policy, not disable middleware |
| Restore failed | External restore journal, maintenance state | Operator-led recovery from pre-restore backup |
| Port conflict | Other aaPanel/PM2 process | Stop only duplicate service after confirmation |
| Server is ARM64 | Release manifest `targetArch` | Build compatible ARM artifact |

Useful non-destructive commands: `pm2 status`, `pm2 describe starter-api`, `pm2 logs ...`, `ss -ltnp`, `nginx -t`, `journalctl -u redis...` depending on distro. Do not paste secrets into support logs. Record exact versions and request IDs.

## 14. Security and operational checklist

- [ ] HTTPS/SSL enabled, HTTP redirected to HTTPS.
- [ ] MySQL/Redis bound private/localhost and firewalled.
- [ ] Service non-root, restrictive file permissions; no public `shared/` exposure.
- [ ] No real secrets in archive, repo, process list or logs.
- [ ] Unique per-project auth secret, DB password and backup encryption key.
- [ ] Installer bootstrap password supplied securely, forced change completed.
- [ ] Public signup disabled; protected super-admin last-holder invariant tested.
- [ ] Rate limits, secure cookies, CSRF and headers verified behind reverse proxy.
- [ ] Verified offsite backups and isolated restore test documented.
- [ ] PM2 restart-on-boot and process log rotation configured.
- [ ] Release checksum and OS/arch/runtime compatibility validated.
- [ ] Maintenance and rollback plan rehearsed; no automatic restore retries.

## 15. Release documentation change rule

At P16, agent must update this file to match **actual implemented artifact names, CLI syntax, filesystem layout, PM2 config and tested Nginx config**; include tested stdout/exit conditions without private values. If steps fail, leave release blocked. A documentation-only template is not evidence that an application is installed.