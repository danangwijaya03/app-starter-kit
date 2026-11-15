# RBAC — single application permission engine (ADR-003/004/002)

Research candidates: [Blur Stack](https://github.com/blurridge/blur-stack), [Celestia Starter](https://github.com/dev-celestia/celestia-starter), [Better Auth Admin Plugin](https://www.better-auth.com/docs/plugins/admin) **for comparison only**.

**Core required.** Better Auth authenticates users; the application RBAC service decides business authorization.

## Canonical rules

- MySQL tables `roles`, `permissions`, `user_roles`, `role_permissions` (central migrations) with typed immutable permission codes in source.
- Deny by default. Effective permission = valid session + active account + known permission + enabled owning module + active permission definition + active role grant. Multiple roles use union; protected super admin exception applies **only after** status, module and permission-existence checks.
- Permission catalog metadata: `code`, `module`, `label`, `delegable`, `sensitive`; server-synced, not freely editable.
- Admin can only delegate permissions tagged `delegable`, within permissions they legitimately possess. `roles.permissions.update`, `users.roles.assign`, recovery/restore and other privileged scopes are protected from normal delegation. Prevent self-escalation, role-based escalation by proxy, and modification of protected roles.
- Mutations of permissions/roles/status and related audit records commit in the **same MySQL transaction**. Protect last-active-super-admin with deterministic locking and concurrent tests.
- Disabled modules: unmount API, 404 Next admin pages, hide nav, remove effective permissions, revoke module grants during controlled sync with audit. Re-enable must not resurrect previous grants.

## Exclude

Second RBAC store in auth plugin; multi-tenant organization grants; PostgreSQL SQL; authorization based on frontend menu or client-side cached permissions alone.

## Tests

`401/403` for direct API; protected code cannot be delegated; attempted self/proxy escalation denied; duplicate grants idempotent; role changes effective on next request; simultaneous disable/demotion cannot remove final super admin; disabled CMS/Media permissions ineffective and not resurrected on re-enable; failed audit insert rolls back security mutation. Use real disposable MySQL for locks.

See [AUTH.md](AUTH.md), [SECURITY.md](SECURITY.md), [TESTING.md](TESTING.md).
