# Backup, Recovery, Deployment & Security — v2

## Deployment topology

One VPS; aaPanel configures TLS/Nginx; Node processes under nonroot PM2:
- Web `127.0.0.1:3000`, fork mode, one instance.
- API `127.0.0.1:4000`, fork mode, one instance.
- Worker one forked instance **only when jobsRequired=true**.
- MySQL 8.4 private; Redis private and optional. Local media directory and backup working directory **outside webroot**.

Do **not** promise zero downtime with PM2 fork restart. Nginx routes exact `/api/*` (including Better Auth) to API; others to Web. `proxy_pass http://127.0.0.1:4000;` without trailing path replacement. Configure forwarded Host/Proto/IP only with trusted reverse-proxy chain, firewall, TLS, secure cookies, body size limits, validated CSP/rate limits.

### Proposed manual deployment checklist

1. Approved commit SHA from CI; verify release config/module hash, planned migration and active module test suite.
2. Offsite encrypted backup recent and verified; confirm no production secrets in repo/client bundle.
3. `npm ci` pinned lockfile and version. Build in controlled path without making secrets accessible to untrusted build scripts.
4. Check `db:migrate:check` and schema compatibility; apply reviewed Drizzle SQL via separate migration DB identity and exclusive migration lock.
5. `permissions:sync --check`, review destructive revocations; `--apply` with approved audit; idempotent seed; never reset existing Super Admin credentials.
6. Restart API and Web under PM2; conditionally start/stop worker per module config. Handle shutdown timeouts/retries for jobs.
7. Test health ready/live, `/api/auth` login, permission deny, disabled routes, public SSR and backup freshness.
8. Record commit, migration journal marker, config hash, CI run, operator and timestamps.
9. If failure, roll back **application code only when database schema is backward compatible**; otherwise use forward fix or independent recovery process.

CI quality gate must run on PR, and production release is manually approved. GitHub Actions needs read-minimal permissions, pinned third-party Actions and no production secrets on untrusted pull requests.

## Independent backups

Always required for real production data, regardless of Operations module or Redis:
- MySQL `mysqldump --single-transaction` for InnoDB, validated version/privileges.
- Local media files immutable after `ready`. Pause physical GC, generate manifest of referenced files for the database snapshot, copy selected files while GC blocked, checksum verify.
- `restic` encrypted repository to **offsite** destination, keys/password stored separately from VPS, scoped credentials. Maintain independent offsite catalog; MySQL `database_backups` not required to recover metadata.
- systemd timer or cron with monitored exit status and last-success age.
- Suggested retention: 7 daily, 4 weekly, 3 monthly; review cost/retention regulation and offsite deletion privileges. Ransomware resilience requires append-only/immutable offsite credentials separated from production where supported.
- Initial RPO 24h and RTO 8h are **proposals**, only accepted once tested in drills. Smaller RPO may require binlog/PITR.

### Backup pseudoflow

```text
acquire backup/GC coordination lock
mysqldump consistent snapshot to restricted tmp
validate dump exits successfully
parse catalog of referenced immutable media from dump DB snapshot
copy media & verify sizes/checksums (GC lock still held)
build manifest: commit, schema, IDs, counts, SHA-256, coverage
restic backup dump + selected media + manifest
verify encrypted repository snapshot and offsite availability
release lock and securely clean temp
```

Protect backup from secrets exposure: snapshots contain sensitive user/auth data; all restoration access is privileged. Do not assume `restic check` is a full restore test.

## Recovery CLI (independent from app)

Production restore **never exposed as one-click dashboard API and never BullMQ auto-retried**.

1. Operator obtains approved snapshot, schema/app commit, offsite access and recovery secrets on a clean isolated host.
2. Use `restic restore` into separate restricted directory. Verify manifest hashes, backup contents and expected schema version.
3. Initialize **fresh recovery MySQL DB** and **separate media tree**; import DB, run integrity checks, check published revision FK, media references, auth login smoke, schema compatibility with selected app commit. Disable outbound email/webhooks and worker on staging.
4. Reconcile recovered `system_jobs` (do not auto-replay old jobs), revoke all sessions and rotate exposed credentials as incident warrants.
5. If old production available, take final recovery point. Enter maintenance; operator approves cutover after integrity and smoke tests.
6. Switch DB/media configuration deliberately, start API/Web, run post-cutover smoke test, then worker only after job review; write durable recovery journal outside the restored DB.
7. If validation fails, do **not** overwrite production; keep staging isolated and investigate. Operator-controlled rollback to pre-cutover environment only when safe.
8. Quarterly recovery drill; measure actual elapsed recovery time and data loss.

No application process, MySQL production, or Redis must be required merely to *start* the recovery CLI.

## Observability

- Pino JSON logs (redacted cookie/token/password/body); request ID propagated Web ↔ Hono ↔ job, user IDs only where necessary and permitted.
- PM2 stdout/stderr rotation, initial 14 days with disk quotas.
- Transactional `audit_logs` for successful business changes; audit read-only API; record denied attempts separately with controls.
- Hono `/api/health/live`: process only. `/api/health/ready`: essential DB/schema dependencies. `/api/health/subsystems`: protected optional jobs/backup freshness.
- Uptime monitor **outside VPS**, including Nginx/TLS; alert 3 failed minute checks. Alerts: backup >30h old, disk >85%, readiness down >2min, worker heartbeat >2min if enabled, job oldest pending >10min if enabled. Thresholds initial only.

## Security separation

Dedicated runtime account (no DDL), migration account (DDL only needed scope), backup account (read-only dump), separate external backup credentials. Avoid storing production secrets in CI PR jobs or app settings. Firewall expose only 80/443 and restricted SSH. MySQL/Redis bind private. Add access logging retention/risk review and vulnerability update cadence.
