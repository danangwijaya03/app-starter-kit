# Roadmap v2 Addendum — Core-First delivery

**M0 specification:** ADR register / dependency graph / task rebase approved.
**M1 Core functional:** P01–P08 subset + Auth/RBAC integration tests pass.
**M2 Core production:** settings/theme/audit Core subset (historical P12), backup + recovery CLI (historical P14/15) and manual deployment/CI components (historical P16) verified. Core-only deploy must not require Redis or CMS.
**M3 Media certification:** P09.
**M4 CMS certification:** P10–P11 with Media.
**M5 Jobs/Operations certification:** P13–P15 optional components.
**M6 Full starter release:** P16 selected active-module matrix, disaster recovery drill, security signoff.

P12-03 Media branding picker depends on P09 and is not Core prerequisite. P16-02C worker production build is optional for Core-only. Preserve task IDs and original test evidence; modify dependency DAG only through reviewed task graph rebase, not directly from this overview.
