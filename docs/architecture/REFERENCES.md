# Architecture and feature references

The canonical **reference-driven** catalog is [Reference Map](../references/REFERENCE-MAP.md), with per-feature notes and [Adoption Protocol](../references/ADOPTION-PROTOCOL.md).

- [Celestia Starter](https://github.com/dev-celestia/celestia-starter): Hono/Next separation, Better Auth, CMS; adapt architectural patterns only, not pnpm/PostgreSQL or feature installer.
- [Blur Stack](https://github.com/blurridge/blur-stack): RBAC and route-permission architecture; exclude multi-tenant/PostgreSQL requirements.
- [Hono Starter](https://github.com/Joker666/hono-starter): Hono/MySQL/BullMQ; exclude JWT-based auth and Docker dependency.
- [Better Auth](https://better-auth.com/docs), [Drizzle](https://orm.drizzle.team/docs/overview), [Hono](https://hono.dev/docs), [OWASP ASVS](https://asvs.owasp.org/): authoritative upstream references for their own responsibilities.

No external source copied by this documentation commit.
