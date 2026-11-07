# Project Progress — Snapshot Dokumen

**Snapshot:** 2026-11-07. **Branch:** `dev` (dokumentasi). Dokumen ini ringkasan manusia, **bukan** registry task. Status task yang sebenarnya hanya [`agent/TASKS.yaml`](agent/TASKS.yaml) melalui `tools/agent_tasks.py`.

## Baseline terobservasi saat revisi dokumentasi

- Repository telah memiliki root Next.js 16.4.3 / React 19.3.0 + npm lockfile; **belum** berada di layout `apps/web`.
- Dokumentasi existing sudah mencakup PRD/TRD/AFD/DBD/BSD/IPD, 17 fase P00–P16, dan 157 task awal.
- Target: npm monorepo dengan Next.js Web, Hono API, BullMQ Worker, MySQL/Drizzle/Better Auth, aplikasi single-tenant, non-Docker artifact deployment.
- Perubahan November ini **dokumentasi saja**; tidak membangun API, Worker, login, database migration, maupun release artifact.
- Status dan hasil tes implementasi **tidak diverifikasi oleh perubahan dokumentasi ini**; jangan menandai task sebagai completed.

## Dokumen orientasi baru

- [ARCHITECTURE](ARCHITECTURE.md): runtime, dependency boundaries, modul, data flow.
- [ROADMAP](ROADMAP.md): mapping blueprint terhadap P00–P16 **existing**.
- [AGENT-WORKFLOW](AGENT-WORKFLOW.md): implementation agent, testing agent, checkpoint dan guardrail.
- [DEPLOYMENT](DEPLOYMENT.md): artifact build/upload, Nginx/PM2, safe rollback.

## Langkah selanjutnya

1. Pada `dev`, jalankan `python3 tools/bootstrap_agent.py`.
2. Ambil task ready dari `.venv-agent/bin/python tools/agent_tasks.py next`, jangan memilih fase berdasarkan deskripsi ringkas saja.
3. Lanjut task P00/P01 sesuai dependensi, lakukan migrasi root Next.js **hanya** pada task P01 yang tepat.
4. Perbarui progres **melalui tooling dan evidence**; dokumen ini boleh diperbarui untuk ringkasan milestone tanpa menduplikasi 157 status.

Jika ada pertentangan antara diagram ringkas dan spesifikasi rinci yang sudah ada, catat terlebih dahulu di review/decision sebelum melakukan perubahan source.
