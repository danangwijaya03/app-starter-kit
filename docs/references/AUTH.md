# Auth — Better Auth identity and session owner (ADR-003)

References: [Better Auth docs](https://www.better-auth.com/docs/), [Drizzle adapter](https://www.better-auth.com/docs/adapters/drizzle), [session docs](https://www.better-auth.com/docs/concepts/session), [Celestia Starter](https://github.com/dev-celestia/celestia-starter) for patterns only.

**Core required**; available even when Media, CMS, Operations and Redis are disabled.

## Adopt

- Better Auth exclusively owns credential hashing, login/logout, password reset, session storage and authentication route `/api/auth/*` in Hono.
- Generate auth tables from the **exact pinned installed Better Auth version**; use centralized Drizzle migration history. Do not replicate passwords or create a parallel identity store.
- Disable public signup by default, implement secure invitation-first provisioning with `invited → active`; distinguish `inactive` and `suspended`. No privileged API access before activation.
- Force first password change, protect reset tokens, revoke sessions on account disable/password reset and check account status on **every** private API request.
- Browser uses same-origin HTTP-only secure cookies; Next.js server client selectively forwards only required auth cookies to internal Hono API with `no-store`; never store bearer tokens in localStorage.
- First-admin command accepts approved email via secure operator input/env, without hardcoded address or default password; keep bootstrap idempotent and protect last active super admin.

## Explicit exclusions

- No JWT ownership imported from Hono Starter; no second session provider or independent Better Auth Admin Plugin RBAC. If a Better Auth plugin is used, formally bridge its administrative endpoints to the application permission service and test privileges.
- No credentials/secrets in code, test screenshots, logs or source attribution.
- Do not treat a cookie's presence or a Next.js route guard as authorization.

## Mandatory tests

Anonymous `401`; insufficient permission `403`; revoked session denied next request; invited/inactive/suspended denied; reset token single-use and expiry; session fixation/CSRF/origin checks; account status and password change across all relevant auth endpoints; first admin bootstrap without hardcoded credentials. Review generated schema and compatibility on upgrades.

**Ownership:** Hono auth integration + server-only application auth service; separate from business RBAC. See [RBAC.md](RBAC.md), [SECURITY.md](SECURITY.md).
