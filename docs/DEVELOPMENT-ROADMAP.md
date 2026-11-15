# Development Roadmap — Modular Core v2, Reference-Driven

**Approved target design, not yet implemented.** Project clone remains single-tenant, npm monorepo, Next.js/Hono/MySQL, no project installer/Docker. Optional Media, CMS, Jobs/Operations; worker+Redis conditional. One active coding agent per scoped task, model/provider-neutral, independent high-risk review.

**Source currently:** root Next.js demo preview. It is not a working Hono/MySQL/auth/worker implementation.

## Milestones, not strict phase order

| Milestone | Core or optional | Exit evidence |
|---|---|---|
| **M0** Architecture frozen | Core | [16 ADRs](architecture/ADR/README.md), [v2 contracts](architecture/README.md), [task registry](agent/TASKS.yaml) DAG, reference sources |
| **M1** Core functional | Core | Better Auth sessions + active/invited status, Hono RBAC limited delegation, user/admin UI, Drizzle 21-table shared migration and Core dashboard |
| **M2** Core production readiness | Core | P12 Core settings/theme/audit; P14-08 encrypted offsite backup, P15 independent recovery CLI; P16-11 CI/manual deployment/PM2/Nginx, reviewed security; Core-only **no Redis/worker/Media/CMS** |
| **M3** Media | Optional | P09-07 safe LocalFs public/private, lifecycle, reference-safe delete |
| **M4** CMS | Optional requires Media | P11-07 immutable block revisions and idempotent save, published-only SSR, protected preview |
| **M5** Jobs/Operations | Optional | P13-06 durable BullMQ replay with Redis; P14-07 optional Operations status UI; Core backups are independent |
| **M6** Full selected module matrix | Conditional certification | P16-12 clean clone, active/disabled route + permissions, config hash, security and recovery exercise |

**Cross-phase work:** P12-03 Media branding is optional and must not block Core theme; Core settings use static fallback. Optional worker build P16-02C must not block web/API P16-11. Backend routes/Next pages/OpenAPI/nav/grants for disabled modules are absent or return 404. No conditional database migrations.

## Technical workstream P00–P16

Full task counts/dependencies: [PHASES.md](agent/PHASES.md). Registry has **162 tasks**: 156 preexisting IDs plus P01-10/P03-10/P05-10/P13-07/P14-08/P16-12. Work only the next ready task based on actual `depends_on`, not a chronological list of phase numbers. All unimplemented task states remain pending after documentation edits.

## Agent execution

RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.

1. Read active card + [v2 Reference Index](references/INDEX-V2.md) and only matching domain contract; compare version/license/compatibility before adaptation.
2. Implement smallest testable vertical slice, keeping runnable preview. Static demo labelled DEMO, real API/DB only once verified.
3. Run real unit/integration/negative, MySQL concurrency, cache/publish or Redis outage tests by risk. High-risk requires independent qualified review, but no specific AI reasoning model.
4. Record exit codes, source fingerprint, preview and checkpoint. Continue unrelated safe tasks without waiting for UI review feedback; destructive live actions always require explicit operator approval.

## Boundaries

Core DB schema centralized and includes optional tables. Auth via Better Auth, business permissions via application RBAC; admin email operator-supplied, role delegation bounded. Published CMS SSR without persistent cache in MVP, no forced revalidate. Jobs via MySQL durable intent/lease and BullMQ at-least-once. Recovery independent CLI + restic offsite, no HTTP restore.

[Unified SPEC](../SPEC-001-app-starter-kit-modular-core.md) · [Architecture v2](architecture/README.md) · [Task Rebase Record](architecture/TASK-REBASE-PLAN.md) · [Manual Clone](MANUAL-CLONE-SETUP.md).
