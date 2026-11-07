# Installer boundaries — reusable starter kit

**Status:** architecture contract, NOT implemented in the current `main` source.

## Three distinct interfaces

1. **Project Initializer** (`init-project`, P16-10 target): initialize a derivative project's identity, unique DB/storage namespace and private secret references; never clone user data, sessions, backups or template credentials. It does **not** deploy a release to a live server.
2. **Application Setup CLI** (`apps/installer`, P01 shell + P05 security/bootstrap + P16 integration): `preflight`, `migrate --check/--apply`, `permissions:sync --apply`, `seed`, `bootstrap-admin`, `verify`. Use a protected private password input for initial admin, enforce idempotence and a single-install lock; never reset existing credentials.
3. **Deployment Manager** (`infra/scripts`, P16): validate archive SHA/manifest/signatures and safe extraction, create versioned release directories, perform upgrade compatibility checks, use controlled symlink switch, health verification and compatible rollback. Preserve shared env/media/backups/logs.

## Installation and upgrade sequencing

For an empty installation, verify archive **and execute CLI directly from the extracted new release path**, e.g. `releases/vX.Y.Z/cli/cli.js`, before expecting a `current` symlink to exist. `current` is switched only after preflight and required installation gates. This resolves the cold-start ambiguity in the draft README-SERVER, whose example uses `current/cli/cli.js`.

Fresh: upload & verify → safe extract to new version → provision isolated `shared` and private env → MySQL/Redis connectivity → reviewed migration → permission sync & seed → one-time admin bootstrap → release switch → PM2/Nginx → health/login checks.

Upgrade: upload/verify → schema compatibility and backup gate → maintain/drain where necessary → approved migrations → switch release → PM2 reload/health; no routine password reset. Rollback code only if schema backward compatible; never auto-retry destructive restore.

**Incremental development:** API, migrations, permission sync and bootstrap are built and tested in their original feature phases; P16 composes those already proven capabilities into a portable artifact. Installer should not duplicate business logic.

**High-reasoning recommendation:** require an independent high-reasoning architecture/security review for new-project isolation, schema migration, production secrets, archive extraction, version cutover and rollback. Low reasoning may build well-specified CLI wrappers and smoke tests; production mutations still need explicit operator authorization.
