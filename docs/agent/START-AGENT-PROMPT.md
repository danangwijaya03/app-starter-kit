# Starting Prompt — Low Reasoning Agent

Use when this **documentation package has been copied into a real repository**. Not an instruction to run destructive actions automatically.

```text
Implement the Codelight Next.js Monorepo Starter Kit using the repository's low-reasoning task cards.

1. Read AGENTS.md, docs/agent/LOW-REASONING-RUNBOOK.md and IMPLEMENTATION-CONTRACTS.md.
2. Run python3 tools/agent_tasks.py doctor and python3 tools/agent_tasks.py next.
3. Inspect git status/diff and any existing work. If there is an in_progress task, resume it.
4. Open ONLY docs/agent/tasks/<CURRENT_ID>.md and its specified references.
5. Start the task with the agent CLI, implement its microsteps, run actual scoped tests, save evidence, and checkpoint.
6. Never mark an untested task complete. If blocked, record the exact sanitized blocker and select a different ready task only if independent.
7. Continue to the next ready task automatically whenever safe; use only one in_progress task at a time.
8. Do not modify production or shared data, destructive migrations, live credentials or production deployment without explicit user authorization.
9. Do not write the initial admin password to source, docs, commits, prompts or logs. Use secure install-time secret input.
10. If session context/limit is nearly exhausted, use progress checkpoint and stop in a recoverable state.

Do not redesign the stack. No production Docker. Release artifact + README-SERVER.md must be tested from an isolated target-compatible environment.
```

**First command for the user in a local developer environment:** `python3 -m pip install -r tools/requirements-agent.txt` (prefer virtualenv), then `python3 tools/agent_tasks.py next`.