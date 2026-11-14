# PRD — Product Requirements Document

**ID:** PRD-1.0 | **Date:** 2026-10-28 | **Status:** Implementation baseline | **Owner:** Product/Engineering

> **Existing repository baseline (2026-10-29):** Next.js 16.4.3 / React 19.3.0 already exists at the Git repository root. Development uses **Lerd + Node.js 26 + npm/npx + existing MySQL and Redis services**. P01 will migrate the existing app to npm Workspaces / apps/web; do not recreate it. For operational details see [LOCAL-LERD-NODE26.md](agent/LOCAL-LERD-NODE26.md). The requirements below describe the future completed product, not features already shipped.

## PRD-01 Purpose and success

Provide a scalable, repeatable single-tenant starter kit for business dashboards, inventory/PO tools, CRM, company websites, and administrative applications. A newly initialized project must not inherit user data, secrets, sessions, audit trails or backups from the template. Backend remains useful for future native/mobile consumers.

**Success criteria:** a development environment can be initialized from an existing clean clone; a fresh manual clone + configured production build produces a functioning login, permission-limited admin shell, CMS public pages, settings and backup workflows; adding a new module through module registry does not require changing existing RBAC internals or main menu shell.

## PRD-02 Actors and roles

| Actor | Goals | Boundaries |
|---|---|---|
| Visitor | Read published public CMS pages | No admin/API private content |
| Viewer | Read permitted dashboard/records | No mutation |
| Content Editor | Manage draft, media and publish with grants | No user/system management by default |
| Administrator | Manage users, standard roles and app content | Cannot elevate to protected super_admin; no critical recovery by default |
| Super Admin | Global system administration and recovery | Protected from last-owner lockout, re-auth for critical actions |
| Coding agent/developer | Extend modules and verify implementation | No automatic access to production data/secrets |

Default roles are system seed templates. A user can hold multiple roles; grant union, no explicit deny for MVP. Public signup is disabled. Super Admin role has protected system semantics and sees all registered active permissions. Admin creation is private/secure, invitation-first when email is configured.

## PRD-03 Scope and priority

**MVP (MUST):**

1. Login/logout/password reset/first-login password change, session status, profile.
2. Admin dashboard with permission-aware registry widgets and recent activity.
3. Users CRUD (non-destructive deactivation), search/filter/pagination, role assignment, session revocation.
4. Roles CRUD, grouped permission checkbox matrix, system role protection, module permission registry, authorization audit.
5. CMS pages, versioned revisions, block editor, save draft, preview, publish/unpublish, public rendering, basic SEO.
6. Media library: secure upload, metadata, reference-safe delete, filesystem storage adapter.
7. Public navigation menus, 2-level nesting and ordered links.
8. General settings (name, short name, logo, favicon, language, timezone/date format), theme appearance and Salt & Pepper default preset.
9. Audit log viewer, system job status, verified MySQL backup; staged restore and documented recovery controls.
10. OpenAPI docs for business API, typed contracts, migrations and repeatable system seed.
11. Clone-based manual setup and production deployment without Docker; npm migrate/seed/admin scripts, PM2 and aaPanel/Nginx guidance.
12. Reference-driven feature docs + server README + selected coding agent task/checkpoint workflow and CI/manual-deploy verification.

**Later (SHOULD/OPTIONAL, not MVP):** multi-tenant organization management, 2FA/SSO/passkeys, scheduled publication, multilingual content, arbitrary custom content types, drag-and-drop Webflow-style builder, S3 storage adapter (interface in MVP), multi-node clustering, notification/webhook, feature flag UI, custom dashboard builder, theme marketplace, advanced workflow approvals.

## PRD-04 Information architecture

```text
Dashboard
Manage Content
  - Pages
  - Media Library
  - Navigation
Manage User
  - Users
  - Roles & Permissions
Setting
  - General
  - Appearance
  - Backup & Restore
  - Audit Logs
```

Profile/logout accessible from user dropdown, not top-level sidebar. Admin navigation is a registry controlled by RBAC; **public CMS navigation is independent**.

## PRD-05 Functional requirements (stable IDs)

