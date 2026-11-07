# app-starter-kit

**Ditujukan untuk: USER / DEVELOPER.** Repository sudah berisi Next.js 16.4.3, React 19.3.0, TypeScript, Tailwind v4, npm/npx. Aplikasi yang dibuat dengan `npx create-next-app@latest` masih berada pada root repository dan **akan dipindahkan oleh task P01**, bukan dibuat ulang.


## Blueprint monorepo (pembaruan dokumentasi 2026-11-07)

Dokumentasi arsitektur terbaru tersedia pada [ARCHITECTURE](docs/ARCHITECTURE.md), [ROADMAP](docs/ROADMAP.md), [AGENT-WORKFLOW](docs/AGENT-WORKFLOW.md), [DEPLOYMENT](docs/DEPLOYMENT.md), dan [PROGRESS](docs/PROGRESS.md). Ringkasan ini **tidak** menggantikan 157 task P00–P16 di `docs/agent/TASKS.yaml`; status dan fase existing tetap otoritatif. Pengembangan dilakukan pada branch `dev`, sedangkan `main` tetap baseline. Perubahan dokumentasi tidak berarti API/worker/monorepo sudah diimplementasikan.

## Menjalankan Next.js saat ini

```bash
npm ci
npm run dev
```

Buka `http://localhost:3000`. Pemeriksaan awal: `npm run lint` dan `npm run build`. Setelah migrasi P01, gunakan script npm workspace yang sudah benar-benar dibuat oleh agent.

**Development:** Lerd + Node.js 26 + MySQL existing (Redis Lerd saat diperlukan). **Production:** upload artifact ke server aaPanel dengan Node/PM2/Nginx, tanpa Docker.

## Memulai development lewat Codex Low

Ikuti **[Panduan Pengguna](PANDUAN-MULAI-LOW-AGENT.md)** untuk setup, memulai, memantau, dan melanjutkan sesi. Prompt pertama: [START](docs/agent/START-AGENT-PROMPT.md); prompt sesi baru: [RESUME](docs/agent/RESUME-SESSION-PROMPT.md).

Coding agent otomatis menyiapkan `.venv-agent` tanpa aktivasi shell melalui `python3 tools/bootstrap_agent.py` sebelum P00, kemudian membaca **[AGENTS.md](AGENTS.md)**, runbook dan task card; panduan pengguna **bukan** instruksi agent.

**Monitoring agent:** `.venv-agent/bin/python tools/agent_tasks.py summary` menampilkan progres seluruh fase. `.venv-agent/bin/python tools/check_repo_contracts.py` memeriksa konsistensi README, script npm dan struktur aktual tanpa mengubah aplikasi. Agent harus mengikuti kebijakan tes/review pada [TEST-AND-REVIEW-POLICY.md](docs/agent/TEST-AND-REVIEW-POLICY.md).

## Dokumentasi lengkap

[Lihat peta dokumen berdasarkan pembaca](docs/DOCUMENTATION-MAP.md). Di sana tersedia PRD, TRD, AFD, DBD, BSD, IPD, 17 fase, task registry dan kontrak Lerd.

**Belum tersedia:** aplikasi full-stack monorepo, API, CMS, RBAC, worker dan installer. [README-SERVER.md](README-SERVER.md) masih spesifikasi sampai release P16 dibangun dan diuji.
