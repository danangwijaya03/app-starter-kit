# Reference → ADR → Module → Task → Acceptance Test Matrix

**Use:** this is a *planning traceability map*, not an assertion that code has been imported or tests have passed. Before implementation replace the task placeholder with its **exact existing ID** from `docs/agent/TASKS.yaml`; do not fabricate IDs.

| Reference/capability | ADR | Module | Actual task selection | Primary acceptance tests |
|---|---|---|---|---|
| Better Auth session + Drizzle | 003, 005 | Core | Auth task from active TASKS.yaml | Signup disabled, account statuses, revocation, session isolation |
| Blur Stack RBAC patterns | 003, 004, 002 | Core | RBAC task | Delegate only allowed permissions, concurrency last super admin, disabled grant |
| Hono + Zod/OpenAPI | 006, 007 | Core | API task | Session 401, permission 403, Zod invalid, disabled route 404 |
| Next.js App Router | 007, 008 | Core/CMS | Web/CMS rendering task | Admin no-store, SSR session isolation, CMS published-only |
| shadcn/UI, RHF, Table | 012, 007 | Core | Settings/UI task | Theme fallback, contrast, keyboard, no false writes |
| Celestia Media patterns | 010 | Media | Media task | Access separation, MIME/path, crash recovery, referenced retention |
| Celestia CMS + Tiptap | 011, 008 | CMS (requires Media) | CMS task | Immutable saves, concurrency 409, legacy block, SSR |
| Hono Starter + BullMQ | 009 | Jobs capability | Queue/worker task | MySQL intent, Redis down, replay after ACK failure, no auto restore |
| Pino | 015 | Core | Observability task | Redaction, audit transaction, correlation |
| PM2/Nginx and GitHub Actions | 014 | Production | Deployment task | Approved SHA, localhost binds, smoke and secrets |
| restic + MySQL dump | 013 | Production outside app | Backup/recovery task | Encrypted offsite verified, clean isolated restore |
| Vitest/Playwright/ASVS | 016 | All | Testing/release task | Core-only suite and per-module certification |

## Mandatory evidence template

```markdown
- Task ID and target module:
- ADR IDs and current implementation contract:
- Upstream reference URL / exact commit / source paths:
- License checked and attribution outcome:
- Changes adopted vs deliberately excluded:
- Expected APIs, schema/migration and permissions:
- Tests (positive, negative, concurrency/failure):
- Actual test commands, exit codes, evidence commit:
- Independent security review (if applicable):
- Remaining risks / follow-up:
```

**Compatibility checks:** compare upstream SQL and auth, package manager, Node/Next/React versions, cache semantics, static modules, worker requirements, license. An upstream CLI installer or Docker compose file is not an acceptance requirement for this starter.
