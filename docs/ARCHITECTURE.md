# Architecture Blueprint — Next.js Monorepo Starter Kit

**Status:** target design, belum terimplementasi penuh. **Updated:** 2026-11-07. Dokumen ini ringkasan arsitektur; ketentuan teknis rinci tetap di [TRD](TRD.md), [BSD](BSD.md), [AFD](AFD.md), dan [implementation contracts](agent/IMPLEMENTATION-CONTRACTS.md).

## Baseline yang benar

Repository `danangwijaya03/app-starter-kit` saat ini **bukan clean/empty repo**: Next.js 16.4.3 + React 19.3.0, TypeScript, Tailwind v4, npm lockfile berada di **root**. P01 harus **memindahkan** app tersebut ke `apps/web` tanpa menjalankan ulang `create-next-app` atau menimpa source existing. Penambahan dokumentasi ini **tidak** memigrasikan source.

## Target proses dan stack

| Komponen | Lokasi target | Runtime / tanggung jawab |
|---|---|---|
| Web | `apps/web` | Next.js App Router; page, SSR, komponen, form, dan konsumsi API |
| API | `apps/api` | Hono Node.js; authentication, authorization, validasi, business API |
| Worker | `apps/worker` | Node.js + BullMQ; asynchronous jobs, retry, reconciliation |
| Installer CLI | `apps/cli` | Perintah instalasi/migrasi/seed dan operasi terkontrol saat release |
| Database | `packages/db` | MySQL 8.4 + Drizzle + mysql2; schema, migrations, transaction helper |
| Core | `packages/core` | Business services reusable yang tidak bergantung framework HTTP |
| Auth | `packages/auth` | Better Auth dan pembatasan server-side |
| Contracts | `packages/contracts` | Zod schema, tipe, kontrak API aman dibagi |
| UI | `packages/ui` | Komponen reusable + Salt & Pepper tokens |
| Queue | `packages/queue` | Job contracts dan konfigurasi BullMQ bersama |
| Configuration | `packages/config` | Shared configuration tanpa secret hardcoded |

Struktur di atas adalah **target logis**, bukan daftar file yang sekarang sudah ada. Bila implementasi existing memiliki nama package berbeda, periksa [implementation contracts](agent/IMPLEMENTATION-CONTRACTS.md), task card P01, dan dokumen spesifikasi sebelum memutuskan rename.

**Toolchain:** npm/npx dan satu `package-lock.json` root, Node.js 26.x dengan patch yang diuji, TypeScript strict. Repository sebelumnya memutuskan menggunakan **Turborepo sebagai orchestrator monorepo**; npm workspaces tetap menjadi package manager. Jangan menghapus atau mewajibkan perubahan orchestrator tanpa memperbarui task registry, task cards, dan menjalankan verifikasi.

## Request/data flow

```text
Browser HTTPS
   |
   v
Nginx / aaPanel
   |-- /, /admin/*, CMS public --> Next.js standalone :3000
   |-- /api/auth/*, /api/v1/* --> Hono API :4000
                                      |-- MySQL service
                                      |-- Redis / BullMQ
Worker (proses terpisah) <----------- Redis queue
   |-- MySQL / private storage (minimum privileges)
```

- Browser menggunakan **satu public origin**; Nginx meneruskan path `/api/*` ke Hono, selain itu ke Next.js. Tidak perlu menggandakan business API dalam Next.js route handler.
- Web boleh import `ui`, `contracts` dan `config`; **tidak** boleh import `db`, `worker`, atau kredensial. API mengakses `auth`, `core`, `db`, `contracts`, dan `queue`. Worker mengakses `core`, `db`, `queue`.
- API dan Web bisa berkomunikasi menggunakan HTTP internal; jangan mengandalkan client-provided headers untuk identitas. Session cookie memakai `HttpOnly`, `Secure` pada HTTPS, `SameSite` sesuai threat model, CSRF defense, dan forwarded-host validation.
- API/DB/Redis bind ke loopback/private network; hanya Nginx yang menerima trafik publik. Health/liveness endpoints tidak mengekspose detail secret atau database.
- MySQL adalah source of truth; Redis dipakai untuk job queue, bukan pengganti persistence atau backup.

## Authentication, RBAC, modules

- Better Auth menggunakan schema yang **dihasilkan dari versi library terpasang**; custom RBAC disimpan di tabel roles, permissions, user_roles, role_permissions. Jangan menebak vendor schema.
- Session dicek di API; setiap operasi yang membutuhkan grant wajib melakukan **server-side permission check**, bukan sekadar menu disembunyikan. Gunakan permission key kanonik dari [BSD](BSD.md), seperti `users.view`, bukan membuat nomenklatur baru.
- Starter kit default **single-tenant per deployment**. Project turunan harus memiliki secrets, akun, database, media, logs, sessions dan backup yang terisolasi.
- Navigasi utama: **Dashboard, Manage Content, Manage User, Setting**. Default visual: Salt & Pepper `#FFFFFF`, `#D4D4D4`, `#B3B3B3`, `#2B2B2B`; theme dapat diganti per proyek.
- Bootstrap super admin melalui secret instalasi, tanpa password tersimpan di source/dokumentasi. Wajib ganti password setelah login pertama.

## Modul dan cakupan v1

Auth, role/permission, dashboard, user management, CMS halaman/publish/navigation/media, app settings/theme, audit, worker, backup/restore aman, installer/release artifact. Detail behavior, prioritas, dan test ada di [PRD](PRD.md), [AFD](AFD.md), dan [roadmap](ROADMAP.md). Backup/restore adalah workstream lanjutan dengan test database disposable; tidak dijalankan otomatis pada production.

## Keputusan release

Production **tanpa Docker**: build dan verifikasi artifact dalam CI/build environment, lalu upload ke server dengan Nginx, Node.js, PM2 (atau systemd bila diadaptasi secara resmi), MySQL dan Redis yang berjalan sebagai service native. Artifact harus mencakup web standalone beserta static/public, compiled API, worker, installer, migrations dan manifest. Rujuk [deployment guide](DEPLOYMENT.md) serta [README-SERVER](../README-SERVER.md).

**Sumber kebenaran:** dokumentasi ini adalah peta ringkas; jika menemukan pertentangan, catat mismatch dan review keputusan sebelum mengubah implementasi. Status task aktual hanya dari [TASKS.yaml](agent/TASKS.yaml).
