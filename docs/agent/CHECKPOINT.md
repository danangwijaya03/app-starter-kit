# Development checkpoint — baseline planning state

- Repository: `danangwijaya03/app-starter-kit`, **branch `main`**.
- Source currently: existing root Next.js 16.4.3 + React 19.3.0; npm lockfile and Tailwind 4. P01 must `git mv` the existing app to `apps/web` rather than reinitialize.
- This revision introduces a **static development preview at `/`** (Salt & Pepper shell mock). It is **NOT** real auth, API, RBAC, MySQL, or dashboard data. Availability/build is **not verified by local execution from this GitHub documentation edit**; run `npm ci`, `npm run lint`, `npm run build` and `npm run dev` locally and record observed results.
- Plan: 157 original tasks preserved, 4 incremental preview tasks appended: **161 pending**; statuses must not be marked done by a docs commit.
- Agent lifecycle: RECOVER → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT.
- Default low reasoning for explicit microtasks. High recommended for security, migrations, restore, releases and dependency rewrite; independent reviewer still mandatory for effective high risk.
- `docs/agent/PREVIEW-AND-FEEDBACK.md` explains handoff and `docs/agent/REVIEW-QUEUE.md` records asynchronous user feedback independent of CLI status.
- Run `python3 tools/bootstrap_agent.py` (one-time/reentrant tooling), then `.venv-agent/bin/python tools/validate_plan.py`, `.venv-agent/bin/python tools/agent_tasks.py doctor` and `next`.
- Do not modify live DB or run production deployment; no initial admin passwords, secrets or real data in source/preview/logs.
