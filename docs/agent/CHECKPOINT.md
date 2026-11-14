# Coding-agent checkpoint — clone-based reference-driven plan

- Repo: `danangwijaya03/app-starter-kit`, branch `main`.
- Existing Next.js 16.4.3 root scaffold and **static demo preview**; web/api/worker monorepo, MySQL integration, auth, RBAC, CMS, operations remain task targets.
- Architecture decision: **Clone-Based Reusable Starter Kit + Reference-Driven Development + Single Active Coding Agent**.
- Active implementer (provider-independent): **coding agent yang dipilih**. High reasoning AI model not mandatory. Effective **high-risk task** still requires **independent qualified review** under `agent_tasks.py`; do not self-approve.
- **NO** `apps/installer`, project generator, release archive/version-symlink deployment manager, or Docker requirement. New projects = clone + private env + new DB/Redis/storage + reviewed manual npm setup scripts; deploy manually using PM2 + Nginx.
- Current documentation task statuses are pending; never mark tasks completed based on planning changes. Start `python3 tools/bootstrap_agent.py`, run `.venv-agent/bin/python tools/validate_plan.py`, `agent_tasks.py doctor`, `next`, `summary`.
- Read one active card + one matching domain under `docs/references/`. Record source URL/version/license only if verified and adapted; tests after last edit, actual preview (or not verified) and user feedback.
- No live DB mutations, restore, production deploy or secrets in repository. Existing working tree should never be force-reset or reinitialized.
- **Documentation-only change:** monorepo and target npm scripts have **not** been implemented/tested as part of this update. Validate docs integrity/CI and npm baseline separately.
