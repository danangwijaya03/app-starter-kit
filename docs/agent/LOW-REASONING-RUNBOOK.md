# Low-Reasoning Agent — Standard Operating Procedure

> **Use this page first** after `AGENTS.md`. This is a **documentation-only specification**, not a completed Next.js application.

Local developer environment: **Lerd, Node.js 26, MySQL and Lerd Redis**. Read [LOCAL-LERD-NODE26.md](LOCAL-LERD-NODE26.md) before P02. Never provision duplicate services, and never let tests target development/production DB. Test evidence must match the final current code state.

## The only workflow

1. Install once: `python3 -m pip install -r tools/requirements-agent.txt` (prefer a virtual environment).
2. Inspect: `python3 tools/agent_tasks.py doctor`.
3. Select: `python3 tools/agent_tasks.py next`.
4. Open the **one task card** indicated in `docs/agent/tasks/<ID>.md`.
5. Inspect Git worktree (`git status --short`, `git diff --stat`) and existing implementation. **Do not assume missing or completed files**.
6. Read `docs/agent/IMPLEMENTATION-CONTRACTS.md` and only the specifications named in the task card. **Do not read all 157 cards.**
7. Begin: `python3 tools/agent_tasks.py start <ID>`. This refuses tasks with incomplete dependencies.
8. Implement card microsteps in order. Never invent API permissions or database columns. When exact schema/API isn't specified, mark blocked.
9. Run focused actual tests and save evidence: `python3 tools/agent_tasks.py run <ID> -- npm --workspace @repo/api test -- rbac` (replace example with a **real command relevant to your task**).
10. Complete: `python3 tools/agent_tasks.py complete <ID> --note "API guard rejects missing grants; tests passing"`. The CLI refuses completion without passing check evidence, but **the agent must additionally verify acceptance criteria honestly**.
11. Select next with `python3 tools/agent_tasks.py next`. Repeat until out of time. No user confirmation for safe routine work.

**Never run an example command containing `<placeholder>` literally.** Do not use `validate_plan.py` alone as proof of application implementation. In P00, documentation validation is relevant; elsewhere use actual implementation tests.

## Small-session strategy

- Plan at most **one card** at a time. Additional ready tasks are optional only after checkpointing.
- If a card is still too large, first write an in-progress checkpoint identifying completed substeps; break into child tasks only if necessary and validate the dependency DAG.
- Finish in a valid state. If a unit cannot be finished, capture WIP: `python3 tools/agent_tasks.py progress <ID> --note "Implemented ... ; test ... pending"`.
- After interruption, run `doctor`, inspect Git, then resume the same `in_progress` task. **Never blindly repeat a non-idempotent operation**.
- If the test environment is missing, `block <ID> --reason "<sanitized reason>"`, and select independent ready work if available.

## Status rules

| State | Meaning | Allowed transition |
|---|---|---|
| `pending` | Not started | `start` or `block` |
| `in_progress` | Agent owns one unit | `progress`, `run`, `complete`, `block` |
| `blocked` | Unmet dependency, environment, risk gate | `unblock` to pending |
| `completed` | Code + relevant tests passed with evidence | Phase `gate` only |
| `verified` | Phase-level tests passed | No automatic rewrites |

## Completion evidence, not wishful thinking

Use `run` to execute real non-destructive verification commands and record JSON containing command, UTC time, exit code and commit. The tool **cannot** independently determine that tests cover all acceptance criteria, so the agent must inspect real assertions and actual outcomes. Never record secrets in command arguments.

The task registry is `docs/agent/TASKS.yaml`. The CLI is the supported writer. The task card is instruction text, not the source of task state. Checkpoint files summarize work and are never authoritative over source files/Git/database state.

## Escalation: when Low reasoning is insufficient

Stop the affected unit and request higher-reasoning review (or a human decision) when dealing with: auth/session security bypasses, super-admin concurrency invariants, destructive migrations, database restore, publishing data integrity violations, production release migration compatibility, or library version/API contradictions. Continue independent safe units if any.

## Commands that are **not** available in a docs-only repository

`npm run dev`, `npm run db:migrate`, `npm run release:build`, `npm run release:verify` and `node current/cli/cli.js ...` are **targets to be implemented by the assigned cards**. Never mark them passed before code and tests exist.