# Alur Kerja AI Coding Agent — Implementasi dan QA Terpisah

**Updated:** 2026-11-07. Dokumen ini memberi panduan praktis di atas [AGENTS.md](../AGENTS.md), [task registry](agent/TASKS.yaml), dan [test/review policy](agent/TEST-AND-REVIEW-POLICY.md). Jika tidak selaras, hentikan task dan catat mismatch, jangan menebak.

## Branch dan sumber kerja

- `main` adalah baseline; seluruh pekerjaan pengembangan ditujukan ke `dev`, kecuali instruksi operator secara eksplisit menyatakan lain.
- Sebelum mengedit: pastikan `git branch --show-current`, `git status --short`, commit HEAD dan task ID. Jangan mengubah working tree pengguna yang tidak terkait.
- **Root Next.js sudah ada.** Jangan menjalankan `create-next-app` lagi. Migrasi root ke `apps/web` hanya saat task P01 terkait.
- Task status, dependencies, dan evidence hanya dikelola melalui `tools/agent_tasks.py`; jangan membuat file status paralel yang menyaingi `TASKS.yaml`.

## Dua peran agent

| Peran | Contoh model (jika tersedia) | Akuntabilitas |
|---|---|---|
| Implementation | GPT-6.1 Sol Medium | Satu atomic task, kode + tes fokus, commit, checkpoint |
| QA/Testing independen | GPT-5.6 Terra | Review code, negative/integration/E2E, laporan defect dan regresi |

Model adalah **pilihan operator**, bukan dependency teknis atau jaminan kemampuan. Jangan menyamakan hasil test agent dengan audit keamanan manusia.

### Pola kerja

1. **RECOVER:** jalankan `python3 tools/bootstrap_agent.py` (tidak perlu activate shell; kompatibel Fish), lalu `.venv-agent/bin/python tools/agent_tasks.py doctor` dan `next`; baca task in_progress atau ready serta spec_refs.
2. **IMPLEMENT:** edit satu jalur end-to-end dan dependensi langsung. Perhatikan DB transactions, auth, RBAC, CSRF, API contracts, error states, dan validasi.
3. **TEST:** jalankan tes nyata yang relevan **setelah edit terakhir** dan rekam evidence via `agent_tasks.py run <ID> --kind ... -- COMMAND`. Negative tests memeriksa perilaku penolakan aman, bukan sekadar command gagal.
4. **VERIFY:** periksa acceptance dan mismatch docs/code. Untuk high-risk minta reviewer independen sesuai policy, jangan self-approve.
5. **CHECKPOINT:** commit satu unit selesai, catat files/evidence/hash/task next. Bila sesi terputus gunakan `progress`/blocker agar sesi selanjutnya melanjutkan dari bukti terakhir.
6. **NEXT:** lanjut task ready berikutnya tanpa konfirmasi rutin, kecuali operasi berisiko/memerlukan akses pengguna.

### Independent QA cadence

- Implementer **wajib** scoped tests setiap task; tidak boleh menunda semua tes sampai implementasi selesai.
- QA independen dapat melakukan batch review **setiap milestone** A/B/C/D atau fase high-risk; laporkan defect bersama langkah reproduksi dan expected/actual.
- Temuan QA dibuat menjadi task perbaikan scoped dan re-test terkait; jangan membatalkan seluruh fase yang sudah terverifikasi kecuali ada bukti regresi.
- Migration, auth/session, RBAC, backup/restore, deploy dan rollback harus mendapat independent review yang dicatat sesuai [policy](agent/TEST-AND-REVIEW-POLICY.md).

## Contoh checkpoint ringkas

```text
Task: P05-xx
Branch: dev
Status: COMPLETED only if CLI recorded valid evidence
Changed files: ...
Tests executed after last edit: command + result
Review: reviewer + artifact (when required)
Commit: <sha>
Mismatch/blockers: ...
Next ready task: ...
```

## Batas keamanan

Tidak boleh menjalankan destructive test pada database produksi/development yang berisi data nyata. Jangan mengakses/mengubah secret live, menghapus backup, melakukan production deployment, atau mengaktifkan restore tanpa otorisasi operator yang eksplisit. Gunakan DB test disposable dan mock external integrations. Jangan menuliskan password bootstrap ke issue/log/checkpoint.

## Pemeriksaan akhir per milestone

Status registry benar, evidence sesuai task, `npm ci` / build (jika task menyentuh workspace), lint/typecheck, integration/negative paths, dokumentasi dan deploy contract konsisten. Sebelum P16 selesai, semua path/command yang masih target **harus** ditandai belum executable.

Rujukan: [ROADMAP](ROADMAP.md), [ARCHITECTURE](ARCHITECTURE.md), [DEPLOYMENT](DEPLOYMENT.md), [LOW-REASONING-RUNBOOK](agent/LOW-REASONING-RUNBOOK.md).
