# v1.2 — npm + existing GitHub Next.js scaffold

- Documentation and low-agent workflow integrated directly into `main`, without relocating the existing application.
- Replaces pnpm workflows with npm/npx + planned npm Workspaces/Turborepo.
- Preserves Next.js 16 generated `AGENTS.md` block verbatim.
- P01 task cards now guide moving the **existing** Next.js into `apps/web`, never scaffolding a second app.
- All feature task statuses remain pending; no npm install/build or application tests were executed as part of docs-only commit.
- Production target remains build/upload without Docker.
