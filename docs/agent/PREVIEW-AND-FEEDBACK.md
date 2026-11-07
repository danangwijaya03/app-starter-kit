# Preview & Feedback Contract — incremental delivery

**Audience:** coding agents, reviewer, developer. **Branch:** `main`; no automatic production deployment.

## Purpose and modes

Every meaningful implementation increment should leave the existing Next.js application runnable. **UI fixture** means illustrative static/mock components only, with visible `DEMO`/fixture labels and no claims of real API/DB behavior. **Integrated** means a real Hono API and development MySQL/Redis are connected, and the intended positive/negative tests pass. Infrastructure-only tasks may demonstrate read-only health diagnostics and reproducible checks instead of inventing a UI feature.

A preview is not a release and does not substitute authentication, authorization or test evidence. Never insert real credentials, sensitive schema values, customer data or unsafe production endpoints in previews. The public app may display only non-sensitive static development status.

## Required handoff for each independently reviewable slice

1. Start from the current checkout. Check `git status --short`, current task/card, and `docs/agent/CHECKPOINT.md`. Do not discard existing edits.
2. Implement the smallest complete vertical slice in its approved scope, using UI + typed API + database contract where relevant. For early UI work, mark fixture-only functionality explicitly.
3. Run the existing scoped lint/typecheck/unit/integration and negative tests **after** the last edit. Do not claim nonexistent npm scripts or a passing app based only on documentation.
4. Verify dev startup with the actual available npm script. In the root Next.js baseline use `npm run dev`; after P01 migration discover scripts in package.json. Use the existing Lerd environment; never change global routing or expose development preview to the LAN.
5. Record in `docs/agent/CHECKPOINT.md`: task ID, commit, runnable URL and path (if personally verified), preview mode (`fixture`/`integrated`/`diagnostic`), precise review steps, observed result, tests/exit codes, blockers and next ready task. Never invent reachability.
6. Update the review queue in `docs/agent/REVIEW-QUEUE.md` with a concise reviewable increment. If URL is not verified, state `not verified` and provide local launch commands instead.
7. User feedback is asynchronous and **non-blocking** for unrelated ready tasks. Convert requests to bounded revision tasks with acceptance criteria, preserve current evidence, and re-run affected tests. Do not interpret silence as approval.
8. Only technical verification promotes `completed` to `verified` through the existing task CLI/gate; visual review state is **separate** (`pending_review`, `approved`, `revision_requested`). Human approval cannot replace independent security review for high-risk code.

## Practical preview milestones

- P00: static Next.js dashboard/roadmap preview at `/` (clearly labelled, not a live admin dashboard).
- P01: integrated monorepo development web/API boot and **early visual admin shell** without unauthorized private routes.
- P02–P03: read-only integration/DB diagnostics visible only in a safe development context, or documented terminal verification when private.
- P04–P05: login and first-admin/permission checks, no bypass via fixture mode.
- P06–P08: authorized shell, user/role management, dashboard using real APIs.
- P09–P12: media, CMS drafts/public publish, settings.
- P13–P15: queue, backup, staging restore as controlled local tests; dangerous operations never exposed through debug preview.
- P16: artifact-only install, upgrade and rollback exercised in disposable/test environment.

## State and boundaries

- Current `agent_tasks.py` statuses remain `pending / in_progress / blocked / completed / verified`. Do not invent unsupported CLI status commands.
- Review status lives only in `REVIEW-QUEUE.md`; do not mutate task registry status to represent UX approval.
- A low-reasoning coding agent may implement well-scoped slices. Follow `AGENT-ROUTING.md` to identify tasks recommended for high-reasoning implementation/review, and block on unclear security-critical decisions.
