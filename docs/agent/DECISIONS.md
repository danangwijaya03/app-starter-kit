# Accepted architecture decisions

- Source: existing GitHub repo `danangwijaya03/app-starter-kit`, branch `main`.
- Preserve existing Next.js 16.4.3 npm app until P01, then use Git moves to `apps/web`; never re-init app.
- npm/npx only; npm Workspaces and Turborepo monorepo target with one `package-lock.json`.
- Future Hono API, BullMQ worker, installer CLI, MySQL/Drizzle, Better Auth and database-driven RBAC.
- CMS hybrid blocks, Salt & Pepper default theme, four main sidebar categories.
- Production: build/upload archive, Node PM2 with aaPanel/Nginx, MySQL and Redis services, no Docker.
- Initial Super Admin `admin@codelight.id`, bootstrap secret + first login forced change; never hardcode password.
- 17 phases, 157 atomic tasks, checkpoint/resume and gates. All tasks pending until real verification.
