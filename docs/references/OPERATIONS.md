# Operations — independent recovery, manual deployment and light observability

References: [PM2 docs](https://pm2.keymetrics.io/docs/usage/quick-start/), [Nginx docs](https://nginx.org/en/docs/), [Pino](https://getpino.io/), [restic](https://restic.readthedocs.io/en/stable/), [BullMQ](https://docs.bullmq.io/) for optional jobs, [Sentry](https://docs.sentry.io/platforms/javascript/) optional only.

## Deployment baseline (ADR-014)

- Manual clone; npm workspaces and one lockfile, no installer/Docker requirement.
- GitHub Actions CI runs lint, types, unit/integration, migration checks, security tests, build and applicable module suites. Operator deploys exact **approved commit SHA** after preflight, not unreviewed branch head.
- aaPanel/Nginx terminates TLS and routes `/api/* → Hono` and `/ → Next.js` on same origin; Web and API bind localhost. PM2 Web and API always run; worker only for enabled jobs.
- Production secrets are not passed to untrusted CI/build steps. Use non-root runtime and separated MySQL permissions. Review migration diff, backup availability and schema compatibility before deployment; no automatic DB downgrade on rollback.
- Validate health and smoke tests post deploy; PM2 fork does not guarantee zero-downtime reload.

## Backup and disaster recovery (ADR-013)

- **Independent backup scheduler and CLI** are required for production even with Operations module disabled and Redis absent; encrypted **offsite** repository and tested recovery credentials.
- Consistent MySQL dump plus immutable media coverage/manifest; hold media GC while gathering backup data. Verify offsite snapshot and periodically restore on **isolated** MySQL/storage.
- Production restore never executes as one-click web UI or auto-retried BullMQ job. Operator-run CLI validates snapshot, migration/app version, media integrity, smoke tests; approved cutover from isolated environment.
- Operations UI may request/observe backup jobs, verify and show audit; it cannot assume app is alive during a disaster.

## Logging/monitoring (ADR-015)

- Pino redacted JSON operational logs and PM2 rotation. Structured `requestId`/correlation across Web-Hono-worker.
- MySQL audit logs distinct from debug logs; sensitive business write + success audit in the same transaction.
- `/api/health/live` checks process; `/api/health/ready` checks Core dependencies; protected subsystem health reports Redis/worker degraded without failing Core when optional.
- Monitor uptime **outside** the VPS and alert on app downtime, backup age, disk usage, worker heartbeat/queue lag if jobs enabled. Optional Sentry/Novu require separate decisions; do not install full platforms by default.

## Tests

Fresh Core-only deploy with no Redis; approved-commit manifest; misconfigured secrets fail closed; audit redaction; backup from independent scheduler while app unavailable; isolated offsite restore; schema-compatible code rollback; subprocess crash and worker conditional start.
