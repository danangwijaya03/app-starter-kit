# Testing references — Core-first and module certification (ADR-016)

References: [Vitest](https://vitest.dev/), [Playwright](https://playwright.dev/), [OWASP ASVS](https://github.com/OWASP/ASVS), [MySQL 8.4 reference](https://dev.mysql.com/doc/refman/8.4/en/).

The test strategy is **risk-based**, not coverage-percentage-based. The current repo may not yet contain runnable monorepo/test scripts; do not report planned tests as passed.

## Test layers

| Layer | Required evidence |
|---|---|
| Static | Strict TypeScript, lint, import boundaries, module config graph, migrations, build |
| Unit | Zod DTO/policy, themes, block registry, slug/collision, idempotency |
| Integration | **Real disposable MySQL 8.4** for foreign keys, transactions, locking, Auth/RBAC, API; Redis only for jobs tests |
| Browser | Playwright login, permission denial, logout, admin flows, optional module UX |
| Infrastructure | Core deploy without Redis, independent offsite backup/isolated restore, manual rollback preflight |

## Core mandatory gate

Login/logout/password lifecycle and revoked/inactive accounts; unauthorized `401`, insufficient grant `403`, disabled module `404`; protected permission delegation/last-super-admin concurrency; full fresh DB migration and seeded permission sync; private no-store and cross-user session/cache isolation; transactional audit fail-closed; theme fallback without Media; health and external uptime; approved CI commit, TLS/secrets review, offsite backup restore evidence.

## Module certification

- **Media:** Core + invalid MIME, oversize, path traversal, public/private delivery, temp crash recovery, referenced asset delete.
- **CMS:** Core + Media + immutable snapshots, stale save `409`, block-version compatibility, media retention, draft/public/preview separation and SSR.
- **Jobs:** Core + MySQL dispatcher + Redis outage, lost ACK, duplicate and retry safety, lease recovery and worker disabled path.
- **Operations:** Core + Jobs + safe backup orchestration / visibility; production restore remains independent CLI.

Required CI checks must fail when a mandatory suite was silently skipped. For a changed optional module, run affected module + dependency suites. All activated modules must pass certification before release. Maintain real exit codes, test fixtures, commit SHA and independent signoff for high-risk features.

## Reviewer constraint

Independent qualified reviewer inspects diff, assertions, run logs and security invariants for sensitive auth/RBAC/file/restore/security tasks. Implementer's own review does not satisfy independence.
