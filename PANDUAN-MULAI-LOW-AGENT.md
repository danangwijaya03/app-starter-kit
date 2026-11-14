# Panduan Pengguna — app-starter-kit dengan coding agent yang dipilih

**Ditujukan untuk: USER / DEVELOPER.** [AGENTS.md](AGENTS.md) adalah instruksi implementer.

## Strategi

Satu coding model: **coding agent yang dipilih**, mengerjakan satu task pada satu waktu. Coding agent mempelajari referensi yang ditentukan untuk task, menyesuaikan dengan Next.js/Hono/MySQL dan npm, menguji kode, menyediakan preview dan checkpoint. Tidak ada kewajiban mempunyai model reasoning tinggi; **review keamanan independen tetap wajib sebelum task high-risk disahkan**.

Penggunaan ulang starter kit: **clone repository + setup manual**, bukan installer atau generator. Baca [Manual Clone Setup](docs/MANUAL-CLONE-SETUP.md) dan [Reference Map](docs/references/REFERENCE-MAP.md).

## Menjalankan baseline Next.js

```bash
cd app-starter-kit
git status --short
git pull --ff-only origin main   # hanya bila working tree bersih
npm ci
npm run dev
```

Buka `http://localhost:3000/`. Halaman saat ini **static preview**. Perintah root saat ini: `dev`, `build`, `lint`; npm workspaces, API, DB, worker, dan script migrasi merupakan target fase berikutnya. Lerd/MySQL/Redis yang sudah tersedia tidak boleh diinstal ulang.

## Memulai coding agent

1. Buka folder repo yang sama di Codex/editor, pilih **coding agent yang dipilih**.
2. Berikan isi [START-AGENT-PROMPT.md](docs/agent/START-AGENT-PROMPT.md).
3. Agent menjalankan `python3 tools/bootstrap_agent.py` sendiri, memilih task ready, membaca **satu** card + satu domain referensi, lalu mengimplementasikan/mengetes/preview/checkpoint.
4. Pantau dengan `.venv-agent/bin/python tools/agent_tasks.py summary`, `next`, [CHECKPOINT](docs/agent/CHECKPOINT.md), dan [REVIEW-QUEUE](docs/agent/REVIEW-QUEUE.md).
5. Jika sesi habis gunakan [RESUME-SESSION-PROMPT.md](docs/agent/RESUME-SESSION-PROMPT.md). Jangan reset Git atau menjalankan ulang migrasi/seed sembarangan.

Status task CLI hanya `pending`, `in_progress`, `blocked`, `completed`, `verified`. Status feedback pengguna (`pending_review`, `approved`, `revision_requested`) dicatat di review queue terpisah. Jangan samakan lint/build dengan tes keamanan. Task high-risk dapat diimplementasikan coding agent yang dipilih tetapi menunggu independent review jika diperlukan; task aman lain tetap berjalan.

**Branch:** `main` sesuai keputusan. Deployment ke server selalu manual dan memerlukan izin operator; lihat [README-SERVER](README-SERVER.md).
