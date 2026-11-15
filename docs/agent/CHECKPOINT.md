# Coding agent checkpoint — Architecture v2 documentation baseline

- Repository: `danangwijaya03/app-starter-kit`, branch `main`.
- **Source truth:** root Next.js 16.4.3 static UI-only demo, not yet a monorepo or working API/MySQL/Auth/RBAC/CMS/worker/backup. No migration, seed, production rollout or feature code is claimed completed from this documentation update.
- **Approved v2:** clone-based Modular Core, web/API + MySQL always on, Redis/worker conditional, Media/CMS/Operations optional with static enabledModules; no installer/Docker. 16 accepted ADRs, one Drizzle journal for 21 tables.
- **Task registry:** `docs/agent/TASKS.yaml` v2.1, **162 planned tasks** = 156 preserved IDs plus P01-10, P03-10, P05-10, P13-07, P14-08 and P16-12. All states remain pending unless independently supported by current-source evidence. Exact status/next via CLI.
- **Core release P16-11** has cross-phase prerequisites: P12 typed settings/theme/audit; P14-08 offsite encrypted Core backup; P15 independent recovery CLI; P16 manual CI/PM2/Nginx. No optional module or Redis dependency for Core.
- Optional certification: P09 Media, P11 CMS requiring Media, P13 Jobs, P14 optional Operations UI; P16-12 selected active-module matrix. The P16-02C worker build must not block Core.
- **Selected coding agent** can be Codex, Claude, Antigravity, DeepSeek, etc; one active implementer per task/session. No required High Reasoning model, but independent qualified security review for high-risk tasks and separate operator approval for live actions.
- Workflow: RECOVER → REFERENCE → IMPLEMENT → TEST → VERIFY → PREVIEW → CHECKPOINT → NEXT. Read active card, [ADR](../architecture/ADR/README.md), [Reference v2](../references/INDEX-V2.md), relevant contract and verify source/license.
- Bootstrap existing tools via `python3 tools/bootstrap_agent.py`, then `.venv-agent/bin/python tools/agent_tasks.py doctor`, `next`, `summary`; run docs/graph validation before starting tasks.
- Never force-reset root Next.js scaffold, copy user data/secrets into template, launch Redis for Core-only, invent passed tests or use production restore HTTP endpoints.
- This checkpoint records **documentation integration only**. Actual CI status and tested source checks must be recorded in subsequent task executions.
