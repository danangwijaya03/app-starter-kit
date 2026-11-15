# IPD v2 Addendum — Cross-phase Core release and independent certification

Historic phase IDs P00–P16 and original 156 task IDs remain unchanged unless a reviewed graph rebase adds IDs. Chronology of task IDs is not the release readiness order.

1. P00–P08 establishes documentation, monorepo, DB, Auth, RBAC, UI and dashboard.
2. Before **Core Production Release**, execute/rebase **Core subset** previously grouped under P12 (typed general settings/theme/audit), **independent backup/recovery CLI** previously grouped under P14/P15, and deployment/preflight/CI/PM2/Nginx validation previously grouped under P16. No dependency on CMS or Redis; no circular task dependency.
3. P09 independent Media certification. P10–P11 CMS certification (requires Media).
4. P13 Jobs subsystem certification; P14/P15 Operations UI and advanced verification certification (not destructive dashboard restore).
5. P16 full clone and all selected-module matrix gate; not a blocker for earlier Core production if approved Core gate prerequisites complete.

When moving/splitting tasks, preserve their original ID/card/status/evidence; new scoped tasks only with unique IDs + task count and DAG validator update. Required evidence includes independent high-risk reviewer for P04/P05/P14/P15.

See `docs/architecture/TASK-REBASE-PLAN.md`.
