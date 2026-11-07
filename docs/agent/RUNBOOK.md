# Agent operational runbook — incremental preview, npm, main

**Canonical branch:** `main`. No planned dev branch; no force-reset. **Default implementer:** low-reasoning coding agent. High reasoning recommended for sensitive work; see [AGENT-ROUTING](AGENT-ROUTING.md).

1. RECOVER: read root AGENTS.md, checkpoint, `git status --short`, actual source and one task card. `python3 tools/bootstrap_agent.py` sets up safe local Python tooling.
2. Select only the first safe ready task from `.venv-agent/bin/python tools/agent_tasks.py next`; honor dependency graph, no hand-waving.
3. IMPLEMENT one bounded end-to-end vertical slice. For early UI display label fixture/demonstration plainly; never use a mock to bypass auth/permission/DB.
4. TEST scoped lint/typecheck/unit/integration/negative in disposable test systems **after the final change**, record actual exit code via agent_tasks.py.
5. VERIFY all acceptance and security denial cases. Independent reviewer required for high-risk effective classification.
6. PREVIEW: run actual available npm dev script (if environment accessible), record path/URL as *verified* only if tested. For infra-only work, report read-only diagnostic, not invented UI. See [preview contract](PREVIEW-AND-FEEDBACK.md).
7. CHECKPOINT: record code state, test evidence, fixture/integrated state, user review queue, commit and remaining task. Maintain [REVIEW-QUEUE](REVIEW-QUEUE.md). Review requested revisions separately from technical CLI status.
8. NEXT: continue automatically to next safe ready task within current session; block ambiguous/destructive/high-risk tasks while allowing independent work to proceed.

**Existing repo:** npm root Next.js 16.4.3. P01 moves it to `apps/web`, never create-next-app again. Production: no Docker, uploaded artifact and aaPanel/PM2. No automatic production DB writes, restore or deploy.

**Installer responsibilities:** [initializer / setup CLI / deployment manager](INSTALLER-BOUNDARIES.md); use an extracted-version CLI on first install before the `current` symlink exists.