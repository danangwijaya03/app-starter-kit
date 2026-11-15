# Roadmap P00–P16 — Modular Core Architecture v2

**Status:** approved target design, **not proof of running implementation**. Technical registry: **162 tasks** (156 old IDs preserved + P01-10, P03-10, P05-10, P13-07, P14-08, P16-12), all pending until verified. No installer or Docker requirement. One active coding agent, provider/model neutral.

## Cross-phase release checkpoints

- **M0**: v2 ADRs/contract baseline + task graph verified.
- **M1 Core functionality**: Hono, Next.js, MySQL/Drizzle, Better Auth, RBAC, Core dashboard/health.
- **M2 Core production readiness (P16-11)**: Core settings/theme/audit (P12 subset), independent offsite backup + operator recovery CLI (P14/P15 subset), manual CI + PM2/Nginx deploy. Web/API/MySQL only; **no Redis/worker/Media/CMS/Operations requirement**.
- **M3 Media certification (P09-07)**: optional media lifecycle and security.
- **M4 CMS certification (P11-07)**: requires certified Media.
- **M5 Jobs/Operations certification (P13-06, P14-07)**: optional Redis/BullMQ and Operations UI; backup CLI exists independently.
- **M6 Full selected-module certification (P16-12)**: validate all chosen module combinations after Core.

| Milestone | Phase | Tasks | Technical objective |
|---|---|---:|---|
| M0/M1 | [P00 — Specification & Agent Setup](phases/P00-specification-and-agent-setup.md) | 5 | Design baseline and architecture v2 ADRs, source provenance and graph integrity |
| M0/M1 | [P01 — npm Monorepo Foundations](phases/P01-monorepo-and-build-foundations.md) | 15 | Keep existing Next scaffold, add Next+Hono with worker scaffold optional; static modules config |
| M0/M1 | [P02 — Lerd Local Infrastructure](phases/P02-local-infrastructure.md) | 7 | Isolated MySQL dev/test; Redis only when jobs are enabled |
| M0/M1 | [P03 — Central MySQL Database](phases/P03-database-foundation.md) | 12 | Drizzle single migration journal, 21 logical tables and Better Auth-generated schema |
| M1 | [P04 — Authentication](phases/P04-authentication.md) | 7 | Better Auth credential/session, invited users and first-login guards |
| M1 | [P05 — RBAC and Admin Bootstrap](phases/P05-rbac-and-initial-administrator.md) | 13 | One server permission engine, limited delegation and locked last-admin invariant |
| M1 | [P06 — Admin Design System](phases/P06-design-system-and-admin-shell.md) | 9 | Authorized UI shell and semantic tokens |
| M1 | [P07 — User & Roles](phases/P07-user-and-role-management.md) | 7 | Account management and bounded role delegation |
| M1 | [P08 — Core Dashboard](phases/P08-dashboard.md) | 5 | Role-scoped widgets without Media/CMS/Operations dependencies |
| M2/M3/M4 | [P09 — Media Module](phases/P09-storage-and-media-library.md) | 7 | Optional safe LocalFs media, public/private delivery and deletion protection |
| M2/M3/M4 | [P10 — CMS Editor](phases/P10-cms-page-editor-and-revisions.md) | 12 | Optional CMS after Media, immutable revisions and idempotent save |
| M2/M3/M4 | [P11 — Public CMS](phases/P11-public-cms-and-navigation.md) | 7 | Optional published-only SSR without persistent cache and protected preview |
| M2/M3/M4 | [P12 — Settings, Theme & Audit](phases/P12-settings-and-appearance.md) | 8 | Core typed settings, immutable themes, audit; P12-03 media branding is optional |
| M2/M5/M6 | [P13 — Jobs & BullMQ](phases/P13-background-worker-and-queue.md) | 7 | Optional Redis/worker, durable MySQL intent and dispatcher with lease/replay |
| M2/M5/M6 | [P14 — Independent Backup & Operations UI](phases/P14-backup.md) | 10 | P14-01..04 and P14-08 independent offsite backup for Core; P14-05..07 optional Operations UI |
| M2/M5/M6 | [P15 — Independent Disaster Recovery](phases/P15-restore-and-recovery.md) | 10 | Operator-only independent CLI, isolated staging and manual cutover, no HTTP restore |
| M2/M5/M6 | [P16 — Manual Deploy and Certifications](phases/P16-manual-clone-and-deployment.md) | 21 | P16-11 Core release without Redis/Media/CMS; P16-12 optional module matrix after Core |

**Phases are historic workstream IDs, not strict release chronology.** Actual `depends_on` in TASKS.yaml controls execution; M2 Core gate depends only on Core prerequisites. Optional module tasks may remain pending without preventing Core production readiness. Do not mark a phase verified merely because Core gate passes.

## Agent and security gates

**RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT**. Use [Architecture](../architecture/README.md), [Reference Map](../references/REFERENCE-MAP.md), [Adoption Protocol](../references/ADOPTION-PROTOCOL.md) and [Test/Release](../architecture/TESTING-RELEASE.md).

Any suitable coding agent (Codex, Claude, Antigravity, DeepSeek, etc) may implement bounded task. Independent high-risk security review remains required, with separate operator authorization for live migrations/recovery/deployment.
