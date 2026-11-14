# app-starter-kit — single-model coding agent instructions

**Ditujukan untuk: CODING AGENT.** User-facing guide: [PANDUAN-MULAI-LOW-AGENT.md](PANDUAN-MULAI-LOW-AGENT.md). Approved development branch: **main**; no destructive reset.

**Baseline:** existing root Next.js 16.4.3 + React 19.3, Tailwind v4, npm/npx and one `package-lock.json`. P01 migrates the **existing** app using Git moves into `apps/web`. Local environment: Lerd, Node.js 26, existing MySQL/Redis. **Do not run create-next-app, install duplicate services, or create Docker requirements.**

## Mandatory startup (START and RESUME)

1. `git status --short`; inspect `docs/agent/CHECKPOINT.md`. Run **`python3 tools/bootstrap_agent.py`** (automatic scoped Python venv; Fish/Bash/Zsh compatible, no `source`).
2. Use `.venv-agent/bin/python tools/agent_tasks.py doctor`, `next`, and `summary`. If bootstrap fails, report actual blocker; do not change global Python/Lerd or task statuses.
3. Recover any `in_progress` task and actual Git evidence first. Otherwise, take only one `ready` task according to `docs/agent/TASKS.yaml`.
4. Read that single task card, `spec_refs`, corresponding domain [Reference Map](docs/references/REFERENCE-MAP.md), [Adoption Protocol](docs/references/ADOPTION-PROTOCOL.md), and relevant source. No wholesale research or all-task loading.

## Single required model and flow

**Implementer:** any selected coding agent. One active agent/model per bounded task or session, without required provider or reasoning-tier routing. `risk: high` represents security/complexity, **not a demand for a High model**; keep independent qualified review for such tasks. See [Single-Model Workflow](docs/agent/SINGLE-MODEL-WORKFLOW.md) and [Test/Review Policy](docs/agent/TEST-AND-REVIEW-POLICY.md).

**RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.**

- Work one bounded vertical slice, respecting task scopes, dependency graph, MySQL schema and server RBAC. Prefer official packages over copying code. Record upstream URL/commit/license and exclusions if adapting from Celestia, Blur Stack, Hono Starter, etc.
- Run **real scoped tests after the final edit**, including negative paths and MySQL concurrency when relevant. Record evidence with `agent_tasks.py run <ID> --kind docs|unit|integration|negative|build -- COMMAND` (do not treat recorder as sandbox).
- For UI, test current route/behavior and label fixture vs integrated. Record actual observed URL (or `not verified`) and steps in [Preview & Feedback](docs/agent/PREVIEW-AND-FEEDBACK.md) and [Review Queue](docs/agent/REVIEW-QUEUE.md).
- Complete with CLI only after acceptance/evidence; independent reviewer is required by the effective high-risk gate. Implementer cannot self-approve. If reviewer unavailable, block that task and continue other safe ready tasks.
- Commit validated increments in `main` when safe; checkpoint before task switching/session limits. **Never** claim asynchronous future completion.

## Architecture / non-negotiable boundaries

- Only three app runtimes: **Next.js web**, **Hono API**, **BullMQ worker**. MySQL/Drizzle, Better Auth, database-driven application RBAC, Redis, Salt & Pepper UI, typed Zod contracts.
- **Clone-based new projects only.** Do not implement `apps/installer`, `init-project`, release archive packaging, switch-release scripts, versioned-symlink deployment, or a feature installer. Manual npm scripts for migrate/seed/permission-sync/admin-bootstrap/verify are retained.
- Production **without Docker**: clone/pull trusted source, environment setup, review-gated migration, build, PM2, aaPanel/Nginx and health check. Live mutations/deploy/restore require explicit operator approval.
- Never store credentials, user data, uploaded media, backup archives or secrets in a starter clone. Test with isolated DB/Redis; never use live production data for fixtures.
- Preserve Next.js generated rules below and baseline config until a verified scoped migration.

<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

