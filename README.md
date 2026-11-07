# app-starter-kit

**Clean Next.js baseline + new monorepo blueprint** (branch `dev`; reset 2026-11-07).

Repository ini berisi source awal Next.js 16.4.3 (App Router), React 19.3.0, TypeScript, Tailwind v4 dan npm lockfile di root. **Hono API, worker, MySQL/Drizzle, RBAC, CMS dan release artifact belum diimplementasikan.**

## Jalankan aplikasi saat ini

Prasyarat: Node.js versi yang mendukung dependency terpasang, npm dan Git. Baseline pengembangan yang ditargetkan: Node.js 26 dengan kompatibilitas yang diuji.

```bash
npm ci
npm run dev
```

Buka http://localhost:3000. Pemeriksaan dasar:

```bash
npm run lint
npm run build
```

Jangan menjalankan `npx create-next-app` di repo ini. Source bawaan Next.js sudah ada. Saat implementasi monorepo (fase P01), **pindahkan** app dari root ke `apps/web` dan bangun npm workspaces dengan satu lockfile.

## Blueprint dan tahap implementasi

- [Architecture](docs/ARCHITECTURE.md) — Next.js Web + Hono API + BullMQ worker + MySQL + Redis.
- [Roadmap](docs/ROADMAP.md) — P00–P16 baru, tanpa task registry lama.
- [AI Agent Workflow](docs/AGENT-WORKFLOW.md) — implementer, independent QA, scoped testing, checkpoint.
- [Deployment](docs/DEPLOYMENT.md) — source-free artifact, Nginx, PM2/systemd, tanpa Docker.

`AGENTS.md` berisi aturan singkat untuk coding agent. Pengembangan dilakukan di `dev` atau feature branch dari `dev`; `main` tidak ikut direset.

**Catatan:** perubahan reset hanya source tree/documentation. Build dan test belum dijalankan melalui GitHub pada reset ini. Jangan menganggap fase roadmap telah selesai.
