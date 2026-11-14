# Auth — Better Auth is the authoritative identity/session engine

Primary: https://better-auth.com/docs and https://better-auth.com/docs/plugins/admin ; comparative: https://github.com/dev-celestia/celestia-starter .

**Adopt:** version-pinned Better Auth MySQL/Drizzle adapter generated schema, session/login/logout/password-reset lifecycle, first-login password change and secure admin lifecycle. Better Auth Admin Plugin only where its authorization semantics are verified against our roles.

**Do not copy:** custom JWT auth from Hono Starter, another starter's OAuth secrets, a duplicated user/password table or PostgreSQL schema. Public signup disabled by default. No credential in repo/log/test evidence. Never hardcode a default administrator password; secure non-echo prompt/private local input, idempotent first-admin command through npm script after migration/seed.

**Contracts:** BSD auth generation, AFD login/first-use, P04/P05; one canonical API/session owner. 401 without valid session; 403 with insufficient permission. Session revocation, ban/deactivate, reset single-use expiration and first-password-change tested.

**selected coding agent microtasks:** (1) pinned auth adapter/schema; (2) session guard; (3) login/logout; (4) reset; (5) admin bootstrap/test. **Independent review** required before high-risk technical completion.
