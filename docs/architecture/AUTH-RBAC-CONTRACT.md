# Auth, RBAC and Audit Security Contract — v2

## Source of truth

Better Auth owns identities, password/reset, session issuance/revocation; Hono application services own `roles`, `permissions`, `user_roles`, `role_permissions`, and security policy. Do not use Better Auth Admin plugin role checks as a second policy. Generate auth schema from pinned Better Auth adapter/version and migrate through Drizzle.

`status ∈ {invited, active, inactive, suspended}` with default `invited` for newly provisioned non-bootstrap users; `must_change_password` can restrict a newly activated or bootstrap account. `active` status is necessary but not sufficient: valid session, forced-password-state, enabled module, active permission and grants must all pass. Invitation token is single-use, expiring; provisioning is administrative and should not generate shareable passwords. If outbound email isn't configured, use a protected manual invitation/activation path, never publicly searchable enrollment.

**Auth API:** `/api/auth/*` uses Better Auth native format. Auth route lifecycle/hook logic must enforce account status on sign-in and account-changing endpoints; business middleware alone is insufficient. Public sign-up disabled. Mutation endpoints enforce CSRF/Origin according to browser session model. Sensitive operation: require recent reauth (define freshness default, e.g., <=5min) and audit.

## Authorization algorithm

```text
allow(user, action):
  require valid Better Auth session
  require user_profiles.status == active
  if must_change_password: allow only password-change/logout
  require action in canonical registry AND registry[action].isActive
  if permission.module optional AND !enabledModules[module]: deny
  if active protected super_admin membership: allow (except recovery CLI scope)
  else: allow if exists active user_role + role_permission for action
```

Cache session/permission? No persistent permission cache on MVP. Each protected API resolves from DB. Revocation must take effect on next request. UI hides denied actions but never authorizes.

### Limited delegation invariants

- `roles.permissions.update` and `users.roles.assign` are capability to **open** management operation, not authority to grant all privileges.
- Permission metadata `delegable=false` by default, `sensitive=true` for security/restore keys; only explicitly listed operational permissions may be delegated by ordinary admins.
- Non-super-admin may only grant permission `p` if `p.delegable=true`, actor currently possesses `p`, and target role has no protected permissions; cannot edit `is_system` roles, protected system roles, or self-assignment that raises effective privilege.
- **Additional invariant:** non-super-admin may not reassign a role whose effective grants include nondelegable/sensitive permissions, even if such a role already existed. Role updates cannot change `delegable`, `sensitive`, `is_active`; registry sync only.
- Only active Super Admin may assign/change protected roles and permissions, after recent re-authentication. `super_admin` implicit authorization is separate from ordinary grant list.
- All role assignment and account status mutations serialise against the same `roles` super_admin row (`SELECT ... FOR UPDATE`) before last-holder count; lock order must be identical across both endpoints. Prevent concurrent removal/suspension/deactivation of final active holder.
- Audit role/grant/status and increment affected `authorization_version` in **same DB transaction**. If audit insert fails, mutation must fail.

## Error and session behavior

| Condition | API | Web |
|---|---|---|
| No valid session | 401 | redirect login |
| Valid session but forbidden | 403 | access denied |
| Disabled module route | 404 | notFound |
| Invalid payload | 422 (or documented Zod-consistent 400) | field errors |
| Stale version / conflicting draft | 409 | refresh conflict UI |
| Forced password change | stable error/redirect for other routes | restricted change password page |

Cookie cache disabled for MVP unless revocation correctness independently verified. Password reset must revoke existing sessions. Status changes revoke sessions; when DB and auth session revocation cross transaction boundaries, request-level status guard is safety net and retry revocation until verified.

## Audit contract

`audit_logs` remains app table. Proposed delta: `actor_type VARCHAR(16)` (`user/system/operator/anonymous`), `reason_code VARCHAR(100) NULL`. On business mutation success, audit insert uses the same MySQL transaction. On failed login/permission denials, use minimum necessary security events outside business transaction, rate limit and redact. No audit edit/delete API. Runtime DB grants do not include update/delete on audit rows where feasible; this does not protect against a DB root or DBA, so offsite append-only export is a future hardening option.

## Required negative tests

1. Direct API denied without session and without grant.
2. Inactive/suspended/invited cannot access auth business session even if old cookie exists.
3. Admin with `roles.permissions.update` cannot grant it to other users or create self-escalation path.
4. Concurrent role removal and status deactivation never remove last active Super Admin.
5. Disabled module permission is ineffective even before grant clean-up; not auto-restored upon re-enabling.
6. Permission update invalidates next-request authorization; no cross-user leak in SSR.
7. Failed audit insert rolls back security mutation.
