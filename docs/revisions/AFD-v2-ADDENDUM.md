# AFD v2 Addendum — User/Operator flows (supersedes conflicting AFD-01, 06, 07, 09, 10)

### Core-only navigation

Anonymous visitor may see static landing page; no public CMS catchall if CMS disabled. Login and admin dashboard/usermanagement/settings/audit available based on permission. Disabled module page route returns server-side 404 even if user enters URL. User preference and appearance use semantic tokens with current snapshot pointer. Default logo/favicon static when Media disabled.

### Auth and role assignment

Invite → inactive invited account → single-use activation → active with first-login password policy. Admin changing roles checks `delegable`, actor ownership of delegated permission, target protection, self-elevation and last-Super-Admin guard under DB lock. Revocation visible next protected API request.

### CMS save/publish

Editor opens latest revision → Save sends saveKey+expectedRevisionNo → server idempotency check → new immutable revision or 409 → Preview requires signed session/revision → Publish sets pointer+slug atomically after validating public media and block compatibility → public SSR sees latest published version on next request, no persistent cache invalidation. Old slug 404 MVP. History restore creates a new draft.

### Media upload/delete

Admin selects file → Hono validates bytes, dimensions, MIME, RBAC → temporary LocalFs and DB pending → durable finalization → ready. Public only ready+public. Private only permission-scoped. Referenced retained revisions/settings prevent physical deletion; reconciliation handles crash.

### Backup / disaster recovery

Production backup runs on independent Linux timer to encrypted offsite repository; Operations dashboard optional for scheduling/view/verify. Production restore is NOT a dashboard API. Operator runs independent CLI to staging DB/storage, verifies integrity, approves maintenance+cutover. No automatic Redis replay or restore retry.

### Errors

401 missing session, 403 insufficient permission, 404 disabled module, 409 concurrent update, 422 malformed input; display actionable error/refresh, do not leak sensitive detail.
