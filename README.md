# app-starter-kit — Next.js 16 + npm Workspaces roadmap

**Currently implemented:** Fresh Next.js 16.4.3 / React 19.3.0 / Tailwind v4 app at repository root, installed using `npx create-next-app@latest`. Full-stack monorepo features are **not** implemented yet.

## Run existing app

```bash
npm ci
npm run dev
npm run lint
npm run build
```

Do not re-run create-next-app. Keep the existing Next.js code. During P01 the coding agent **moves** existing code into `apps/web`, then builds npm Workspaces + Turborepo.

## Start a low-reasoning coding agent

```bash
python3 -m pip install -r tools/requirements-agent.txt
python3 tools/validate_plan.py
python3 tools/agent_tasks.py doctor
python3 tools/agent_tasks.py next
```

Read [AGENTS.md](AGENTS.md), [Low Agent Runbook](docs/agent/LOW-REASONING-RUNBOOK.md), and **only one** [current task card](docs/agent/tasks/). Complete each atomic task with real testing evidence. On a new session, inspect Git and checkpoint and resume safely.

## Docs
[PRD](docs/PRD.md) · [TRD](docs/TRD.md) · [AFD](docs/AFD.md) · [DBD](docs/DBD.md) · [BSD](docs/BSD.md) · [IPD](docs/IPD.md) · [Task registry](docs/agent/TASKS.yaml) · [Phases](docs/agent/PHASES.md) · [Checkpoint](docs/agent/CHECKPOINT.md).

[README-SERVER.md](README-SERVER.md) is a **future deployment runbook**. The CLI described there does not exist until its tasks are implemented and tested.

## Production
**No Docker.** Build release artifact compatible with Linux target, upload to server, run web/API/worker with Node/PM2 behind aaPanel/Nginx; MySQL and Redis are services. Installer bootstraps a protected `admin@codelight.id` via a secure one-time secret and mandatory password change.
