# Phase Roadmap — P00–P16

**Baseline:** documentation only; task statuses remain `pending`. All dependencies in `TASKS.yaml` have been validated as an acyclic graph.

| Milestone | Phase | Tasks | Gate |
|---|---|---:|---|
| A | [P00 — Specification and Agent Setup](phases/P00-specification-and-agent-setup.md) | 5 | Semua docs, registry, checkpoint, dan aturan eksekusi terverifikasi. |
| A | [P01 — Monorepo and Build Foundations](phases/P01-monorepo-and-build-foundations.md) | 7 | Clean install, package dependency graph, minimal runtime artifact proof. |
| A | [P02 — Local Infrastructure](phases/P02-local-infrastructure.md) | 6 | MySQL/Redis dev berjalan terisolasi, env tidak bocor. |
| A | [P03 — Database Foundation](phases/P03-database-foundation.md) | 8 | Schema auth+app fundamentals dan migrations dapat diulang pada test DB. |
| B | [P04 — Authentication](phases/P04-authentication.md) | 7 | Login/reset/session aman dan first-login guard diuji. |
| B | [P05 — RBAC and Initial Administrator](phases/P05-rbac-and-initial-administrator.md) | 9 | Permission registry, super admin protections, bootstrap idempotent. |
| B | [P06 — Design System and Admin Shell](phases/P06-design-system-and-admin-shell.md) | 7 | Salt & Pepper, responsive shell, dynamic authorized sidebar. |
| B | [P07 — User and Role Management](phases/P07-user-and-role-management.md) | 7 | User CRUD/invite and role matrix dengan negative security tests. |
| B | [P08 — Dashboard](phases/P08-dashboard.md) | 5 | Widget registry and scoped metrics accessible. |
| C | [P09 — Storage and Media Library](phases/P09-storage-and-media-library.md) | 7 | Secure media CRUD, usage tracking, storage persistence. |
| C | [P10 — CMS Page Editor and Revisions](phases/P10-cms-page-editor-and-revisions.md) | 9 | Immutable revision editing and safe publish/unpublish. |
| C | [P11 — Public CMS and Navigation](phases/P11-public-cms-and-navigation.md) | 7 | Public published-only pages, nav and protected preview. |
| C | [P12 — Settings and Appearance](phases/P12-settings-and-appearance.md) | 8 | Typed settings, branding, theme changes, audit viewer. |
| D | [P13 — Background Worker and Queue](phases/P13-background-worker-and-queue.md) | 6 | Reliable worker, protected job API, retry controls. |
| D | [P14 — Backup](phases/P14-backup.md) | 7 | Encrypted verified backup and recovery manifest. |
| D | [P15 — Restore and Recovery](phases/P15-restore-and-recovery.md) | 7 | Isolated staged restore and safe maintenance/recovery flow. |
| D | [P16 — Build, Artifact and Server Release](phases/P16-build-artifact-and-server-release.md) | 11 | Portable artifact, actual aaPanel/PM2 install test, two READMEs. |

## Execution rules

1. Read root `AGENTS.md` → task registry → checkpoint → relevant phase guide.
2. Select only `pending` tasks whose all `depends_on` IDs are completed/verified.
3. Record `in_progress`, edit only scoped modules, validate and checkpoint.
4. At phase completion, run gate; promote task statuses to `verified` with evidence.
5. Do not alter production data automatically. Source code is not included in this documentation archive.

**Total predefined atomic tasks:** 123.