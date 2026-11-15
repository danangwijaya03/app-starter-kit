# Reference Architecture Baseline — v2.0

Status: **approved design baseline, not proof of implementation**. This document makes reference adoption safe even before the proposed ADR files have been merged. It summarizes the 16 decisions agreed in the architecture review; it does not replace PRD/TRD/BSD/AFD migration until their v2 changes are merged.

## Precedence when sources disagree

1. Approved v2 Architecture Decision Records (when installed) and this baseline.
2. Updated implementation contracts, active module configuration and verified DB/API schemas.
3. Aligned PRD/TRD/BSD/AFD/roadmap and the active `TASKS.yaml` task.
4. These domain reference playbooks.
5. Third-party starter kits, articles, examples and old tasks (research only).

When documentation still conflicts, **stop the affected security-sensitive implementation**, record the conflict and obtain an architecture decision. Never reinterpret a third-party example as authority.

## Approved architecture decisions

| ADR | Decision | Non-negotiable invariant |
|---|---|---|
| 001 | Single-tenant modular monolith | No default microservices, no installer, one clone per deployment |
| 002 | Static module configuration | Modules enabled at build/deploy; dependency closure checked |
| 003 | Better Auth + application RBAC | One identity/session owner and one business permission owner |
| 004 | Limited permission delegation | Admin cannot grant protected permissions/roles or self-escalate |
| 005 | Centralized MySQL migrations | Shared schema and journal independent of enabled modules |
| 006 | Standalone Hono API | Same-origin `/api/auth/*` and `/api/v1/*` behind Nginx |
| 007 | Next.js server/client boundary | Direct browser API; server-side Hono HTTP, no duplicate BFF |
| 008 | SSR-first CMS caching | Admin no-store; public CMS SSR without persistent cache in MVP |
| 009 | Durable job dispatch | MySQL job intent; BullMQ/Redis/worker optional |
| 010 | LocalFs + S3-ready adapter | Files outside webroot, public/private isolation, safe lifecycle |
| 011 | Structured, versioned CMS blocks | Immutable revisions, optimistic concurrency, published-pointer isolation |
| 012 | Unified semantic theme | Immutable theme snapshots, global branding, per-user mode |
| 013 | Independent disaster recovery | Encrypted offsite backups, CLI-only production cutover |
| 014 | Automatic CI, manual production deploy | Approved commit SHA, gated migrations and smoke tests |
| 015 | Lightweight Core observability | Pino JSON, transactional audit, health, external uptime |
| 016 | Core-first release | Optional modules certified with dependencies independently |

## Module contract

- **Core always on:** Auth, RBAC, users, settings, semantic theme, audit, health and API. Requires Web + Hono + MySQL.
- **Media optional:** LocalFs upload/delivery and usages. No Redis required for limited synchronous operations.
- **CMS optional:** Depends on Media. Structured blocks, revisions, public SSR.
- **Operations optional:** Operations dashboard; requires jobs capability. Independent production backup CLI is **not** part of Operations and is mandatory for a production deployment.
- **Jobs capability conditional:** Worker + Redis are required only when at least one enabled module requests background processing.
- **All tables migrated centrally:** Disabling a module neither drops tables nor automatically restores old permission grants if enabled later.

### Module activation preflight

Reject unknown module, missing dependency, dependency cycle, Web/API config mismatch, missing required runtime, and permission catalog mismatches. Disabled module must expose no API or admin pages, navigation, permission grants, worker processors or OpenAPI operations. Do not treat UI hiding as authorization.

### Boundary contract

`apps/web` must not import DB or server-only API services. `apps/api` owns HTTP, auth middleware, domain services and persistence. `apps/worker` shares server-safe services, not Hono routes. `packages/contracts` is Zod/DTO without database access. `packages/database` defines every table and one migration journal. CMS schema/renderer/editor must have separate exports.

## Reference adoption gate

Every implementation must record: active task ID; module and ADR; exact upstream URL/tag/commit; license/path; code vs pattern vs package; rejected upstream assumptions; source-to-target gap; DB/API/permission effects; positive/negative tests; independent reviewer where high-risk. See [ADOPTION-PROTOCOL.md](ADOPTION-PROTOCOL.md) and [REFERENCE-ADOPTION-MATRIX.md](REFERENCE-ADOPTION-MATRIX.md).

This baseline is documentary design, **not** evidence that the monorepo, tests, worker, CLI or production deployment exists.
