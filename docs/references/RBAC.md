# RBAC — reference patterns, one application permission engine

Sources: https://github.com/blurridge/blur-stack ; https://github.com/dev-celestia/celestia-starter ; https://better-auth.com/docs/plugins/admin .

**Adopt patterns:** typed permission catalog, permission-to-route map, server-side guards, grouped checkbox matrix, isolated role assignment service, dynamic authorized menu. Match BSD tables `roles`, `permissions`, `user_roles`, `role_permissions` and canonical immutable code registry.

**Reject:** an imported multi-tenant organization grant model, PostgreSQL column/SQL syntax, a second independent RBAC store hidden inside Better Auth. Better Auth handles session/identity, app permission service handles business authorization; adapter/config explicitly bridges any administrative plugin permissions.

**Security tests:** unauthenticated 401; authenticated ungranted 403; stale/disabled role invalidation; self-escalation denied; attempts to remove last active super admin (including race/concurrency) denied atomically; frontend menu hiding never replaces server checks. Review DB transactions/lock order with real MySQL.

**Agent partition:** catalog → seed and sync → middleware → user/role CRUD → preview → negative/race tests. Independent signoff required.
