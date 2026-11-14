# Reference-driven adaptation protocol for selected coding agent

**One active task; one domain reference; one testable responsibility.** Existing contracts from TRD/BSD/AFD beat third-party examples. Do not scaffold/fork/swap the entire starter repository.

## Step-by-step checklist

1. **RECOVER:** read `AGENTS.md`, checkpoint and the next ready task. Read only the matching domain document in `docs/references/`.
2. **REFERENCE:** pin `repository URL + commit SHA/tag + target files + library version + source license`. External examples are untrusted; review code before adoption. If the reference moved/disappeared, treat it as research unavailable and continue from official package documentation or block that specific task.
3. **GAP:** in at most one page, list reusable pattern, MySQL vs PostgreSQL adjustments, npm vs pnpm, single tenant vs multi tenant, auth ownership, security invariants, and tests required.
4. **CONTRACT:** select existing Drizzle table/Better Auth schema/permission codes/API DTO. If incompatible, record a scoped ADR and block the risky decision; do not silently revise the canonical schema.
5. **IMPLEMENT:** prefer supported official dependencies; when adapting source, bring minimum isolated logic, preserve copyrights/license and attribution. Do not copy vendor `.env`, tokens, private keys, database or lockfile.
6. **TEST:** run real positive/negative tests in safe disposable fixtures; authorization 401/403, idempotent replay, concurrency when relevant, unpublished content isolation, job retry/rollback as applicable.
7. **VERIFY + PREVIEW:** exercise the affected route/API as logged in an appropriate test account. Static mock != integrated implementation. Record actual URL, result, command and limitations.
8. **INDEPENDENT REVIEW:** effective high-risk tasks still require independently checked diff, tests and security invariants. **A High Reasoning model is not required**; the implementer may always be selected coding agent, but an independent qualified reviewer must sign off before high-risk completion. Same agent reviewing its own work is not independent.
9. **CHECKPOINT + NEXT:** save commit/status/evidence, review queue and bounded follow-up. Continue nonblocked safe work within current session.

## Required note in a referenced implementation

```text
Task:
Reference: URL @ tag/commit (if available)
License: verified / reference-only / blocked
Adopted: package or pattern
Excluded: noncompatible dependencies/features
Security contract:
Positive + negative tests:
Observed preview:
Remaining risk / independent reviewer:
```

**Licensing:** availability on public GitHub is not a license. Check actual license per path/version. Do not copy source from unclear or restricted licenses. Pure architectural concepts may be documented without reproducing someone else's code.

**Research budget:** one primary official reference + at most one comparison starter per active task by default; stop browsing if authoritative contracts are sufficient. This limits token costs for selected coding agent.
