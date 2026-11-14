# Operations — manual clone, PM2, backup, observability

Sources: https://github.com/Joker666/hono-starter (MySQL/BullMQ); https://github.com/pinojs/pino (JSON logs); https://github.com/getsentry/sentry-javascript (optional error SDK); https://github.com/novuhq/novu (optional notification patterns, open-core licensing).

**No installer** (no `apps/installer`, project generator, release archive manager, versioned-symlink rollout tool). Clone template into a new Git repository/project, use separate production env/DB/storage/Redis namespace; follow [Manual Clone Setup](../MANUAL-CLONE-SETUP.md) and [Server Guide](../../README-SERVER.md).

**Minimum MVP operations:** documented `npm ci`, migration check/apply, seed permissions/roles, manual first-admin secure command, production build, PM2 web/API/worker, aaPanel Nginx, health smoke, backup/restore on isolated test first. **These are manual commands not an installer/wizard.**

**Audit vs logs:** Pino for structured operational logs, DB audit_logs for immutable business event history. Optional Sentry monitoring only if configured, redacted and approved. Notifications/webhooks are optional future modules; do not add full Novu platform as a dependency without a separate decision.

**Production boundary:** review schema change, take recovery backup, stop affected writes/workers if required, deploy code with source-controlled history, restart PM2, run health tests. Git checkout/rollback does **not** roll back DB schema. Never auto-restore or silently mutate live data.
