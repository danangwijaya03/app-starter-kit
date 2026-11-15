# Testing Strategy, Quality Gates & Release Criteria — v2

## Risk-based test layering

- Static: strict TS, ESLint import boundaries, dependency-cycle detection, SQL migrations generated and reviewed, source lint/build.
- Unit: Vitest for Zod schemas, policies, module graph, block registry, themes, slug canonicalization, idempotency hashes.
- Integration: Vitest + isolated **real MySQL 8.4** for RBAC concurrency, transaction/audit, Drizzle FK/unique constraints, CMS save/publish, job dispatcher. Redis used only in jobs integration.
- E2E: Playwright for login/first password change, role editor, no access, module missing, media upload, CMS draft/publish, appearance, logout/session switch.
- Recovery/deploy: disposable VPS-like environment, fresh MySQL DB and offsite snapshot restore drill.
- Independent review for high-risk auth/RBAC/restore/security features before production acceptance.

## Mandatory Core gate

- Typecheck/lint/build passed for Web+API; no worker/Redis required or connected.
- Fresh database migrations and upgrades from previous release pass; DB seed idempotent and bootstrap safe.
- Signup blocked; login/reset/session tests pass; account status and forced password guard enforced.
- Negative tests: 401, 403, self escalation, nondelegable permissions, concurrent last-active-superadmin.
- Admin response no-store, SSR cross-account isolation; changing permission reflected next request; disabled routes return 404.
- Settings + theme fallback, contrast, transactional audit fail-closed, external uptime check.
- Production manual deploy, TLS, secrets separation, independent encrypted offsite backup verified plus measured isolated restore test.
- Approved CI run + approved commit SHA + operator signoff, P0/P1 security defects closed.

## Module certification matrix

| Feature config | Required suites |
|---|---|
| Core only | Core all, disabled Media/CMS/Operations routes |
| Media | Core + Media validation/lifecycle/security |
| CMS | Core + Media + CMS blocks/revisions/preview/public SSR |
| Operations | Core + Durable Jobs/Redis outage + backup UI tests |
| CMS + Operations | all required dependencies and combinations |

Do not treat a skipped CI job as test success. `release-gate` final job must prove the exact required jobs were actually executed for the selected module config.

## CI and evidence

PR: `npm ci`, lint, typecheck, unit, build, import boundary checks; integration with isolated MySQL after API foundation. Release: full active module suites, E2E, backup/recovery rehearsal current, npm lock/version/SQL diff/permission sync checks. Playwright trace on first retry, failing/flaky tests investigated, never muted to green. Suggested targets for service packages: 80% line, 70% branch; **negative security tests trump coverage percent**.

Each task evidence: changed files, executed command + exit code, test output, source commit hash, environment, reference license/version, reviewer approval when high-risk. Preserve existing 156 task IDs and status unless verified work is genuinely completed. Archived original task card remains traceable after splits.

## Measurable postproduction outcomes

- Availability measured externally; target agreed per deployment.
- 95th percentile API request time measured after production traffic exists (no invented baseline).
- Backup freshness and quarterly recovery RPO/RTO measurements.
- Media orphan count and cleanup reconciliation.
- Dispatch pending age and duplicate side effect count = 0 on tested retry matrix.
- Audit failure alerts; secrets leak incidents = 0 in log sample audits.
- Pre-release defects closed with evidence; module versions and config hash recorded.
