# Accepted architecture decisions

- Source: existing GitHub repo `danangwijaya03/app-starter-kit`, branch `main`.
- Preserve existing Next.js 16.4.3 npm app until P01, then use Git moves to `apps/web`; never re-init app.
- npm/npx only; npm Workspaces and Turborepo monorepo target with one `package-lock.json`.
- Future Hono API, BullMQ worker, installer CLI, MySQL/Drizzle, Better Auth and database-driven RBAC.
- CMS hybrid blocks, Salt & Pepper default theme, four main sidebar categories.
- Production: build/upload archive, Node PM2 with aaPanel/Nginx, MySQL and Redis services, no Docker.
- Initial Super Admin `admin@codelight.id`, bootstrap secret + first login forced change; never hardcode password.
- 17 phases, 157 atomic tasks, checkpoint/resume and gates. All tasks pending until real verification.

## 2026-11-07 — incremental review and agent reasoning

- Keep work on **main**, no dev-branch requirement. No force-reset.
- Preserve the 157 task IDs/technical dependency graph; append four bounded early-preview tasks (P01-08/09, P02-07, P03-09). Front-load visible fixture UI while respecting later auth/RBAC phases.
- Each slice flows RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT. User UI review recorded asynchronously in REVIEW-QUEUE, separate from technical task completion.
- Low reasoning is default implementer for bounded work; High reasoning recommended for security-critical / architecture-heavy tasks; independent high-risk review mandatory.
- Installer has project initializer, application setup CLI and deployment manager as separate contracts; fresh install invokes CLI at extracted version before switching current symlink.
- Root static Next.js dashboard preview is a fixture; not claim of working API/MySQL.
