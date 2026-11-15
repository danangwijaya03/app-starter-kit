# app-starter-kit

**Architecture v2 (accepted design):** [Modular Core Specification](SPEC-001-app-starter-kit-modular-core.md) · [16 ADR Decisions](docs/architecture/ADR/README.md) · [Architecture Contracts](docs/architecture/README.md) · [Reference v2](docs/references/INDEX-V2.md). **Current source remains Next.js static preview; none of the new v2 features are claimed implemented.**

**Core-first:** Next.js + Hono + MySQL with Better Auth, application RBAC, dashboard, typed settings/immutable semantic theme, transactional audit, Core health/monitoring and independent encrypted offsite recovery. **Optional:** Media; CMS (requires Media); Jobs/Operations (Redis and BullMQ worker conditional). Core-only deployment needs no Redis/worker, CMS or Media. Production backup/recovery remains mandatory independent of Operations UI.


Reusable **single-tenant, clone-based** application foundation. **Approved approach:** build our architecture and selectively adapt **reviewed references** from established open-source projects. **No project generator/installer/release-archive manager.**

## Current source status

The repository **currently runs root Next.js 16.4.3, React 19.3, Tailwind v4, npm** with a **static development-preview page**. It is **not yet** a completed monorepo; Hono API, MySQL integration, auth/RBAC, CMS, worker and backup are planned task implementations. Treat task descriptions and target scripts as plans until code/tests prove otherwise.

```bash
npm ci
npm run lint
npm run build
npm run dev
```

Open `http://localhost:3000/` when the server is running. The visible dashboard is a **DEMO**, not live authentication or database data.

## Target architecture

```text
apps/web             Next.js 16 / public and admin UI
apps/api             Hono Node API / Better Auth / server authorization
apps/worker          Optional BullMQ with Redis (only for modules requiring jobs)
packages/database    MySQL 8.4 / Drizzle schema & migrations
packages/contracts   Typed Zod API contracts
packages/permissions Single-tenant app RBAC
packages/ui          Reusable Salt & Pepper components
infra/nginx, infra/pm2  Manual aaPanel/VPS deployment examples
```

npm workspaces + Turborepo, Node 26 baseline, **no Docker requirement**, one lockfile. When starting a new business application, **clone the template and configure DB/Redis/env manually**; no installer. Initial database migration, seed, permission sync and first-admin bootstrap will be standalone **manual npm scripts** after they are implemented.

## Where to start

- [Manual Clone Setup](docs/MANUAL-CLONE-SETUP.md) — new project from template (distinguishes current commands from planned scripts).
- [Development Roadmap](docs/DEVELOPMENT-ROADMAP.md) — phases P00–P16 and incremental review checkpoints.
- [Reference v2 Index](docs/references/INDEX-V2.md) and [Reference Map](docs/references/REFERENCE-MAP.md) — approved source candidates, feature playbooks, optional ideas.
- [Reference Adoption Protocol](docs/references/ADOPTION-PROTOCOL.md) — safe reuse, source license/version, MySQL conversion and tests.
- [Single-Model Workflow](docs/agent/SINGLE-MODEL-WORKFLOW.md) — coding agent yang dipilih for implementation, independent security review for high-risk.
- [Start Agent Prompt](docs/agent/START-AGENT-PROMPT.md) — copy to coding agent.
- [User Guide](PANDUAN-MULAI-LOW-AGENT.md) — run/monitor/resume.
- [README-SERVER](README-SERVER.md) — **manual** PM2 + Nginx + aaPanel operations, not an installer.
- [Documentation Map](docs/DOCUMENTATION-MAP.md) — technical specs and task navigation.

Development uses **main** as approved; no full reset or forced overwrite. Work on a small task, test, preview, checkpoint, continue. Security-critical implementations are not declared production-ready without independent review.
