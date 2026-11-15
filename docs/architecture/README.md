# Architecture v2 — Canonical Revision Pack

**Ditetapkan secara konseptual:** 2026-11-14. **Integrasi dokumentasi v2:** diterapkan ke PRD/TRD/BSD/AFD/IPD/task graph; **fitur source belum diimplementasikan**.
Semua pernyataan “harus” adalah target implementasi. [REBASE-EXISTING-DOCS.md](REBASE-EXISTING-DOCS.md) adalah catatan migrasi dokumen; keputusan v2 mengikat bila ada teks lama yang masih ambigu. Core release adalah [P16-11](../agent/tasks/P16-11.md), module matrix [P16-12](../agent/tasks/P16-12.md).

## Urutan baca

1. [ADR Register](ADR/README.md) — 16 keputusan yang disetujui.
2. [System and Module Contracts](MODULE-BOUNDARIES.md) — layout, modul, dependency enforcement.
3. [Security and RBAC](AUTH-RBAC-CONTRACT.md) — identity, delegation, session, audit.
4. [Database](DATABASE-CONTRACT.md) — 21 base tables, schema delta, migration algorithm.
5. [API and Web](API-WEB-CONTRACT.md) — Hono, Next, cache, errors, routes.
6. [Media and CMS](MEDIA-CMS-CONTRACT.md) — file lifecycle, blocks, revision & publish.
7. [Jobs](JOBS-CONTRACT.md) — durable dispatch, processor idempotence.
8. [Settings and Theme](SETTINGS-THEME-CONTRACT.md).
9. [Recovery and Deployment](OPERATIONS-RUNBOOK.md).
10. [Testing and Release Gates](TESTING-RELEASE.md).
11. [Task Rebase Plan](TASK-REBASE-PLAN.md), [Traceability](TRACEABILITY.md), [Original Docs Rebase](REBASE-EXISTING-DOCS.md).

## Truth hierarchy after integration

Accepted ADR > architecture contracts > revised PRD/TRD/BSD/AFD/IPD > task acceptance criteria > code examples.
Jika ada kontradiksi, *block task* dan ajukan ADR/PR, jangan menebak. `TASKS.yaml` tetap sumber status task; tidak pernah mengesahkan keputusan arsitektur sendiri.

## Non-goals

Installer, SaaS multi-tenancy, multi-node distributed architecture, zero-downtime guarantees, custom security framework, arbitrary visual HTML builder. Semua backup/restore contoh harus diuji di lingkungan terisolasi lebih dulu.

## Integrasi dua ZIP oleh pengguna

Paket **architecture-v2** adalah sumber ADR/kontrak dan addenda lama; paket **references-v2** adalah sumber pengganti 12 playbook serta 3 dokumen baru dalam [docs/references/INDEX-V2.md](../references/INDEX-V2.md). Keduanya menyatakan desain, tidak mengklaim fitur sudah live. Task registry direbase dari 156 menjadi 162 ID dengan sejarah status/evidence tidak dinaikkan. Integrasi dokumentasi tidak menjalankan migrasi MySQL, worker, server, atau backup.
