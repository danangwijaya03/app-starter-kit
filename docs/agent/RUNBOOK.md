# Agent operational runbook (npm)

1. Read root AGENTS.md, current repo baseline and low-reasoning runbook.
2. Run `python3 tools/agent_tasks.py doctor` and `next`.
3. Inspect `git status`, active card, dependencies and scope.
4. Start the task, implement, run actual tests, record evidence, complete and checkpoint.
5. Continue automatically with another ready task when safe. Do not promise continuation after a session ends.
6. For session recovery inspect Git + CHECKPOINT first, never blindly reset or rerun data operations.

**Existing repo:** npm and root Next.js 16.4.3. P01 moves it to apps/web; never scaffold a new app. **Production:** no Docker; uploaded release with aaPanel/PM2.
