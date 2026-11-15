# TASKS.yaml Rebase Plan — v2 rebase record\n\n**Registry integration:** original 156 task IDs/status/evidence preserved; six new scoped IDs **P01-10, P03-10, P05-10, P13-07, P14-08, P16-12** yield 162 tasks. Old task plan descriptions below are the change rationale, not the active registry. `docs/agent/TASKS.yaml` and corresponding cards are authoritative, CI/DAG checks still required.\n\n**Key dependency cuts:** Core P12-07 no longer requires Media picker P12-03; backup P14-01..04 and P14-08 no longer rely on Redis/Media/Operations; P15 independent operator recovery depends P14-08 rather than Operations UI; P16-02 Core build excludes worker P16-02C; P16-05 PM2 Core excludes P13; P16-02A excludes CMS. **P16-11 Core production gate** can be verified without Redis/worker/Media/CMS/Operations; **P16-12** certifies all module-enabled variants later.\n\n**Scope correction:** output_artifact paths for independent recovery use `tools/recovery/`, not `apps/worker/`; permission Media uses `media.*`, hardcoded first admin email removed, REST restore endpoint prohibited, all DB tables centrally migrated. This is docs/task rebase only, not a claimed implementation.\n

The reviewed registry declares **156 tasks** across P00–P16; many tasks have microtask children. Do not write a replacement YAML from memory. Read every task and card in the checkout, retain IDs/status/commit/test evidence, and modify per task only after recording original and new dependencies. Use `tools/agent_tasks.py` or another YAML DAG validator to ensure no cycle/dangling ID. Record diff + count before/after.

## Known task IDs requiring review

| Existing task IDs | Change required | Gate |
|---|---|---|
| P00-01 / P00-02 / P00-05 | Incorporate v2 ADRs, consistent requirement IDs, architecture links; no silent legacy replacement | Specs baseline |
| P01 tasks | Build two always-on apps + optional worker; no assumption Redis startup mandatory | Core build |
| P02 tasks | Redis setup only when jobs enabled; Core-only local dev tests | Core dev |
| P03 tasks | Single migration history; 21 base tables; expanded columns; permission metadata; **DB migration compatibility** | Database |
| P04/P05 tasks | Status `invited`, Better Auth protection, limited delegation, last-holder lock and audit transaction | Security |
| P06–P08, especially P08-05 | Make dashboard Core-only with missing CMS widgets suppressed; add release checkpoint AFTER settings/backup prerequisites (not blindly after P08) | Core UI |
| P09 | Media public/private endpoints, lifecycle, no worker dependency for simple images | Media certification |
| P10/P11 (P11-06/P11-07) | Save idempotency, block version renderer compatibility, SSR no persistent cache; remove stale cache-invalidation requirement | CMS certification |
| P12-01/02/04/05/07/08 | Move **execution readiness** earlier than Core production release without renumbering; base branding without Media; immutable theme snapshots | Core release |
| P12-03 | Media-backed branding enhancement only; depends on P09 (optional) | Media/UI |
| P12-06 | Audit viewer/Core; log write integration should exist earlier P05 | Core release |
| P13 tasks | Durable `system_jobs` dispatcher, lease/replay/idempotent worker; optional runtime | Jobs certification |
| P14-02A/B/02, P14-03/04 | Extract **independent** backup CLI and offsite manifest/recovery verified before first Core production release; may need new explicitly scoped prerequisite task cards | Core production prerequisite |
| P14-05/06/07 | Operations API/UI optional; UI must not be mandatory for core backup | Operations certification |
| P15 tasks including P15-07 | Rework production recovery as CLI, staging import, operator gate. Remove one-click restore API & worker retry | Recovery |
| P16-01/P16-02A/B/C/P16-02 | P16-02C worker build **conditional**, not required for Core release | Deployment |
| P16-03/04A-D/04 | Manual migration/seed/bootstrap preflight executed for Core before first production use; admin email operator-supplied | Core setup |
| P16-05/06/07/08 | Two PM2 processes minimum, worker optional, Nginx same-origin and operator rollback compatibility | Deployment |
| P16-09A/B/09, P16-10/11 | Document and test Core-first release and separate active-module matrix | Final release |

## Rebase strategy

- **Do not make all P12/P14/P16 tasks prerequisites of P08**, causing a task graph cycle. Instead introduce bounded infrastructure Core tasks after P05 or P08 as needed and/or split existing tasks with original parent ID retained; inspect DAG before selecting exact IDs.
- Task IDs of existing 156 items remain unchanged. New tasks must be assigned only after `TASKS.yaml` has been parsed to check ID uniqueness, new cards created, `metadata.task_count` recalculated and generated task reports updated. Do not invent empty `completed` state.
- Core phase gate has extra cross-phase prerequisites: P08 UI + Core subset of P12 + independent backup/recovery + manual-deploy subset of P16. Phase numbers describe historical workstreams, **not necessarily chronological strict release milestones**.
- Module certification requires its own dependencies and tests; avoid `P16-11` forcing CMS/worker when disabled.
- For every modified task card, update `scope`, `steps`, `acceptance_criteria`, `validation`, and `spec_refs`; do not change historical `completed_commit/tests_evidence` without legitimate revalidation.
- Remove `cms.media.*` usage in relevant cards and use `media.*` with migration and test.
- Remove API `POST /backups/:id/restore` as production restore path and all old UI promises.

## Required rebase acceptance report

Task count/IDs before and after; newly added IDs/cards; zero dangling refs/cycles; state and evidence preserved; no forced worker for Core-only; settings/backup prerequisites satisfy Core release; no production destructive restore endpoint; link checker clean; diff approved by reviewer.
