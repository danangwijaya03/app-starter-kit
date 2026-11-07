# Deployment Blueprint — Tanpa Docker

**Updated:** 2026-11-07. **Status:** target rancangan, **bukan panduan executable sampai P16 terimplementasi dan diuji**. Untuk kontrak release lengkap lihat [TRD](TRD.md), [IPD](IPD.md), dan [README-SERVER](../README-SERVER.md).

## Target infrastruktur

- Nginx/aaPanel menerima HTTPS publik dan reverse proxy ke Next.js :3000 serta Hono :4000 yang bind ke loopback.
- PM2 mengelola proses **web**, **api**, dan **worker**, satu process manager per service. Installer CLI dieksekusi on-demand.
- MySQL 8.4 dan Redis berjalan sebagai service native/server, tidak dikontainerisasi.
- Deploy user non-root, private env di luar document root, privilege terpisah untuk runtime, migrasi, backup.
- Node.js patch, architecture, ABI, OS target, dan native modules harus sesuai manifest build yang teruji; jangan mengasumsikan artifact Linux x64 berjalan di ARM.

## Alur build → release

```text
Git commit/tag
  → npm ci (lockfile root)
  → lint/typecheck/unit/integration/negative tests yang relevan
  → compile Next standalone + Hono API + Worker + Installer
  → include static/public + migrations + runtime dependencies
  → release manifest/checksum
  → test isolated artifact (tanpa repository sumber)
  → upload archive ke aaPanel/server
  → verify, preflight, migrate terkontrol, switch, health check
```

Target isi archive:

```text
release/
├── web/                     # standalone server + .next/static + public
├── api/                     # compiled Node API & runtime deps
├── worker/                  # compiled BullMQ worker & runtime deps
├── cli/                     # installer / migrator
├── database/migrations/
├── config/                  # templates only, no production .env
├── README-SERVER.md
└── release-manifest.json    # commit, versions, target OS/arch, checksums
```

Keterangan: bila bundler mengeksternalkan dependency atau native addon, seluruh dependency runtime dan binary yang diperlukan harus ikut artifact. Next standalone harus di-build dengan tracing root monorepo yang benar. Implementer wajib tes proses dari folder hasil ekstraksi yang **tidak** memerlukan source repository.

## Server layout contoh

```text
/srv/apps/app-starter-kit/
├── releases/
│   ├── 2026-11-07-release-a/
│   └── 2026-11-08-release-b/
├── current -> releases/2026-11-08-release-b/
└── shared/
    ├── env/
    ├── media/
    ├── backups/
    └── logs/
```

Nama dan path final mengikuti installer contract yang telah diuji. `shared/env`, logs, media private dan backups tidak boleh tersedia sebagai static file publik.

## Rute proxy yang wajib

| Public | Reverse proxy |
|---|---|
| `/api/auth/*` | Hono `127.0.0.1:4000` |
| `/api/v1/*` | Hono `127.0.0.1:4000` |
| Semua route lain | Next.js `127.0.0.1:3000` |

Nginx harus mempertahankan host/proto yang tervalidasi serta path API. Session cookie same-origin; verifikasi konfigurasi Secure/HttpOnly/SameSite, CSRF, upload limit, proxy timeout, health endpoint, dan rate limiting. Jangan expose port 3000/4000/MySQL/Redis ke publik.

## Tahapan deployment terkontrol

1. Upload archive baru ke **folder release baru** dan cocokkan checksum/manifest.
2. Lakukan preflight Node runtime, arsitektur, layanan, env, disk, permission, dan koneksi DB/Redis.
3. Verifikasi schema compatibility dan persetujuan operator untuk migration berisiko; backup yang memadai sebelumnya.
4. Eksekusi migrator/seed idempotent sesuai kontrak installer; bootstrap admin hanya fresh install dengan secret lokal.
5. Jalankan/update service via satu process manager, lalu alihkan symlink `current` secara aman.
6. Lakukan HTTP health, auth smoke, queue/worker health, dan error log check.
7. Saat gagal, hentikan rollout; rollback aplikasi lewat symlink **hanya bila schema backward-compatible**. Bila migration tidak compatible, gunakan recovery runbook yang disetujui operator; jangan mengembalikan DB secara otomatis.

## Larangan

- Jangan Docker di production.
- Jangan hardcode credentials, secret, bootstrap password, atau token di source/release archive.
- Jangan tes restore, `drop database`, destructive migration atau live credential rotation pada production.
- Jangan mengklaim deployment siap sebelum E2E artifact-isolated smoke P16 dan README-SERVER benar-benar direproduksi.
- Jangan menjalankan dua process manager (aaPanel Node Project dan PM2) untuk proses/port yang sama.

Dokumentasi ini melengkapi, **bukan mengganti**, prosedur khusus di [README-SERVER.md](../README-SERVER.md).
