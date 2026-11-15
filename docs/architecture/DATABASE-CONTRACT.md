# Database & Migration Contract — v2

**Source compatibility:** Preserve existing `docs/BSD.md` 21 logical tables (4 Better Auth generated + 17 app-owned). All 17 app tables are migrated for every clone, regardless of module flags. Existing columns/FKs/unique constraints in BSD remain unless explicitly superseded below.

## Canonical schemas and deltas

All app `DATETIME(3)` timestamps UTC; app UUID textual `CHAR(36)`; **Better Auth user IDs** must match actual generated SQL type/collation. Use InnoDB, utf8mb4, reviewed FK and indexes. `deleted_at` soft delete is not physical data purge.

| Table | Revision delta | Constraints |
|---|---|---|
| `user_profiles` | `status` add `invited` as default for normal provisioning | Validate enum at Zod + DB CHECK where supported; bootstrap active |
| `permissions` | `delegable BOOLEAN NOT NULL DEFAULT FALSE`, `sensitive BOOLEAN NOT NULL DEFAULT FALSE` | Registry-owned; unique code; check for enabled module at runtime |
| `cms_page_revisions` | `save_key VARCHAR(128) NULL`, `request_hash CHAR(64) NULL` | UNIQUE(`page_id`,`save_key`), NULL for legacy saves, `(page_id,revision_no)` unique |
| `media_assets` | `status VARCHAR(16) NOT NULL DEFAULT 'pending'`, `visibility VARCHAR(16) NOT NULL DEFAULT 'private'`, `ready_at DATETIME(3) NULL` | `status` pending/ready/failed/deleted; `visibility` private/public; UQ storage disk/key retained |
| `system_jobs` | `dispatch_state VARCHAR(16)`, `payload_json JSON`, `idempotency_key VARCHAR(150) NULL`, `dispatch_attempts INT UNSIGNED DEFAULT 0`, `next_dispatch_at DATETIME(3)`, `dispatch_lease_until DATETIME(3) NULL`, `dispatch_lease_owner VARCHAR(128) NULL`, `request_id VARCHAR(100) NULL` | UQ `queue_job_id`; UQ(`job_type`,`idempotency_key`) if globally scoped key by job type; index(dispatch_state,next_dispatch_at), lease expiry |
| `database_backups` | `backup_snapshot_id VARCHAR(128) NULL`, `verified_restore_at DATETIME(3) NULL`, `offsite_verified_at DATETIME(3) NULL`, `verification_error_code VARCHAR(100) NULL` | Verified archive != tested restore, separate statuses |
| `audit_logs` | `actor_type VARCHAR(16)` and `reason_code VARCHAR(100) NULL` | historical rows backfill default `user/system` only when defensible |
| `theme_configs` | Immutable snapshot contract (no mutating tokens); optional `source_theme_id CHAR(36) NULL` FK | Existing `preset_key` UQ remains; new snapshots get unique `custom-<uuid>` preset_key. `is_system` protected |

No new table required for outbox: `system_jobs` is the durable intent table. Idempotency key uniqueness is scoped by job_type; if one job_type can be requested by multiple tenants/projects sharing a DB (not current design), extend scope accordingly. `payload_json` must be validated and contain references, **never secrets**.

### Example SQL migrations (illustrative; generate via Drizzle, review generated output)

```sql
ALTER TABLE permissions
  ADD COLUMN delegable BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN sensitive BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE cms_page_revisions
  ADD COLUMN save_key VARCHAR(128) NULL,
  ADD COLUMN request_hash CHAR(64) NULL,
  ADD UNIQUE KEY uq_cms_page_save (page_id, save_key);

ALTER TABLE media_assets
  ADD COLUMN status VARCHAR(16) NOT NULL DEFAULT 'pending',
  ADD COLUMN visibility VARCHAR(16) NOT NULL DEFAULT 'private',
  ADD COLUMN ready_at DATETIME(3) NULL;

ALTER TABLE system_jobs
  ADD COLUMN dispatch_state VARCHAR(16) NOT NULL DEFAULT 'pending',
  ADD COLUMN payload_json JSON NULL,
  ADD COLUMN idempotency_key VARCHAR(150) NULL,
  ADD COLUMN dispatch_attempts INT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN next_dispatch_at DATETIME(3) NULL,
  ADD COLUMN dispatch_lease_until DATETIME(3) NULL,
  ADD COLUMN dispatch_lease_owner VARCHAR(128) NULL,
  ADD COLUMN request_id VARCHAR(100) NULL,
  ADD UNIQUE KEY uq_job_type_idempotency (job_type, idempotency_key),
  ADD INDEX ix_job_dispatch (dispatch_state, next_dispatch_at);

ALTER TABLE database_backups
  ADD COLUMN backup_snapshot_id VARCHAR(128) NULL,
  ADD COLUMN verified_restore_at DATETIME(3) NULL,
  ADD COLUMN offsite_verified_at DATETIME(3) NULL,
  ADD COLUMN verification_error_code VARCHAR(100) NULL;
```

These snippets illustrate columns, **not executable production migration**: for existing rows, plan safe backfill (especially legacy media assets must be `ready`, and legacy jobs require state mapping) before enforcing NOT NULL / CHECK constraints. On fresh database use final create-table DDL. Revisions may have a cyclic FK (`cms_pages.published_revision_id` → `cms_page_revisions`): generate ordering carefully and test same-page composite FK in MySQL.

### Invariants

- Published pointer must reference revision of **same page**. Enforce with composite FK `(page_id,published_revision_id)` → unique `(page_id,id)` plus service validation, or documented tested equivalent.
- Immutable CMS revisions, immutable final media files, immutable theme snapshot tokens.
- Media deleted only when no refs in any retained revision/settings. Ref insert + delete interlock under compatible locking.
- `roles.version`, `app_settings.version`, `authorization_version` increment in transactions.
- `role_permissions` revoked on module-disable, audited; no auto-regrant.
- No production `drizzle-kit push`, no silent destructive reset.

## Migration lifecycle

1. Pin Better Auth/Drizzle versions, generate vendor auth schema, review SQL diff against baseline.
2. CI `generate` diff check + migration consistency; isolated MySQL 8.4 apply **from empty DB** and **from previous tested release**.
3. Production preflight: selected commit, schema version, successful offsite backup, free disk, exclusive migration lock, compatibility and operator approval.
4. Run checked migrations **once** with dedicated DDL account; never share DDL with regular API account.
5. Permissions sync `--check`, then audited `--apply` with operator approval for destructive grant revocation.
6. Start API/Web and check readiness, RBAC, settings, disabled routes.
7. Failure: do not blindly rollback MySQL DDL (implicit commits); inspect schema, use expand/contract or independent recovery.

## Seed strategy

`db:seed` idempotent, creates system roles + Salt & Pepper + Core registries; optional CMS nav/media demo seed only if enabled, no test/mock data on production. `setup:admin` email supplied interactively or secure env, secret non-echo, never resets existing credential, last-holder invariants. Do not hardcode `admin@codelight.id`.

## Open questions requiring migration-level test

Exact Better Auth generated `user.id` SQL spec; DB CHECK support/test for status; `system_jobs` existing nullable-to-not-null backfill; correct enum values in old `audit_logs`; FK identifier/collation consistency; concurrency under chosen InnoDB isolation.
