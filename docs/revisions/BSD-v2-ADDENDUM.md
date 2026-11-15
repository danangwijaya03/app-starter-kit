## BSD v2 Addendum — Schema and API deltas (supersedes conflicting clauses of BSD-03..07)

Retain existing **21 logical tables**, all FKs and detailed existing columns unless the linked [DATABASE-CONTRACT](../architecture/DATABASE-CONTRACT.md) explicitly changes them. Add:
- `user_profiles.status` permits `invited` default for normal created user; bootstrap admin active.
- `permissions.delegable` and `permissions.sensitive`, both BOOLEAN NOT NULL DEFAULT FALSE, registry-owned.
- `media_assets.status` pending/ready/failed/deleted, `visibility` private/public, `ready_at`. Historical data migration must backfill ready where verified.
- `cms_page_revisions.save_key`, `request_hash`, UNIQUE(page_id,save_key); maintain unique page/revision number and same-page published composite FK.
- `system_jobs.dispatch_state`, payload, idempotency/attempt/lease/next-dispatch fields with indexes and deterministic queue job ID.
- `database_backups.backup_snapshot_id`, offsite_verified_at, verified_restore_at, verification_error_code.
- Audit actor type/reason code if chosen in actual reviewed migration; old audit rows preserved.
- Theme configs immutable; each custom snapshot receives unique preset key; active theme pointer in app_settings versioned.

**Permission registry:** replace `cms.media.view/upload/update/delete` with `media.view/upload/update/delete` in future permissions and API routes. Perform one-time audited migration of existing grants if any; aliases are not a second active permission source. Reclassify `backups.restore` as **CLI-only privilege/approval**, not an exposed business API endpoint.

**API changes:** keep original `/api/v1/*` business URLs except add public/private media file endpoints. Delete production `POST /backups/:id/restore` from supported API. Health canonical `/api/health/live`, `/api/health/ready`, `/api/health/subsystems`. All public CMS SSR requests read published revision only and bypass persistent cache.

**Database migration:** fresh installs have all schemas; existing installs require nullable/backfill/index/constraint-safe sequences. Generator must be pinned and reviewed; no untested SQL snippet applied directly to production.
