# app-starter-kit

**Ditujukan untuk: USER / DEVELOPER.** Repository sudah berisi Next.js 16.4.3, React 19.3.0, TypeScript, Tailwind v4, npm/npx. Aplikasi yang dibuat dengan `npx create-next-app@latest` masih berada pada root repository dan **akan dipindahkan oleh task P01**, bukan dibuat ulang.

## Menjalankan Next.js saat ini

```bash
npm ci
npm run dev
```

Buka `http://localhost:3000`. Pemeriksaan awal: `npm run lint` dan `npm run build`. Setelah migrasi P01, gunakan script npm workspace yang sudah benar-benar dibuat oleh agent.

**Development:** Lerd + Node.js 26 + MySQL existing (Redis Lerd saat diperlukan). **Production:** upload artifact ke server aaPanel dengan Node/PM2/Nginx, tanpa Docker.

## Preview development yang langsung bisa direview

Halaman `/` sekarang berupa **static UI development preview** dengan preset Salt & Pepper dan empat menu rancangan. Bukan dashboard live: API/MySQL/auth belum aktif. Jalankan `npm ci` lalu `npm run dev`; akses `http://localhost:3000/` (jika server benar-benar menyala).

Development berlangsung incremental di **branch `main`**: task kecil → implementasi → tes → preview (fixture atau real integration diberi label) → checkpoint → task berikutnya. Review UI/UX pengguna dicatat terpisah dan tidak memblokir pekerjaan aman lainnya.

- [Development Roadmap](docs/DEVELOPMENT-ROADMAP.md) — hasil yang dapat dilihat di setiap fase.
- [Preview & Feedback](docs/agent/PREVIEW-AND-FEEDBACK.md) — kontrak preview, langkah review, dan aturan feedback.
- [Agent Routing](docs/agent/AGENT-ROUTING.md) — Low untuk rutin, rekomendasi High untuk keputusan/fitur penting.
- [Installer Boundaries](docs/agent/INSTALLER-BOUNDARIES.md) — initializer, setup CLI dan deployment manager.

## Memulai development lewat Codex Low

Ikuti **[Panduan Pengguna](PANDUAN-MULAI-LOW-AGENT.md)** untuk setup, memulai, memantau, dan melanjutkan sesi. Prompt pertama: [START](docs/agent/START-AGENT-PROMPT.md); prompt sesi baru: [RESUME](docs/agent/RESUME-SESSION-PROMPT.md).

Coding agent otomatis menyiapkan `.venv-agent` tanpa aktivasi shell melalui `python3 tools/bootstrap_agent.py` sebelum P00, kemudian membaca **[AGENTS.md](AGENTS.md)**, runbook dan task card; panduan pengguna **bukan** instruksi agent.

**Monitoring agent:** `.venv-agent/bin/python tools/agent_tasks.py summary` menampilkan progres seluruh fase. `.venv-agent/bin/python tools/check_repo_contracts.py` memeriksa konsistensi README, script npm dan struktur aktual tanpa mengubah aplikasi. Agent harus mengikuti kebijakan tes/review pada [TEST-AND-REVIEW-POLICY.md](docs/agent/TEST-AND-REVIEW-POLICY.md).

## Dokumentasi lengkap

[Lihat peta dokumen berdasarkan pembaca](docs/DOCUMENTATION-MAP.md). Di sana tersedia PRD, TRD, AFD, DBD, BSD, IPD, 17 fase, task registry dan kontrak Lerd.

**Belum tersedia:** aplikasi full-stack monorepo, API, CMS, RBAC, worker dan installer. Preview di `/` hanyalah UI statis. [README-SERVER.md](README-SERVER.md) masih spesifikasi sampai release P16 dibangun dan diuji.