| ID | Priority | Requirement | Acceptance signal |
|---|---|---|---|
| AUTH-REQ-01 | MUST | Email/password sign-in with secure session | Valid account redirects to first authorized page; invalid creds rejected without account enumeration |
| AUTH-REQ-02 | MUST | Password reset with expiring single-use token | Reused/expired tokens rejected; no credential exposed in logs |
| AUTH-REQ-03 | MUST | Initial bootstrap must_change_password | Only password change/logout allowed until completed; old sessions revoked |
| AUTH-REQ-04 | MUST | Public self-registration disabled | Public sign-up denied and tested |
| DASH-REQ-01 | MUST | Permission-aware widgets | Role without widget grant never receives restricted data |
| USER-REQ-01 | MUST | User listing/search/status/role management | Filters/page state stable; only authorized API access |
| USER-REQ-02 | MUST | Multiple roles and last super-admin protection | Concurrent attempts cannot remove all active super_admin users |
| RBAC-REQ-01 | MUST | CRUD roles/permission matrix | Exact registry codes, group select-all, save/reload correct |
| RBAC-REQ-02 | MUST | Deny by default backend | 401 no auth; 403 no permission, including direct API calls |
| RBAC-REQ-03 | MUST | Module manifest + sync | New permission shows in editor after sync, not auto-granted |
| CMS-REQ-01 | MUST | Pages and immutable revisions | Editing draft does not change published page or slug |
| CMS-REQ-02 | MUST | Preview/publish/unpublish | Preview requires authorized short-lived session; public only published revision |
| CMS-REQ-03 | MUST | Typed block registry | Invalid block props rejected; missing renderer handled safely |
| CMS-REQ-04 | MUST | Public SEO | Title, description, OG assets reflect published revision |
| MEDIA-REQ-01 | MUST | Safe upload | Server validates type, size, signature, authorized storage key |
| MEDIA-REQ-02 | MUST | Safe delete | Files referenced by published content cannot be deleted |
| NAV-REQ-01 | MUST | 2-level public nav | No cycle/cross-menu parent; unpublished links excluded |
| SET-REQ-01 | MUST | General branding configuration | Name/logo update without rebuild after cache invalidation |
| THEME-REQ-01 | MUST | Salt & Pepper preset customizable | Light/dark/system and validated semantic tokens |
| AUDIT-REQ-01 | MUST | Non-editable audit history | Role, publishing, settings, backup and restore events searchable |
| BAK-REQ-01 | MUST | Consistent backup + checksum | Artifact verified and restorability checked in isolated database |
| BAK-REQ-02 | MUST | Controlled restore | Re-auth, staging validation, maintenance/lock, no auto-retry |
| REL-REQ-01 | MUST | Manual clone + setup | Fresh project clone uses unique env/DB/Redis/storage, reviewed npm scripts, builds and runs web/api/worker without Docker |
| REL-REQ-02 | MUST | Idempotent manual setup scripts | Re-run migration checks, permissions, seeds/admin bootstrap does not duplicate users/roles or reset passwords |
| AGENT-REQ-01 | MUST | Phase task checkpoint system | Fresh agent session resumes WIP correctly and avoids repeats |

## PRD-06 Module behaviors

### Auth and security

- Only authenticated/active users can access admin business APIs; session revoke/disable becomes effective at next protected request.
- First login sets a server-side must_change_password flag in user_profiles; enforcement also applies to API.
- A bootstrap account uses admin@codelight.id; initial password supplied via protected non-echo manual setup input, never embedded in source/docs. Require unique production password and change on first login.
- Protected role changes, backup restore and credential actions require recent re-authentication.

### CMS

- Page editor: block picker, preview canvas, properties; MVP supports reordering, no arbitrary code injection.
- Every save produces a new immutable draft revision; publish advances an atomic pointer to a revision of that page.
- Slugs unique only in published namespace; draft slug conflict checked at publish; homepage slug / reserved for one published page.
- Rich text via Tiptap, structured JSON, sanitization, no executable JSX/HTML from CMS fields.
- Media references across published revisions must remain valid; archive retains history.

### Settings

- Setting categories: General, Appearance, Backup & Restore, Audit Logs.
- Global app preset stored in DB with source-defined fallback; separate per-user color-mode preference.
- Secrets are environment-only, never editable in Settings UI.

### Backup/restore

