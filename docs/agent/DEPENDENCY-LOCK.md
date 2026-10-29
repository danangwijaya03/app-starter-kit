# Dependency baseline (v1.2 npm)

| Item | Confirmed state / target |
|---|---|
| Next.js | Existing `16.4.3` |
| React / React DOM | Existing `19.3.0` |
| Tailwind | Existing `^4`, Turbopack loader |
| TypeScript | Existing `^5`, strict |
| Package manager | npm with existing root `package-lock.json` |
| Node runtime | Target Node 24 LTS, verify exact version |
| Workspaces | npm `workspaces` (only after P01 migration) |
| Turborepo | Future P01 install, pin compatible version |
| Hono, Better Auth, Drizzle, BullMQ | Future; verify compatibility and pin after test |

**P01 sequence:** capture `npm ci`, `npm run lint`, `npm run build` baseline; move existing source to `apps/web`, add npm workspaces and scripts, regenerate lockfile via `npm install`, then `npm ci` and targeted checks. No second `npx create-next-app`. No pnpm lock or `workspace:*` dependency specifier.

All commands for not-yet-implemented features are targets, not already available executables.
