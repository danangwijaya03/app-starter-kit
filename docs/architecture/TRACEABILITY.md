# Requirements → Architecture → Tests / Tasks — v2

**Preserve all original PRD IDs**. The following mapping supplements the existing PRD/BSD/AFD identifiers, which remain in force unless scope is reclassified.

| Requirement(s) | Release scope | Architecture contract | Suggested existing phase | Validation |
|---|---|---|---|---|
| AUTH-REQ-01..04 | Core MUST | AUTH-RBAC-CONTRACT | P04 | Session, reset, signup deny, forced password |
| USER-REQ-01..02 | Core MUST | AUTH-RBAC-CONTRACT; DATABASE-CONTRACT | P05/P07 | Concurrent last holder, status revocation |
| RBAC-REQ-01..03 | Core MUST | AUTH-RBAC-CONTRACT; MODULE-BOUNDARIES | P05/P07 | Delegation, grant sync, enabled modules |
| DASH-REQ-01 | Core MUST | API-WEB-CONTRACT | P06/P08 | Role-limited widgets |
| SET-REQ-01 and theme | Core MUST | SETTINGS-THEME-CONTRACT | P12-01/02/04/05/07/08 **rebase earlier** | CSS contrast, runtime branding, 409 |
| Audit/logging | Core MUST | AUTH-RBAC-CONTRACT; OPERATIONS-RUNBOOK | P03/P05/P12-06 | Transactional audit fail |
| Core production backup/recovery | Core MUST operational | OPERATIONS-RUNBOOK | P14/P15 **split CLI prerequisite earlier** | clean-server restore rehearsal |
| MEDIA-REQ-* | Media OPTIONAL | MEDIA-CMS-CONTRACT | P09 | upload denial, lifecycle, refs |
| CMS-REQ-* / NAV-REQ-* | CMS OPTIONAL (requires Media) | MEDIA-CMS-CONTRACT | P10/P11 | old block version, 409, no draft leak |
| Worker/Jobs | Jobs capability OPTIONAL | JOBS-CONTRACT | P13 | Redis outage, lease replay, side effect |
| Operations UI | Operations OPTIONAL | JOBS-CONTRACT; OPERATIONS-RUNBOOK | P14/P15 | jobs and backup viewer, no restore production endpoint |
| Clone/setup/release | Core MUST | OPERATIONS-RUNBOOK; TESTING-RELEASE | P16 + Core checkpoint | same-origin HTTPS, approved SHA, module matrix |

**New IDs proposed for requirement classification only:** `CORE-01..04`, `OPS-01`, `RELEASE-01`. Do not renumber existing PRD IDs or task IDs.

The source task registry reported `metadata.task_count:156` as of 2026-11-14. Before modifying it, verify actual task ID set using `tools/agent_tasks.py`. Registry status and DAG remain authoritative for execution but do not supersede architecture ADR.
