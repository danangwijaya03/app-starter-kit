# Error / Blocker Playbook (Low Agent)

Follow this table **without broad changes outside the task**. If a suggested check is unavailable, record the missing prerequisite.

| Symptom | Safe first check | What NOT to do | Status |
|---|---|---|---|
| Missing package or script | Check `package.json`, task deps, lockfile; verify `node --version` | Invent script result or install random major | Block if dependency missing |
| TypeScript compile failure | Run scoped `tsc` and inspect first error; fix only touched contract/module | Set `strict:false`, use `any` to silence | In progress until test passes |
| npm lock conflict | Check `git diff package-lock.json` and installed npm version | Delete entire lockfile or re-resolve all deps | Block on version mismatch |
| Migration SQL error | Read applied migration history and current schema; use disposable test DB | `db:push`, DROP production schema, reorder history blindly | Block; escalate if shared DB |
| 401/403 incorrect | Check session, status, permission registry, route middleware | Hide menu only, bypass middleware | Block security task if unresolved |
| Better Auth schema mismatch | Compare pinned library generator output with current schema | Modify auth tables ad hoc | Block for scoped schema review |
| 502 Nginx | Inspect read-only process health, bound port, proxy path | Change firewalls/production service without approval | Block deployment if unauthorized |
| Standalone static asset 404 | Check packaged `public` and `.next/static` paths | Upload source tree as workaround | Fix packaging task |
| CMS preview leaks draft | Check authorization/no-store and published pointer path | Return draft publicly | Block; escalate |
| File upload invalid or unsafe | Check MIME signature, size, storage key and traversal prevention | Disable validation | Block media task |
| Redis job duplicated | Inspect queue IDs, locks, DB/job journal | Blindly replay restore or payment jobs | Block if non-idempotent |
| Backup checksum mismatch | Validate manifest and archive in isolated context | Proceed to production restore | Block high-risk task |
| Restore fails mid-import | Keep maintenance, consult external journal and recovery snapshot | Automatically retry or claim rollback completed | Block and escalate |
| Checkpoint disagrees with Git | Trust actual files and commits; rerun narrow tests | Reset hard / delete unknown files | Reconcile first |

## Standard block action

```bash
.venv-agent/bin/python tools/agent_tasks.py block TASK_ID --reason "Specific sanitized error and missing prerequisite"
.venv-agent/bin/python tools/agent_tasks.py doctor
```

When blocked, continue only independent ready tasks. Never guess credentials, disable security, or modify production data to make a task pass.
## Additional optimization guardrails

| Situation | Required response |
|---|---|
| Build passes but business assertion missing | Do not complete; write targeted positive/negative tests, rerun with correct evidence `--kind` |
| Evidence exists but source changed | Rerun focused test after last edit, previous fingerprint cannot be reused |
| High-risk task has no independent review | Leave in-progress/blocked, request separate High/human review, never self-approve |
| Task too large for one session | Before starting, create reviewed split JSON, run `agent_tasks.py split`, verify DAG; never bypass risk gate |
| README references missing npm command | Run `.venv-agent/bin/python tools/check_repo_contracts.py`; fix docs or implement command in correct task |
