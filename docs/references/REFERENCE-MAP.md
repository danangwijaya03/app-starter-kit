# Reference Map — architecture-v2 curated sources

**Status:** research/adoption plan, not proof of dependency installation or source-code reuse. Prefer official documentation for package behavior. The current repository may still be a Next.js preview until the monorepo tasks are implemented.

**Binding decisions:** [Architecture Baseline v2](ARCHITECTURE-BASELINE.md) and [Adoption Protocol](ADOPTION-PROTOCOL.md). The chosen starter architecture is single-tenant **Modular Core**, not a feature installer or mandatory all-in-one CMS/worker. Core is Next.js + Hono + MySQL with Centralized Migration, Better Auth, app-level RBAC, Settings/Theme, audit, monitoring; Media, CMS and Operations are optional. Worker/Redis are conditional; independent offsite backup is required operationally for production.

## Primary reference candidates

| Source | Study / adapt | Target and ADR | Reject |
|---|---|---|---|
| [Celestia Starter](https://github.com/dev-celestia/celestia-starter) | Separation of Web/API, CMS editorial workflow, media, dashboard UX | Web/API 006-008, CMS 011, Media 010 | PostgreSQL, pnpm, installer, mobile, bundled all-on modules |
| [Hono Starter](https://github.com/Joker666/hono-starter) | Hono services, MySQL/Drizzle patterns, worker structure | API 006, database 005, jobs 009 | JWT auth ownership, Docker requirement, direct Redis enqueue without durable intent |
| [Blur Stack](https://github.com/blurridge/blur-stack) | Permission catalog, role editor, authorization-aware menu | RBAC 003-004 | Multi-tenant organization grants, PostgreSQL, second permission system |
| [Better Auth](https://www.better-auth.com/docs/) | Credential/session handling, schema generation, session revocation | Core Auth 003 | Independent RBAC created via Admin Plugin without bridge; public signup by default |
| [Hono security docs](https://hono.dev/docs/middleware/builtin/csrf) | CSRF, secure headers, middleware and API routing | Core API 006 | Assuming middleware alone replaces resource-level policy |
| [OWASP ASVS](https://github.com/OWASP/ASVS) | Testable security requirements | Security gates 003-016 | Treating a reference checklist as proof of implementation |
| [Tiptap](https://tiptap.dev/docs) | Rich text JSON within typed CMS blocks | CMS 011 | Raw HTML/JS editor, unversioned arbitrary widgets |
| [BullMQ](https://docs.bullmq.io/) | Worker, retry, backoff, deduplication behavior | Jobs 009 | Exactly-once assumptions or Redis as durable business intent |

## Other approved research and official libraries

| Source | Use when needed | Module | Gate |
|---|---|---|---|
| [shadcn/ui](https://ui.shadcn.com/), [TanStack Table](https://tanstack.com/table/latest) | Accessible components, data grid | Core UI | Preserve semantic theme; RBAC server-side |
| [React Hook Form](https://react-hook-form.com/), [Zod](https://zod.dev/) | Interactive forms and shared validation | Core/active modules | Hono validates independently |
| [Pino](https://getpino.io/) | Redacted operational JSON logs | Core | Audit stored separately in MySQL |
| [Vitest](https://vitest.dev/), [Playwright](https://playwright.dev/) | Unit/integration/browser | Core and module certification | Real MySQL; optional Redis only for jobs suites |
| [Sharp](https://sharp.pixelplumbing.com/) | Bounded image processing | Media | Input pixel, size and timeout ceilings |
| [restic](https://restic.readthedocs.io/en/stable/) | Encrypted offsite backups and restore validation | Production operations | CLI independent of app/Redis |
| [Sentry](https://docs.sentry.io/platforms/javascript/) | Optional exception reporting | Optional | Redaction, contract and cost review |
| [Novu](https://github.com/novuhq/novu) | Optional notification ideas | Future | Open-core license review; no platform import |
| [next-intl](https://next-intl.dev/) | Optional localization | Future | Separate ADR/task |
| [Better Auth plugins](https://www.better-auth.com/docs/plugins) | Optional MFA/passkeys | Future | Keep session ownership with Better Auth |

## Release placement

| Release | Mandatory scope | Reference playbooks |
|---|---|---|
| Core-first production gate | Web, API, MySQL, Auth/RBAC, Users, Settings/Theme, audit/health, CI and manual deployment, independent backup | AUTH, RBAC, SECURITY, UI-FORMS, OPERATIONS, TESTING |
| Media certification | Safe LocalFs upload, visibility, usage retention and reconciliation | MEDIA, SECURITY, TESTING |
| CMS certification | Media passed; structured blocks, immutable revisions, preview/publish/public SSR | CMS, MEDIA, UI-FORMS, TESTING |
| Jobs/Operations certification | Durable DB dispatch, Redis/worker failure recovery, Operations UI as enabled | WORKER, OPERATIONS, SECURITY, TESTING |

**Do not assume task IDs:** map each adaptation to the actual existing ID from `docs/agent/TASKS.yaml` at implementation time. Do not introduce extra tasks or an installer solely because a reference contains them. Implementation contracts and schema migration changes must be approved before code copying.

## Rules before adopting

1. Read the active task and [ARCHITECTURE-BASELINE.md](ARCHITECTURE-BASELINE.md).
2. Select a source and **pin upstream commit/tag, path, library version and license**.
3. Produce source-to-target gap against MySQL, npm, static modules, Better Auth, domain permissions, and current code.
4. Prefer supported packages/API contracts over copied source; never automatically import full starter.
5. Record licensing evidence in [SOURCE-ATTRIBUTION.md](SOURCE-ATTRIBUTION.md), and test negative/security paths.
6. Require independent review for high-risk auth, RBAC, recovery, and upload security changes.

## Domain playbooks

[AUTH.md](AUTH.md) · [RBAC.md](RBAC.md) · [CMS.md](CMS.md) · [MEDIA.md](MEDIA.md) · [WORKER.md](WORKER.md) · [SECURITY.md](SECURITY.md) · [UI-FORMS.md](UI-FORMS.md) · [OPERATIONS.md](OPERATIONS.md) · [TESTING.md](TESTING.md) · [ADOPTION-PROTOCOL.md](ADOPTION-PROTOCOL.md)

The detailed source-to-decision matrix and evidence template live in [REFERENCE-ADOPTION-MATRIX.md](REFERENCE-ADOPTION-MATRIX.md).
