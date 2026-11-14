# Reference Map — curated reuse candidates

**Status:** architecture/development research. No third-party source has been incorporated into this repository by this documentation change. References are patterns to evaluate, not proof that the same stack, database or API version already works here.

**Project invariants:** Next.js 16 + React 19 frontend, standalone Hono API, BullMQ worker, MySQL/Drizzle, Better Auth and server-side permission checks. npm workspaces/Turborepo, one lockfile, single tenant per clone, no installer, no Docker requirement, deployment via build + PM2 + aaPanel/Nginx. Coding implementer: **coding agent yang dipilih** for all bounded tasks. See [Adoption Protocol](ADOPTION-PROTOCOL.md), [Single Model Workflow](../agent/SINGLE-MODEL-WORKFLOW.md).

## Primary reference candidates

| Capability | References (verified pages) | Reuse approach | Important mismatch |
|---|---|---|---|
| Web/API separation, typed contracts, CMS workflow | [Celestia Starter](https://github.com/dev-celestia/celestia-starter) | Study architecture, auth/dashboard/CMS/access feature patterns | PostgreSQL, pnpm, CLI/feature installer and optional mobile are **not** our architecture |
| Backend MySQL, Hono, queue | [Hono Starter](https://github.com/Joker666/hono-starter) | Study layered API, MySQL/Drizzle, BullMQ worker patterns | JWT-based auth and Docker examples; do not replace Better Auth or require Docker |
| Role/permission and navigation maps | [Blur Stack](https://github.com/blurridge/blur-stack) | Study permissions matrix and API middleware | PostgreSQL and multi-tenant concepts; adapt to MySQL/single-tenant |
| Auth/session/admin APIs | [Better Auth docs](https://better-auth.com/docs), [Admin Plugin](https://better-auth.com/docs/plugins/admin) | **Use official package**; generate schema from installed version | Review plugin permission semantics against app-level DB RBAC; one canonical authorization decision |
| API hardening | [Hono CSRF](https://hono.dev/docs/middleware/builtin/csrf), [Secure Headers](https://hono.dev/docs/middleware/builtin/secure-headers) | Official middleware + threat-model-specific tests | Middleware defaults alone do not cover API authorization/business logic |
| Security acceptance | [OWASP ASVS](https://asvs.owasp.org/) | Testable security requirements, not copy/paste source | Apply relevant controls and record how implemented |
| CMS editing | [Tiptap](https://github.com/ueberdosis/tiptap) | Core editor library for typed block editing | Headless editor is not a complete safe CMS/revision workflow |
| Async jobs | [BullMQ](https://github.com/taskforcesh/bullmq) | Official queue primitives and worker patterns | Job idempotency, retry, cancellation and backup safety remain app-specific |

## Additional reusable ideas — evaluate individually, not automatic MVP

| Feature family | Potential source | Value for business starters | Decision |
|---|---|---|---|
| UI primitives / accessible patterns | [shadcn/ui](https://ui.shadcn.com/), [TanStack Table](https://tanstack.com/table/latest) | Forms, dense data tables, keyboard UX | Prefer existing design tokens and minimal dependencies |
| Typed forms / schema validation | [React Hook Form](https://react-hook-form.com/), [Zod](https://zod.dev/) | Validation shared across UI and Hono | Server validates input independently of client |
| Audit logs and structured logging | [Pino](https://github.com/pinojs/pino) | Action traceability and operations | Never log tokens/passwords/PII by default; audit log is distinct from debug log |
| Error monitoring | [Sentry JavaScript](https://github.com/getsentry/sentry-javascript) | Production exception reporting | Optional external service; redact data and review retention costs |
| In-app / multi-channel notifications | [Novu](https://github.com/novuhq/novu) | Reusable notification ideas/workflow | **Optional**; mixed/open-core license, verify module licenses and do not add full platform as default |
| Internationalization | [next-intl](https://next-intl.dev/) | Future multilingual apps | Optional after MVP; keep language/timezone settings |
| 2FA/passkeys and session management | [Better Auth Plugins](https://better-auth.com/docs/concepts/plugins) | Optional stronger login | Keep authentication ownership inside Better Auth |
| Media adapters | [Celestia media-R2 feature](https://github.com/dev-celestia/celestia-starter) | Abstract local/S3-compatible media | Local-first; optional R2/S3 driver, no secrets in browser |
| Job dashboard | [BullMQ documentation](https://docs.bullmq.io/) | Queue visibility for operators | Authorization and retry controls mandatory; no publicly exposed queue UI |
| Automated UI/API tests | [Playwright](https://playwright.dev/), [Vitest](https://vitest.dev/) | Low-effort repeatable regressions | Fixtures isolated from development/production DB |

**Priority:** Core MUST = auth/RBAC/CMS/security, MySQL/API, media, worker, backup/restore. Suggested optional features above are **reference candidates only**, not automatic additional task IDs, tables, dependencies, or scope expansion.

## Rules for starting a feature

1. Choose **one** relevant reference page and its pinned commit/tag; verify maintenance status and LICENSE before reusing **source code**.
2. Record a short source-to-target map and security expectations in the domain document below.
3. Copy as little source as needed, preferably consume official packages rather than copying implementations. Record attribution in [SOURCE-ATTRIBUTION.md](SOURCE-ATTRIBUTION.md).
4. Avoid importing source project package manager (pnpm), DB driver (PostgreSQL), multi-tenancy, Docker, build tool, or installer just to get one feature.
5. Implement only the active TASKS.yaml work unit; run scoped positive/negative tests. For high-risk tasks, require an independent reviewer before completion, not a specific High Reasoning model.

## Domain playbooks

- [AUTH.md](AUTH.md) · [RBAC.md](RBAC.md) · [CMS.md](CMS.md) · [SECURITY.md](SECURITY.md)
- [MEDIA.md](MEDIA.md) · [WORKER.md](WORKER.md) · [UI-FORMS.md](UI-FORMS.md)
- [OPERATIONS.md](OPERATIONS.md) · [TESTING.md](TESTING.md) · [ADOPTION-PROTOCOL.md](ADOPTION-PROTOCOL.md)
