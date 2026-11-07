# Architecture — Next.js Monorepo Starter Kit

**Status: blueprint, belum diimplementasikan.** Tanggal reset: 2026-11-07. Dokumen ini berlaku untuk pengembangan pada branch `dev`.

## 1. Baseline dan tujuan

Repository ini **sudah** mempunyai source awal Next.js 16.4.3 + React 19.3.0 di root (`app/`, `public/`, `package.json`, `package-lock.json`). Jangan jalankan `create-next-app` lagi. Implementasi P01 akan **memindahkan** aplikasi existing ke `apps/web`, bukan membuat ulang.

Tujuan: starter kit reusable untuk aplikasi dashboard/CMS/operasional dengan MySQL mandiri, API Hono, worker, RBAC, serta deployment artifact tanpa Docker. **Single-tenant per deployment**; setiap proyek turunan memakai database dan secret terpisah.

## 2. Stack yang ditargetkan

| Area | Keputusan |
|---|---|
| Monorepo | npm workspaces; satu root `package-lock.json`; npm/npx |
| Web | Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui; Aceternity UI selektif |
| API | Hono di runtime Node.js tersendiri, REST, Zod validation |
| Background jobs | Node.js worker, Redis + BullMQ |
| Persistence | MySQL 8.4 / InnoDB / utf8mb4, Drizzle ORM + mysql2 dan versioned migrations |
| Authentication | Better Auth dengan schema sesuai versi library terpasang |
| Authorization | Custom server-side RBAC (user, role, permission) |
| Test | ESLint, TypeScript, Vitest, Playwright; negative authorization tests |
| Runtime | Node.js 26.x setelah verifikasi dukungan dependensi dan pin exact tested version |
| Production | Build artifact → upload → Nginx + PM2/systemd + native MySQL/Redis; tanpa Docker |

Tidak wajib menambahkan Turborepo, Docker, Kubernetes, atau framework lain pada bootstrap. Gunakan npm workspaces terlebih dahulu; tambahkan orchestrator hanya bila bottleneck terukur.

## 3. Struktur target (belum ada)

```text
app-starter-kit/
├── apps/
│   ├── web/                # Next.js App Router; hasil migrasi app root
│   ├── api/                # Hono HTTP runtime
│   └── worker/             # BullMQ consumers
├── packages/
│   ├── db/                 # Drizzle schemas, migration, DB client
│   ├── auth/               # Better Auth server config/helpers
│   ├── core/               # Business services
│   ├── contracts/          # Shared Zod schemas and safe types
│   ├── ui/                 # Reusable components and theme tokens
│   ├── queue/              # Job names and payload validation
│   └── config/             # Shared config without secrets
├── infra/                  # Nginx / service template, saat dibutuhkan
├── docs/                   # 4 blueprint docs
├── AGENTS.md
├── package.json
└── package-lock.json
```

Worker tidak perlu HTTP listener kecuali health strategy memerlukannya. Installer/migration CLI **opsional**, dapat ditambahkan pada milestone release bila diperlukan dan harus diuji dari artifact.

## 4. Data flow dan batas dependensi

```text
Browser ─ HTTPS ─> Nginx
                     ├── /, /admin/*, halaman publik -> Next.js (127.0.0.1:3000)
                     └── /api/auth/*, /api/v1/*    -> Hono (127.0.0.1:4000)
                                                         ├── MySQL
                                                         └── Redis queue
                        Worker <───────────────────────── Redis queue
                          └── MySQL / private storage
```

Web hanya memuat UI dan berkomunikasi ke API; **jangan** akses MySQL atau membaca rahasia langsung dari `apps/web`. Core/domain rules terpusat di API + shared core, tanpa menggandakan business endpoints di Next.js Route Handlers.

| From | Import yang diizinkan |
|---|---|
| `apps/web` | `packages/ui`, `contracts`, konfigurasi client-safe |
| `apps/api` | `auth`, `core`, `db`, `contracts`, `queue`, konfigurasi server |
| `apps/worker` | `core`, `db`, `queue`, konfigurasi server |
| `packages/contracts` | utilitas pure/schema saja; **tidak** boleh import app/database |

Gunakan Nginx single-origin dengan session cookie `HttpOnly`, `Secure` saat HTTPS, `SameSite` yang cocok, CSRF defense pada mutasi terautentikasi, rate limit, request validation, dan pemeriksaan permission **di setiap endpoint terlindungi**. Port API, MySQL, Redis hanya bind private/loopback. Semua timestamps aplikasi konsisten UTC.

## 5. Fitur dasar reusable

1. Authentication: login/logout/session, reset password, first-login password change; disable public sign-up secara default.
2. Authorization: `users`, `roles`, `permissions`, `user_roles`, `role_permissions`, server middleware dan permission matrix.
3. Admin shell: **Dashboard, Manage Content, Manage User, Setting**. Sidebar mengikuti permission, bukan pengganti otorisasi API.
4. CMS dasar: halaman, draft/publish, media dan navigasi; content public hanya yang published.
5. Application settings: nama/logo, tema customizable. Preset Salt & Pepper: `#FFFFFF`, `#D4D4D4`, `#B3B3B3`, `#2B2B2B`.
6. Audit event penting, error handling, example background job.
7. Backup/restore menjadi workstream terpisah berisiko tinggi; tidak otomatis mengeksekusi restore production.

Bootstrap admin `super_admin` menggunakan secret instalasi lokal, wajib ganti password pertama kali, tanpa password dalam repository/log. Kode dan database template harus bebas dari sesi, media, backup, dan data pengguna proyek asal.

Lihat [ROADMAP.md](ROADMAP.md), [AGENT-WORKFLOW.md](AGENT-WORKFLOW.md), dan [DEPLOYMENT.md](DEPLOYMENT.md). Semua modul selain source Next.js root masih **target**, bukan fitur aktif.
