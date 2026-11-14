# Coding Agent Runbook — single model + incremental preview

**Implementer: coding agent yang dipilih.** **Branch: main.** **Runtime plan:** three apps (web/API/worker) + manual clone/setup, no installer.

1. RECOVER — `git status --short`, checkpoint, `python3 tools/bootstrap_agent.py`, `.venv-agent/bin/python tools/agent_tasks.py doctor` and `next`. Resume in-progress work after inspecting real diff.
2. REFERENCE — read only active task, relevant specs, one domain [reference](../references/REFERENCE-MAP.md) and [adoption protocol](../references/ADOPTION-PROTOCOL.md). Pin external source/version/license before adapting code.
3. IMPLEMENT — one bounded responsibility/end-to-end slice. Prefer official library; preserve local contracts, MySQL and npm. No installer/generator/feature installer.
4. TEST — run actual scoped positive/negative checks on isolated fixtures **after last edit**, use `agent_tasks.py run` for evidence.
5. VERIFY — check API permission/DB data/side effects, rollback/retry/concurrency where relevant. For effective high-risk, independently reviewed result required; no self-approval or need for a High Reasoning model.
6. PREVIEW — verify local UI/API/diagnostic, record actual route/URL and fixture/integrated status; if unavailable record failure truthfully.
7. CHECKPOINT — source and test evidence, reference attribution, review queue, commit and next ready task.
8. NEXT — continue another safe ready task during the session. Production actions and destructive DB operations require explicit authorization.

Current scripts: root `npm run dev`, `lint`, `build`. Future workspace scripts must exist before running; `docs/MANUAL-CLONE-SETUP.md` lists planned commands.
