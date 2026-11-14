# Development Roadmap — clone-based starter and reference-driven delivery

**Branch:** `main`. **Implementer:** coding agent yang dipilih. **Reusable deployment:** clone + manual configuration (no installer, no project initializer, no portable archive/symlink switch, no Docker requirement). **Reference source:** [Reference Map](references/REFERENCE-MAP.md).

## Architecture target

Three Node runtimes: Next.js public/admin web; standalone Hono business API with Better Auth, server-side RBAC, MySQL/Drizzle; BullMQ worker using Redis. npm workspaces/Turborepo, single tenant per clone, Salt & Pepper UI, media/CMS/backup modules. Existing source is still root Next.js 16.4.3 with static preview only; task registry is a plan, not completed functionality.

## Incremental delivery

**RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.** Select one ready task and one relevant domain reference; adapt only compatible patterns from Celestia/Blur/Hono Starter and official libraries. Preview routes must identify fixture vs integrated API/DB/permission. A runnable app/reproducible diagnostic is expected per safe increment, not after all phases. A reviewer with an appropriate independent security perspective must approve high-risk work; that reviewer is **not required to use a High Reasoning AI model**.

| Phase | Reviewable target |
|---|---|
| P00 | Static Next.js UI, docs/graph/reference requirements |
| P01 | npm monorepo with web/API/worker; Salt & Pepper fixture and preview smoke; **three apps only** |
| P02 | Existing Lerd MySQL/Redis separated dev/test; dev-only service health |
| P03 | Generated Better Auth/Drizzle MySQL schema and safe DB readiness |
| P04 | Real login/logout/password-reset/session |
| P05 | RBAC, role/admin bootstrap **as a manual npm command**, negative and race tests |
| P06 | Authenticated admin shell replacing static fixture |
| P07 | Real users/roles matrix |
| P08 | Authorized dashboard metrics |
| P09 | Private media and uploads |
| P10 | CMS editor/draft/revision/publish |
| P11 | Published-only public CMS, private preview |
| P12 | Persisted settings, branding, theme |
| P13 | Queue/worker retry and health |
| P14 | Verified encrypted backup |
| P15 | Staged restore/recovery in isolated environment |
| P16 | **Manual clone/setup/deploy verification** with npm migration/seed/admin scripts, PM2, aaPanel Nginx, E2E and recovery rehearsal; no installer/release archive |

**P01-08/P01-09**, **P02-07**, **P03-09** are early preview/diagnostic tasks added previously. Existing tasks keep stable identifiers when still relevant; obsolete installer-only tasks are removed and P16 task names/contracts are updated in `TASKS.yaml`. Run `.venv-agent/bin/python tools/agent_tasks.py summary` to see current count/status, not archived counts.

## Reference-driven feature sequence

Core: Better Auth → DB role/permission engine → Hono guards → public/private CMS → media → worker → backup/restore → documented production setup. See [Adoption Protocol](references/ADOPTION-PROTOCOL.md).

Optional future candidates **not part of the initial task graph**: 2FA/passkeys, notifications, SMTP email templates, data table upgrades, S3/R2 storage, webhooks, internationalization, audit enhancements, error monitoring, job dashboards. Every option needs explicit selection and a scoped implementation task.

## Review and quality gates

- Technical task statuses: `pending`, `in_progress`, `blocked`, `completed`, `verified`; user UI review separate in `docs/agent/REVIEW-QUEUE.md`.
- Code/DB work requires relevant tests after final edit; visual mock does not prove API integration.
- High-risk independent review and operator approval of production mutations remain separate controls.
- Session checkpoint records files, command+exit, preview, reference version/license, unfinished blockers and next safe task.
