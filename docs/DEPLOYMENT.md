# Deployment Blueprint — Artifact Tanpa Docker

**Status: target, belum executable.** Tidak ada API/worker/release artifact produksi saat reset dokumentasi 2026-11-07. Seluruh command, manifest dan scripts implementasi harus diverifikasi pada fase P15–P16 sebelum dipakai live.

## Target runtime

- **Nginx/aaPanel:** terminasi HTTPS; `/` dan route aplikasi → Next.js pada `127.0.0.1:3000`; `/api/*` → Hono `127.0.0.1:4000`.
- **Node.js:** exact version / arch / ABI sesuai build yang diuji. Web Next standalone, API compiled, worker compiled adalah proses terpisah dikelola PM2 **atau** systemd (hindari dua process manager untuk satu proses).
- **MySQL 8.4 dan Redis:** service native pada host/private network, tanpa Docker, tidak publik.
- **Secrets/storage:** shared private, bukan di `public/`, artifact, atau Git.

## Pipeline yang harus dibangun

```text
Git commit/tag
 → npm ci dari root lockfile
 → lint / typecheck / unit / integration / negative tests
 → build Next standalone + static/public
 → compile Hono API + worker + production dependencies
 → include versioned Drizzle migrations & optional migration runner
 → checksums + manifest (SHA commit, OS/arch, Node, entrypoints, migrations)
 → smoke test hasil ekstraksi tanpa repository sumber
 → upload ke server, preflight, migrasi terkontrol, switch, health checks
```

```text
/srv/apps/app-starter-kit/
├── releases/
│   ├── release-001/
│   └── release-002/
├── current -> releases/release-002/
└── shared/
    ├── env/
    ├── media/
    ├── backups/
    └── logs/
```

Artifact release contoh: `web/`, `api/`, `worker/`, `database/migrations/`, `release-manifest.json`, `config/examples/`. Sertakan installer/CLI hanya jika diterapkan dan diuji. Packaging Next harus mengatur tracing root monorepo dan menyertakan `.next/static` serta `public`. Jika native modules atau dependencies di-external-kan, wajib ikut artifact dan cocok dengan target.

## Safe rollout / rollback

1. Build dan test pada lingkungan yang kompatibel dengan server tujuan.
2. Upload ke folder release baru; verifikasi manifest, checksum, permission, secret references.
3. Periksa health MySQL/Redis dan kompatibilitas migrasi; ambil backup sesuai risiko.
4. Jalankan migrasi hanya setelah konfirmasi operasi aman dan persetujuan operator untuk operasi high-risk.
5. Jalankan/reload proses yang benar, alihkan `current`, lalu HTTP/auth/job smoke check.
6. Jika gagal, hentikan rollout. Rollback symlink hanya jika migrasi schema backward-compatible; recovery database perlu prosedur khusus dan persetujuan operator.

**Keamanan:** cookie session `HttpOnly`/`Secure`, CSRF defense, validasi forwarded host/proto, least-privilege service accounts, API/database/Redis loopback/private, rate limits dan log tanpa secret. Backup/restore produksi bukan bagian dari test otomatis.

Definition of Done deployment: seluruh service berjalan dari archive tanpa checkout source, dengan instruksi reproduktif untuk fresh install, update, rollback dan pemeriksaan pascadeploy.

Rujukan: [ARCHITECTURE.md](ARCHITECTURE.md), [ROADMAP.md](ROADMAP.md).
