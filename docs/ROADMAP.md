# Roadmap Implementasi — Monorepo P00–P16

**Updated:** 2026-11-07. **Status:** rencana pelaksanaan, **bukan** bukti fitur sudah ada. Task registry [`agent/TASKS.yaml`](agent/TASKS.yaml), task cards, dan [`agent/PHASES.md`](agent/PHASES.md) adalah sumber otoritatif untuk nomor, dependensi, serta status.

## Kenapa fase tidak dinomori ulang?

Blueprint ringkas baru mengelompokkan pekerjaan menjadi Foundation, Identity, Features, Quality, Release. Repository sudah mempunyai 157 atomic task dalam 17 fase dengan **pemetaan fase yang lebih detail**. Untuk menghindari konflik task ID dan mengulang pekerjaan, gunakan fase **existing** di bawah. Jangan menganggap label P04 dari rancangan ringkas sebelumnya identik dengan P04 registry.

| Milestone | Fase existing | Fokus | Gate minimum |
|---|---|---|---|
| A Foundation | P00 | Spesifikasi, validasi dokumen, kesiapan agent | Link/registry/contract valid |
| A Foundation | P01 | Migrasi root Next.js ke npm monorepo, Hono/worker scaffolding | `npm ci`, workspace build smoke |
| A Foundation | P02 | Lerd Node 26, dev/test MySQL dan Redis | Koneksi dan isolasi lingkungan terbukti |
| A Foundation | P03 | Drizzle, Better Auth schema, migration, transactions | Migration di DB disposable teruji |
| B Core | P04 | Better Auth login, logout, reset, session | Auth positives/negatives lulus |
| B Core | P05 | RBAC, permission registry, first admin | Server deny + bootstrap tests lulus |
| B Core | P06 | Design system Salt & Pepper, admin shell | Responsif, route/menu visibility |
| B Core | P07 | CRUD user, role, permission editor | Endpoint dan UI end-to-end |
| B Core | P08 | Dashboard & widget registry | Grant checks + render |
| C Product | P09 | Storage/media library | Upload safety, access, persistence |
| C Product | P10 | CMS editor dan revisi | Draft/publish invariant |
| C Product | P11 | Public CMS & navigation | Hanya published content ditampilkan |
| C Product | P12 | Settings, branding, appearance, audit viewer | Persistensi dan authorization |
| D Operations | P13 | Redis/BullMQ worker | Retry, idempotency, shutdown |
| D Operations | P14 | Backup terverifikasi | Isolated backup, checksum, encryption |
| D Operations | P15 | Restore & recovery | Staging, fail-safe, manual approval |
| D Release | P16 | Standalone artifacts, CLI, Nginx/PM2, E2E | Fresh install, upgrade, rollback smoke |

Lihat [`IPD.md`](IPD.md) dan [`agent/PHASES.md`](agent/PHASES.md) untuk dependency graph dan acceptance criteria detail. Tidak boleh melompati dependensi yang tercatat.

## Workflow per atomic task

**RECOVER → IMPLEMENT → TEST → VERIFY → CHECKPOINT → NEXT**

1. **RECOVER:** periksa branch dan `git status --short`, task yang in_progress, commit terakhir, evidence. Jalankan `python3 tools/bootstrap_agent.py` sesuai [AGENTS](../AGENTS.md), kemudian CLI `doctor`, `next`, `show`.
2. **IMPLEMENT:** kerjakan satu task yang ready pada scope card saja. Untuk fitur end-to-end ikuti urutan migration → core service → API → permission → UI → relevant test; pecah resmi jika melebihi satu unit.
3. **TEST:** implementer menjalankan scoped tests setelah edit terakhir; test tidak boleh hanya dinyatakan lulus. Gunakan evidence runner `agent_tasks.py run`. Gunakan database disposable untuk destructive scenarios.
4. **VERIFY:** cek acceptance criteria, lint/typecheck/build yang relevan, negative authorization paths. High-risk task memerlukan independent review sesuai policy.
5. **CHECKPOINT:** commit kecil dan simpan bukti dengan tooling. Jangan mengubah field status YAML manual atau menyelesaikan task tanpa bukti.
6. **NEXT:** lanjut task ready berikutnya secara mandiri selama aman dan tidak membutuhkan persetujuan berisiko.

## Pembagian agent

- **Implementation agent (mis. GPT-6.1 Sol Medium jika tersedia):** kode, migration, focused tests dan checkpoint per task.
- **Testing agent (mis. GPT-5.6 Terra jika tersedia):** review independen, integration/E2E, keamanan, regresi per milestone. Temuan dibuka sebagai task perbaikan yang scoped, bukan perubahan tak terbatas.
- **High-risk reviewer:** terpisah dari implementer; pemeriksaan auth/RBAC, migration, backup/restore, deploy/rollback tidak boleh self-approve.
- Testing komprehensif dapat berjalan setelah satu milestone, **tetapi unit tests dan security smoke tests tidak boleh ditunda sampai seluruh 17 fase selesai**.

Lihat [`AGENT-WORKFLOW.md`](AGENT-WORKFLOW.md) dan [kebijakan tes](agent/TEST-AND-REVIEW-POLICY.md).

## Gate keseluruhan

Fresh `npm ci` dan build tiga runtime, migration ke MySQL kosong, authenticated flows, RBAC deny checks, CRUD end-to-end, worker retry, tests lint/type/E2E, source-free artifact isolated smoke, template clone tanpa secret/data, serta dokumentasi deployment yang benar-benar diuji. Pada fase P16, installer/backup/restore harus sesuai scope existing IPD, bukan dipotong hanya karena blueprint ringkas.

## Mulai dari repository yang sudah ada

**Jangan** mengulang `npx create-next-app`: root app sudah tersedia. P01 migrasi via Git move, memperbarui npm workspace dan lockfile root, lalu membuat skeleton Hono/worker/installer. Berkas `apps/` dan `packages/` pada [architecture](ARCHITECTURE.md) adalah target dan hanya dibuat pada task yang tepat.

Untuk status terbaru: `.venv-agent/bin/python tools/agent_tasks.py summary`. Catatan manusia bisa dirujuk di [PROGRESS](PROGRESS.md), tetapi **`TASKS.yaml` adalah sumber status tunggal**.
