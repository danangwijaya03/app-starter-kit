## PRD v2 Addendum — Modular Core & MoSCoW (supersedes PRD-01 success and PRD-03 MVP scope)

**Product goal unchanged:** reusable single-tenant starter for business applications, manually cloned, no installer. **Success now has two milestones**: Core production-ready; optional modules certified independently. Existing `AUTH-REQ`, `USER-REQ`, `RBAC-REQ`, `CMS-REQ`, `MEDIA-REQ`, `NAV-REQ`, `SET-REQ` IDs remain unchanged. Their MoSCoW priority follows module classification below, without renaming them.

### Core Must

Authentication and sessions; invitation-first and optional secure reset; first-admin setup; RBAC user/role management and limited delegation; dashboard admin shell; typed settings & global theme; audit and health; Hono API and typed contracts; MySQL migrations; independent offsite encrypted backup + CLI recovery; production CI/manual deployment and security gates.

### Optional Should (release certification)

Media library independently enabled, secure LocalFs public/private media; structured CMS with immutable revision and published pages/navigation (requires Media); Operations UI and durable Redis/BullMQ jobs (requires background jobs capability). Disabled modules must not expose route/permission/nav and must not prevent Core login.

### Could / Won't

Could: S3 implementation, caching webhooks, SaaS extensions, PITR, full visual builder. Won't MVP: dynamic modules, installer, microservices, one-click production restore.

### Navigation

Top-level dashboard groups remain Dashboard / Manage Content / Manage User / Setting **only when nonempty**, based on enabled modules and RBAC. Core-only does not render Manage Content. Media can appear in Manage Content without CMS, if enabled. Backup list may appear under Setting only when Operations active. Audit Logs is Core.

### Acceptance gates

Core-only passes all security/deploy/recovery tests without Redis; Media/CMS/Operations independently certified; initial admin email operator-provided and secret non-echo; no false preview data or untested feature marked shipped.
