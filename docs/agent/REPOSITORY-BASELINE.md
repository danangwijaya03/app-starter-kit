# Verified repository baseline — 2026-10-29

- Repository: https://github.com/danangwijaya03/app-starter-kit (`main`, private).
- Root Next.js `16.4.3`, React/ReactDOM `19.3.0`, Tailwind v4, TypeScript strict; root `package-lock.json` uses npm.
- Existing files: `app/`, `public/`, `next.config.ts`, `tsconfig.json`, `eslint.config.mjs`, `package.json`, `package-lock.json`, `AGENTS.md`, `README.md`, `LICENSE`.
- Next.js config already enables `cacheComponents`, `partialPrefetching`, `experimental.agentFeedback`, and Turbopack CSS loader rules. Preserve unless scoped tests justify changes.
- Next.js generated AGENTS.md rules have been preserved. Never delete them or recreate the Next.js app.
- P01 moves existing app to `apps/web` and updates root to npm Workspaces/Turborepo with one root lockfile. This is NOT done by the documentation commit.
- Local development: Lerd + Node 26 + existing MySQL; reuse Lerd Redis. Verify actual version and host connection before P02. See [LOCAL-LERD-NODE26.md](LOCAL-LERD-NODE26.md).
- Production target: non-Docker uploaded artifact, Node.js/PM2 + aaPanel/Nginx, MySQL/Redis server services.
- CI/build not yet verified by this documentation commit. P01 must record real baseline checks.
