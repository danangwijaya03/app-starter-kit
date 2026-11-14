# Start Coding Agent — provider-agnostic

**Ditujukan untuk: CODING AGENT (prompt disalin oleh USER).**

```text
Kerjakan app-starter-kit dari repository yang SUDAH ADA pada branch main, menggunakan satu coding agent aktif per task; bebas provider/model (Codex, Claude Code, Antigravity, DeepSeek, dll), boleh ganti antar task/sesi setelah checkpoint. Tujuan: Clone-Based Reusable Starter Kit + Reference-Driven Development + Single Coding Model.

Baca AGENTS.md, docs/agent/SINGLE-MODEL-WORKFLOW.md dan dokumen task aktif saja. Jangan membuat installer, generator, Docker requirement, archive release manager, atau re-run create-next-app. Pertahankan root Next.js sampai task P01 memigrasikannya ke apps/web; gunakan npm/npx dan Lerd MySQL/Redis yang sudah tersedia.

git status --short
python3 tools/bootstrap_agent.py
.venv-agent/bin/python tools/agent_tasks.py doctor
.venv-agent/bin/python tools/agent_tasks.py next
.venv-agent/bin/python tools/agent_tasks.py summary

Jika bootstrap gagal, berhenti dengan laporan blocker; jangan mengganti Python sistem atau status task. Jika task in_progress, audit Git/source/evidence dahulu. Pilih hanya satu task ready dan baca card + spec_refs + satu domain referensi docs/references/ (lihat REFERENCE-MAP.md dan ADOPTION-PROTOCOL.md). Tidak perlu membaca seluruh task atau meneliti semua starter kit.

Flow: RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT. Ikuti kontrak MySQL/Drizzle/Better Auth/Hono/RBAC, catat sumber/version/license bila adaptasi kode, tidak copy source besar. Pecah tugas yang terlalu luas ketika masih pending.

Jalankan scoped tests nyata dan negative tests relevan setelah edit terakhir dengan agent_tasks.py run. Task risiko tinggi memerlukan independent qualified reviewer untuk complete; model High Reasoning tidak wajib. Jangan self-approve, jangan minta izin deploy production otomatis. Jika blocked karena review, lanjut task independen yang aman.

Untuk UI, jalankan preview bila memungkinkan: URL nyata, fixture/integrated, langkah review, CHECKPOINT dan REVIEW-QUEUE. Catat 'not verified' jika browser/dev server tidak dapat diuji. Commit bounded hasil teruji di main jika aman. Lanjut otomatis ke ready task berikutnya selama sesi berjalan, tanpa menunggu user untuk review visual biasa.
```

Panduan untuk pengguna: [PANDUAN-MULAI-LOW-AGENT.md](../../PANDUAN-MULAI-LOW-AGENT.md).
