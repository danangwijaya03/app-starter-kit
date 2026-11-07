# Roadmap — Implementasi Baru P00–P16

**Status: semua fase P00–P16 belum dikerjakan setelah reset dokumentasi pada 2026-11-07.**

Ini adalah **roadmap baru, berdiri sendiri**. Task registry 157 item, file `docs/agent/TASKS.yaml`, checkpoint dan scripts Python lama **sengaja dihapus**. Tidak ada task ID lama yang perlu dipulihkan. Mulai dari source Next.js root yang telah ada. Agent membuat task kecil berdasarkan fase berikut tanpa menganggap tahap selesai sebelum verifikasi aktual.

| Fase | Deliverable | Verification gate |
|---|---|---|
| P00 | Audit baseline, kontrak teknis, kriteria berhasil | Git clean, Next scaffold teridentifikasi |
| P01 | **Migrasi** root Next.js ke `apps/web`; npm workspaces | `npm ci`, web lint/build lulus, history aman |
| P02 | Shared config, TypeScript, contracts, batas package | Typecheck/lint + import boundary |
| P03 | Hono API skeleton + Next → API proxy | Web/API health dan same-origin smoke |
| P04 | MySQL, Drizzle schema + migrations | Migrate dari DB test kosong, repeatability |
| P05 | Better Auth + bootstrap admin + session | Login/logout dan negative tests |
| P06 | Custom RBAC dan server authorization | 401/403, privilege escalation ditolak |
| P07 | Zod/REST API contracts & error envelopes | Validation/negative API tests |
| P08 | Responsive admin shell + Salt & Pepper | UI + authorized route/navigation smoke |
| P09 | User/role CRUD + permission editor | Vertical slice end-to-end |
| P10 | Branding, settings, theme persistence | Isolasi config/permissions |
| P11 | CMS draft/publish, media/navigation minimal | Published-only public content |
| P12 | Redis queue, BullMQ worker, sample job | Retry, idempotence, shutdown |
| P13 | Audit, observability, health/ops | Logs tanpa secret, error handling |
| P14 | Integration, E2E, security/regression tests | Seluruh test kritis lulus |
| P15 | Portable build artifacts + Nginx/process templates | Artifact-only smoke (tanpa source tree) |
| P16 | Template onboarding + fresh-install validation | Proyek turunan terisolasi dapat dibuat |

Dependency dasar: `P00→P01→P02→P03→P04→P05→P06→P07→P08→P09`; P10/P11/P12 dapat dimulai setelah dependensi masing-masing lulus; P13–P16 harus diverifikasi di bagian akhir. Tidak boleh menunda tes unit/fungsional sampai P14: setiap fase tetap mempunyai gate.

## Aturan kerja

- **Jangan** menjalankan `npx create-next-app`; source Next sudah tersedia di root. P01 memindahkan, bukan mengulang bootstrap.
- Pertahankan `main`; semua perubahan pada branch `dev` atau feature branch dari `dev`.
- Selesaikan satu **atomic task** pada satu waktu. Setiap task memiliki scope, berkas yang diubah, acceptance criteria, perintah tes aktual, dan commit.
- Gunakan pendekatan **RECOVER → IMPLEMENT → TEST → VERIFY → CHECKPOINT → NEXT**.
- Jangan menjalankan tindakan destructive pada production/DB lokal yang berisi data nyata.
- Test berisiko (auth/RBAC, migrations, backup/restore, release) memerlukan review independen.
- Dokumentasikan mismatch jika kode tidak sesuai blueprint, lalu ubah dengan keputusan yang eksplisit; jangan menyamakan design target dengan implementasi selesai.
- Jangan menambah tool checkpoint besar dan puluhan dokumen otomatis sejak awal. Status/progress minimal bisa didapat dari commit dan satu checkpoint ringkas per task.

## Definition of Done

Fresh `npm ci`, three independent builds (web/API/worker), empty-DB migration, login/session/permission negative tests, user-role CMS-settings E2E, worker retry/idempotence, audit, artifact isolation/deploy smoke, serta template baru tidak membawa data/secret proyek awal. Jalankan semua gate di lingkungan disposable atau sesuai izin operator.

Referensi: [ARCHITECTURE.md](ARCHITECTURE.md), [AGENT-WORKFLOW.md](AGENT-WORKFLOW.md), [DEPLOYMENT.md](DEPLOYMENT.md).
