# Library and Upstream Contract Verification

Review date 2026-11-14. **Do not interpret this list as a verified installed dependency list.** `package-lock.json` after P01 is the exact source of installed versions. Install and lock actual versions only during corresponding implementation tasks; test before release.

| Library / service | Planned responsibility | Authoritative documentation |
|---|---|---|
| Next.js 16 App Router | SSR, Cache Components defaults and server/client rendering | https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents |
| Hono | Node HTTP API, middleware | https://hono.dev/docs/getting-started/nodejs |
| Hono Zod OpenAPI | Business DTO/OpenAPI routes | https://hono.dev/examples/zod-openapi |
| Better Auth | Session, credential and generator | https://www.better-auth.com/docs/adapters/drizzle |
| Drizzle ORM | Single migration journal | https://orm.drizzle.team/docs/drizzle-kit-migrate |
| MySQL 8.4 | FK, transaction, SKIP LOCKED, dump semantics | https://dev.mysql.com/doc/refman/8.4/en/ |
| BullMQ | Background queue/retry/at-least-once | https://docs.bullmq.io/ |
| Redis | Private queue state, persistence | https://redis.io/docs/latest/ |
| restic | Encrypted offsite backup/recovery | https://restic.readthedocs.io/en/stable/ |
| Pino | JSON structured logs/redaction | https://getpino.io/ |
| Sharp | Safe image decode/limitInputPixels | https://sharp.pixelplumbing.com/ |
| Tiptap | Structured rich text JSON | https://tiptap.dev/docs |
| Vitest / Playwright | Unit/integration/browser tests | https://vitest.dev/ and https://playwright.dev/docs/intro |

**Pinning workflow**: evaluate current stable version, review release/major compatibility with Node and TS baseline, write exact package-lock version, run fresh/upgrade DB integration tests and negative auth tests, then record accepted version in dependency decision log. Never run `npx auth@latest generate` unreviewed for committed schema; use matching pinned CLI/package versions.

**Security checkpoints**: inspect CVEs before deployment, license compatibility for reused UI/source reference code, and generated vendor auth tables after any Better Auth major/minor upgrade. The current GitHub repository states Next.js 16.4.3 and React 19.3 preview, but these do not prove other planned libraries are installed.
