# Accepted architecture decisions

- Source: existing GitHub repo `danangwijaya03/app-starter-kit`, branch `main`.
- Preserve existing Next.js 16.4.3 npm app until P01, then use Git moves to `apps/web`; never re-init app.
- npm/npx only; npm Workspaces and Turborepo monorepo target with one `package-lock.json`.
- Future Hono API, BullMQ worker, installer CLI, MySQL/Drizzle, Better Auth and database-driven RBAC.
- CMS hybrid blocks, Salt & Pepper default theme, four main sidebar categories.
- Production: build/upload archive, Node PM2 with aaPanel/Nginx, MySQL and Redis services, no Docker.
- Initial Super Admin `admin@codelight.id`, bootstrap secret + first login forced change; never hardcode password.
- 17 phases, 157 atomic tasks, checkpoint/resume and gates. All tasks pending until real verification.

## Documentation alignment — 2026-11-07 (branch dev)

- Added high-level [architecture](../ARCHITECTURE.md), [roadmap](../ROADMAP.md), [agent workflow](../AGENT-WORKFLOW.md), [deployment](../DEPLOYMENT.md), and [progress](../PROGRESS.md) overview. These are navigation/implementation guidance, not claims of code completion.
- Keep existing P00–P16 phase mapping, 157 task IDs, registry dependencies and evidence CLI. Do **not** overwrite/renumber tasks from a simplified blueprint.
- Existing approved Turborepo target stays in place alongside npm workspaces; any removal/deferment requires a scoped ADR, task-card/registry alignment and tests. Package manager remains npm/npx.
- `dev` is working branch; `main` remains baseline until explicitly instructed otherwise. No production deployment or data mutation authorized.
- Implementer (e.g. GPT-6.1 Sol Medium) runs focused tests per task; independent QA (e.g. GPT-5.6 Terra) reviews milestones and high-risk work according to existing test policy.
