# Synchronization Plan for Existing Documentation — Architecture v2 transition record\n\n**Status after integration:** PRD/TRD/BSD/AFD/IPD/README-SERVER/Roadmap/Agent Contract/DECISIONS have been aligned with accepted v2 as target requirements. This remains a historical checklist, **not a statement that application features are implemented**. Task graph currently has 162 tasks (156 retained + six scoped additions); validation is required on every change.

**Intended action:** Integrate revision addenda in `docs/revisions/` into corresponding legacy files with review. Do not delete original requirement IDs, SQL tables, task status or evidence. `tools/integrate_revision.py` can add versioned appendices to legacy Markdown without overwriting original details; this is an **interim safe merge**, not the final editorial cleanup. Once accepted, fold addenda into original sections in a follow-up PR and eliminate contradicted old sentences.

| Original | Current conflict | Authoritative v2 addendum |
|---|---|---|
| `docs/PRD.md` | All CMS/worker/restore MUST in one MVP | [PRD](../revisions/PRD-v2-ADDENDUM.md): Core Must, optional Media/CMS/Operations Should |
| `docs/TRD.md` | Three always-on runtimes, Redis default, CMS cache invalidation | [TRD](../revisions/TRD-v2-ADDENDUM.md): 2 required runtimes, job conditional, SSR no cache |
| `docs/BSD.md` | Missing schema deltas, `cms.media.*`, `/backups/:id/restore` | [BSD](../revisions/BSD-v2-ADDENDUM.md): DB/access contracts and API corrections |
| `docs/AFD.md` | Media menu under CMS, public page revalidate, one-click restore flow | [AFD](../revisions/AFD-v2-ADDENDUM.md): module gating, concurrency, CLI recovery |
| `docs/IPD.md` | P00-P16 linear phase graph implies Core waits for P15/P16 | [IPD](../revisions/IPD-v2-ADDENDUM.md): cross-phase Core checkpoint and certifications |
| `docs/DEVELOPMENT-ROADMAP.md` | Phase outcomes group everything | [ROADMAP](../revisions/ROADMAP-v2-ADDENDUM.md) |
| `docs/agent/IMPLEMENTATION-CONTRACTS.md` | Fixed admin email, worker mandatory, controller mandatory | [CONTRACTS](../revisions/IMPLEMENTATION-CONTRACTS-v2-ADDENDUM.md) |
| `README-SERVER.md` | Worker/Redis always listed | [SERVER](../revisions/README-SERVER-v2-ADDENDUM.md) |
| `docs/agent/DECISIONS.md` | Explicit single MVP | `docs/agent/DECISIONS.v2-PROPOSED.md` (needs reviewed replacement) |
| `docs/agent/TASKS.yaml` + 156 task cards | Priority, dependency and outcomes aligned to old MVP | `TASK-REBASE-PLAN.md` (manual graph-aware update) |
| `docs/DOCUMENTATION-MAP.md`, `README.md` | Links don't mention v2 | Link to architecture v2 readme, ADR index and final SPEC |
| `docs/DBD.md` / other related docs | Possibly mirror old behavior | Diff via repo-wide search before merging; update traced references |

## Must-fix searches before claiming complete

```text
cms.media.
admin@codelight.id
/backups/:id/restore
restore production from dashboard
Redis required
worker always
three Node runtimes
revalidate old/new public paths
installer
task_count: 156
```

"installer" search results may be historical negation and should **not** all be deleted. For each hit record replacement decision. In all docs include `Status: target, not implemented` and never claim source now contains Web/API/worker code.

## Review checklist

- Stable original PRD IDs and BSD relational invariants preserved.
- `docs/agent/TASKS.yaml` task IDs, statuses, links and evidence preserved during rebase; task_count and DAG validator reflect any reviewed new tasks.
- No duplicated `permissions` authority; Media codes `media.*`; no one-click production restore.
- Core release requires settings+backup CLI even though historic phases P12/P14 occur later.
- All module routes from Hono + Next are disabled when configured off.
- No unconditional Redis/worker startup in Core-only scripts, CI or deployment docs.
- No stale cache invalidation requirement on SSR/no persistent cache MVP.
- Explicit legal decision pending regarding GPL-3.0 distribution.
- Each changed requirement has acceptance test and owner; all docs links local-resolvable.

## Workflow

1. Create feature branch; capture source SHA and `git diff --stat`.
2. Copy new docs with `prepare_revision.py --apply` (skips conflicts).
3. Read addenda and optionally append to legacy files with `integrate_revision.py --apply` (backs up originals outside repo).
4. Review each edit, replace old conflicting sentences at source sections and remove duplication while retaining IDs. Prefer small PRs by domain.
5. Modify original task registry only after full `TASKS.yaml` parse+validation and task card updates. Review high-risk entries.
6. Run Markdown link check, YAML load, `tools/agent_tasks.py summary`, DAG checks, test commands **when implemented**. Document results, review, merge.
