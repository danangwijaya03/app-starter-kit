# Architecture v2 — Consistency Reconciliation (2026-11-15)

**Status:** documentation-only corrective patch for the accepted architecture v2 design. **Not evidence of implemented features.**

Repository: <https://github.com/danangwijaya03/app-starter-kit>. The default branch was publicly inspected on 2026-11-15. At inspection time the repository already contained the 16 ADRs, the v2 reference playbooks, an integrated PRD/roadmap and a **162-task** registry. This patch **does not** reconstruct or replace the previous Architecture v2 packages, rewrite task IDs, or imply those features are deployed.

## Why this patch exists

Earlier review notes marked broad architecture integration as incomplete. The newer `main` state already incorporates most of it. The remaining risks are **legacy statements inside otherwise-current documents**, which a coding agent could misread in isolation. The companion `tools/architecture_v2_sync/apply.py` makes narrow, fail-closed changes against the actual checked-out files; it refuses unexpected source text.

## Canonical decisions preserved

- Web + API + MySQL mandatory; Redis/BullMQ worker only when a statically enabled module needs jobs.
- Better Auth identity plus application RBAC, four user statuses (`invited`, `active`, `inactive`, `suspended`), bounded grant delegation.
- All 21 logical tables use one Drizzle migration history; never create conditional schemas based on module toggles.
- Media LocalFs public/private with immutable ready objects; retained revisions/settings protect media from physical deletion.
- Structured CMS immutable revisions; Admin/draft `no-store`, published public SSR **without persistent cache** on MVP.
- Jobs persist durable intent in MySQL; Redis enqueue is a transport, execution is at-least-once. A dispatcher claim must be fenced by a persisted lease owner.
- Independent encrypted offsite backup and **operator CLI-only production recovery**, not HTTP restore, not BullMQ retry.
- CI automatic; production deployment approved and manual. Core release P16-11 is independent of optional module certification P16-12.

## Corrected documents

| Path | Key correction |
|---|---|
| `docs/PRD.md` | Core release language for Redis, SSR branding, media retention, independent CLI recovery, settings UI |
| `docs/TRD.md` | Two required runtimes, conditional Redis provisioning, health probe isolation |
| `docs/BSD.md` | `invited` default, no installer, lease-fenced durable jobs, no active `backups.restore` permission, SSR publish |
| `docs/AFD.md` | Operations backup route is not restore UI, media retention, recovery CLI test wording, model-neutral agent |
| `docs/agent/IMPLEMENTATION-CONTRACTS.md` | No `backups.restore` business permission, no forced CMS cache invalidation, optional worker, four status values |
| `docs/references/ARCHITECTURE-BASELINE.md` | ADR and v2 docs are integrated, not merely planned |
| `docs/references/ADOPTION-PROTOCOL.md` | Read current accepted ADR/162-task registry; stop on actual conflicts |
| `docs/architecture/README.md` | Replace stale instructions to integrate two already-merged ZIP packages |
| `docs/architecture/DATABASE-CONTRACT.md` | Persist `dispatch_lease_owner` for safe dispatcher ACK |
| `docs/architecture/JOBS-CONTRACT.md` | Fence queue-send acknowledgement against current stored lease |

## Required test evidence before any source implementation

1. **Core-only test** — no Redis environment variable, Web + API + MySQL ready, optional routes 404.
2. **RBAC/auth** — `invited` denied until activation, inactive/suspended denied, delegation bounded, last Super Admin race secured by transaction.
3. **Media** — unauthorized/private reads denied; referenced media from every retained revision cannot be physically removed.
4. **CMS** — `409` for stale saves, retries do not duplicate revision, publish visible on next SSR without revalidate webhook.
5. **Jobs** — two dispatchers competing with expired leases cannot ACK each other's claims; Redis success + lost DB ACK does not duplicate terminal effects.
6. **Recovery** — public/business API has no production restore endpoint; independent CLI works with app/Redis offline; offsite manifest and staging import verified.
7. **Release** — 162 task IDs and 16 accepted ADRs unchanged; no task status changed simply because docs were patched.

## Scope and caution

The patch only changes Markdown prose. It **does not** alter `docs/agent/TASKS.yaml`, migration SQL, permissions tables, code, secrets, CI, runtime, or GitHub. Complete database column definitions, JSON schemas and worker protocols are still implementation targets; review with pinned library versions before coding.

The `dispatch_lease_owner` column is an additional *proposed schema contract* needed for the already accepted leased dispatcher algorithm. This is **not** a production migration. Drizzle must generate/review its actual SQL, including legacy backfills and concurrency tests.

## How to verify

```bash
python3 tools/architecture_v2_sync/apply.py --repo . --show-diff
python3 tools/architecture_v2_sync/apply.py --repo . --apply
python3 tools/architecture_v2_sync/apply.py --repo . --check
git diff --check
git diff -- docs
```

The tool backs up edited original files outside the repository directory before applying and refuses unknown/multiple matching anchors. To create **complete replacement Markdown files** for manual copy/replace without editing the checkout, use `python3 tools/architecture_v2_sync/apply.py --repo . --export`.
