# Resume Prompt — Low Reasoning Agent

```text
Resume work in the existing repository. Do NOT restart the project or duplicate completed modules.

1. Read AGENTS.md and LOW-REASONING-RUNBOOK.md.
2. Run python3 tools/agent_tasks.py doctor and python3 tools/agent_tasks.py next.
3. Inspect git status --short, git diff, recent commits and current checkpoint.
4. If a task is in_progress, open its card and reconcile actual modified files and tests before editing.
5. If no task is active, select only the first ready pending task and read its card.
6. Finish the task, execute real tests, record evidence with agent_tasks.py run, then complete with factual note.
7. Checkpoint each unit and continue automatically to the next independent ready task if safe.
8. Never repeat migration/seed/bootstrap/restore or destructive action without checking actual state, target environment and authorization.
9. If blocked or time/context is low, save a truthful checkpoint. Never claim tests or features that did not run.
```