- Logical dump of compatible MySQL InnoDB tables; manifest includes schema/app version, checksum, encryption metadata and media coverage.
- Backup database only is distinguished from full app backup. Restore from verified managed artifact only in MVP.
- Restore workflow must maintain off-database journal, pre-restore snapshot and documented recovery path; never promise atomic import.

## PRD-07 Nonfunctional acceptance

| Dimension | MVP target / method |
|---|---|
| Accessibility | Keyboard operation, visible focus, reduced motion; WCAG 2.2 AA targeted |
| Authorization | All private endpoint operations deny by default; negative permission tests |
| Reliability | Health probes for web, API, DB, Redis, worker; resumable jobs; controlled maintenance |
| Performance | Paginated queries and indexes; measure baseline for representative seeded datasets; no invented SLA |
| Security | CSRF/session safeguards, input validation, upload screening, audit, least privilege |
| Portability | Tested Node/npm dependency install and production build on target Linux; manual PM2/Nginx deployment |
| Maintainability | Strict TypeScript, automated validation, stable task IDs, docs updated on contract changes |
| Data integrity | FK/unique constraints, transactions for role/publish invariants, safe migration process |

## PRD-08 Out of scope and product decisions

- No Docker in production. Local development reuses **existing Lerd MySQL and Redis**, with no duplicate database/Redis container or daemon for this project.
- No automatic production deployments or destructive restores by coding agent.
- No built-in ERP/PO functionality; future business modules plug in through registry.
- No public sign-up, no multi-tenancy or self-service tenant provisioning in MVP.
- UI design is Salt & Pepper (#FFFFFF, #D4D4D4, #B3B3B3, #2B2B2B) with semantic status colors where necessary.

## PRD-09 Traceability

Use IDs above in tests and phase tasks. Technical resolution in TRD, flows in AFD, visual detail in DBD, schema/API in BSD, and execution sequence in IPD. New requirements must be added with impact to all affected documents and tasks. The live task registry is [TASKS.yaml](agent/TASKS.yaml); it governs execution status, not product requirements.

## PRD-10 Incremental preview and reviewability (2026-11-07)

- **DEV-REQ-01 (MUST):** Each meaningful delivery slice keeps source runnable, relevant tests repeatable and a user-visible preview or safe diagnostic before the full project finishes.
- **DEV-REQ-02 (MUST):** Fixture/mock and integrated/API-backed states must be visibly differentiated. Never imply authentication, persistence or permissions exist merely because a layout renders.
- **DEV-REQ-03 (MUST):** Log verified preview route and reproduction steps, test evidence, unresolved limitations and explicit user feedback separately from technical task completion.
- **DEV-REQ-04 (MUST):** selected coding agent implements all bounded tasks using curated official/source references. No High Reasoning model is required. Effective high-risk implementation requires independent qualified security review.
- **DEV-REQ-05 (MUST):** Continue unrelated safe tasks without waiting for user visual approval; revision feedback creates bounded new work.
- **DEV-REQ-06 (MUST):** Preserve main branch, existing Next.js scaffold, npm tooling, Lerd services and production no-Docker rule.

See [Development Roadmap](DEVELOPMENT-ROADMAP.md), [Preview/Feedback](agent/PREVIEW-AND-FEEDBACK.md) and [Agent Routing](agent/SINGLE-MODEL-WORKFLOW.md).
## PRD-11 Clone-based and reference-driven reuse (2026-11-14)

- **CLONE-REQ-01 (MUST):** Each new project is an independent Git template clone with private config, unique DB/Redis/storage and manual npm setup; never copy sessions/media/backups/secrets.
- **CLONE-REQ-02 (MUST):** No installer CLI, project generator, release archive manager, Docker requirement or symlink switch workflow.
- **REF-REQ-01 (MUST):** Task-specific reference mapping, version/license/compatibility check and attribution for copied source. Official packages preferred.
- **REF-REQ-02 (MUST):** selected coding agent completes bounded positive/negative tests; high-risk tasks are not marked complete without independent qualified review.
- **REF-REQ-03 (SHOULD):** Catalog optional reusable ideas (2FA, notifications, i18n, observability, optional storage) without making them new MVP requirements automatically.

See [Reference Map](references/REFERENCE-MAP.md), [Manual Clone](MANUAL-CLONE-SETUP.md), [Single Model](agent/SINGLE-MODEL-WORKFLOW.md).
