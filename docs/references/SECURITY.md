# Security — Core API / modules / operations (ADR-003/004/006/010/013/015)

Authoritative references: [OWASP ASVS](https://github.com/OWASP/ASVS), [Hono CSRF](https://hono.dev/docs/middleware/builtin/csrf), [secure headers](https://hono.dev/docs/middleware/builtin/secure-headers), [Better Auth](https://www.better-auth.com/docs/).

## Security invariants

- Server validates Better Auth session, account status, active module, permission, resource scope and Zod input. Direct `/api/v1/*` browser requests are same-origin via Nginx; no frontend-only checks.
- Apply origin/CSRF protections on relevant unsafe cookie-auth requests, including auth/plugin routes; do not rely on CORS or SameSite alone. Trust forwarded headers **only** from declared proxy hops.
- Auth and private admin data never persist in Next.js caches; browser/API request `no-store` on private responses. Selectively forward only required auth cookies for server-to-Hono calls.
- Rate-limit auth/credential endpoints, bound request bodies and image decode resources, avoid raw paths, and redact secrets/token/cookie/body from logs and error responses.
- Separate runtime, migration and backup DB accounts; never allow app runtime DDL or unrestricted audit mutation. Secrets server-only and outside Git/client bundle.
- Privileged RBAC modifications require limited delegation rules, transactional audit and last-super-admin concurrency locking.
- Disabled modules have no routes/permissions; Centralized Migration never means disabled modules are accessible.
- Production restore only via independent operator CLI, using isolated validation/cutover; offsite encrypted backup with recoverability tests.

## Threat-model required tests

`401/403/404` boundaries, direct-API bypass attempts, CSRF/origin violation, revoked/inactive account, delegated escalation, last-super-admin race, cookie forwarding and cross-user SSR isolation, sensitive-log redaction, path traversal/symlink and MIME spoof, oversized upload, stale/replayed job, invalid migration environment, safe isolated recovery.

Review independently for auth, RBAC, media, restore and deployment changes. **Passing lint or a visual demo does not count as security evidence.**
