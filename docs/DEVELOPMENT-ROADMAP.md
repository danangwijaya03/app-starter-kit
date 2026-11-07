# Development Roadmap — Continuous Preview on main

**Branch:** `main` only (as approved). **Primary goal:** each implementation increment changes real source and is reviewable before the whole project is complete. **Baseline:** Next.js 16.4.3 root scaffold. Existing 157 technical task IDs and dependency semantics remain intact; 4 small preview/integration tasks are added (161 total). No claim is made that all 161 have been executed.

## Delivery method

Development is an **incremental vertical-slice model**: implement a small coherent slice → execute real scoped tests → verify feature/data/denial behavior → show a verified local preview (or diagnostic) → checkpoint/commit → continue safe ready task. End-user visual feedback is asynchronous and kept separately from technical gate states.

A frontend-only preview may precede API/database implementation, but MUST be visibly labelled `fixture / demo` and MUST NOT simulate authentication or claims of persistence. Once real API/DB integration exists, replace the fixture or label it separately. The local preview uses existing Lerd and npm. Do not add Docker or another MySQL/Redis instance; do not expose diagnostics on public production routes.

## Review checkpoints for the retained technical phases

| Phase | Scope | Reviewable result |
|---|---|---|
| P00 | Existing scaffold, plans, tools | Next.js static dashboard preview (not integrated) |
| P01 | Monorepo, early UI shell | Salt & Pepper sidebar layout with four sections and preview smoke |
| P02 | Lerd/MySQL/Redis development environment | Read-only safe diagnostic for service availability |
| P03 | Drizzle schema and migrations | Real DB connection readiness (no schema details/secrets) and test evidence |
| P04 | Auth | Login/session/first-password-change integrated flows |
| P05 | RBAC & admin bootstrap | Actual admin with granted/denied paths and protected bootstrap |
| P06 | Authorized admin shell | Turn fixture shell into authenticated responsive navigation |
| P07 | User/role CRUD | Real permission checklist and user management |
| P08 | Dashboard metrics | Role-aware metrics from API/MySQL, not mock numbers |
| P09 | Storage/media | File upload/list/delete with persistence and access checks |
| P10 | CMS drafts and revisions | Page editor and draft/publish lifecycle |
| P11 | Public CMS | Published-only public routing, navigation and protected draft preview |
| P12 | Settings | Persistence of app name, logo and visual preset |
| P13 | Worker/queue | Local queue health/job test with safe retry semantics |
| P14 | Backup | Verified encrypted backup on disposable test data |
| P15 | Restore/recovery | Isolated staging restore and maintenance/recovery evidence |
| P16 | Release/installer | Artifact-only installation, update, rollback, derivative initializer tests |

**Technical ordering detail:** UI fixture appears at P00/P01; the full authenticated shell is deliberately built only at P06 after P04/P05. The table is not a license to break the authoritative `TASKS.yaml` dependency DAG. The original phase ID order remains unchanged because renumbering historical IDs would create avoidable migration errors.

## New early tasks

- `P01-08` create a post-monorepo Salt & Pepper shell fixture; output is clearly labelled demo.
- `P01-09` add repeatable preview smoke and documented handoff; fail when URL is unreachable.
- `P02-07` dev-only Hono/Lerd status; hard deny in production, no secret response.
- `P03-09` DB readiness diagnostic after verified schema/migrations; test healthy/unhealthy conditions.

## Acceptance at each increment

1. Code, not just documentation, changes in the scoped repository path when implementation is requested.
2. Existing app remains runnable; pass relevant automated tests after final edit. Failure is disclosed, not hidden.
3. UI review handoff records **actual URL+path if verified**, fixture/integrated/diagnostic mode, reproduction steps and unresolved behavior.
4. Current checkpoint and review queue updated without inventing a passing test, user approval or running server.
5. Independent review for security-critical work; review does not grant production mutation permission.
6. Continue safe ready tasks automatically during the same session; user's UI feedback is non-blocking except where it changes a blocking dependency.

## Tooling and agent selection

Start with `python3 tools/bootstrap_agent.py`; run `.venv-agent/bin/python tools/agent_tasks.py doctor`, `next`, `summary`, and inspect one task card. Default **Low reasoning** for bounded routine work. Use **Medium** for cross-module integration; recommend **High reasoning** for design/implementation or independent review involving Auth/RBAC, migrations, secrets, private media/CMS preview, backups/restore, release/rollback/installer and graph refactors. See [Agent Routing](agent/AGENT-ROUTING.md).

The task CLI's technical statuses are unchanged: `pending`, `in_progress`, `blocked`, `completed`, `verified`. Human UI review lives in [REVIEW-QUEUE](agent/REVIEW-QUEUE.md): `pending_review`, `approved`, `revision_requested`. No automatic promotion of CLI status based on UI review.

## Installer delivery model

Three components: **Project Initializer**, **Application Setup CLI** and **Deployment Manager**. Implement lower-level services incrementally in P01/P03/P05; P16 packages/coordinates them. On a cold install, run setup from `releases/vX.Y.Z/cli/cli.js` before the `current` symlink exists. See [Installer Boundaries](agent/INSTALLER-BOUNDARIES.md) and [Server Guide](../README-SERVER.md).

## Practical run for user review

From the existing Next.js root: `npm ci` then `npm run dev`, open `http://localhost:3000/`. After P01 migration consult actual npm workspace scripts; do not assume old scripts work. Static preview at `/` is currently a fixture; app/test reachability must be verified on your machine. Do not claim an unrun build passes.
