# Task graph validation

Run `.venv-agent/bin/python tools/validate_plan.py` after installing PyYAML. The registry should contain 162 unique task IDs (156 original + six scoped v2 tasks); preserve statuses, graph and independent risk review.

## Architecture v2 graph invariants (2026-11-15)

- Core release gate is **P16-11**; selected module matrix is **P16-12**. M2 Core dependency closure must not contain Media, CMS, Jobs or Operations certification tasks.
- P12-03 is optional Media branding. P14-08 is Core independent offsite backup; P15 recovery CLI is outside Hono/Redis; P16-02C worker is optional. No unconditional REDIS_URL or worker dependency for Core-only.
- Phase ID number is a workstream label, not an instruction to finish all lower numbered optional phases. Require actual TASKS.yaml DAG, correct cards and real tests before status changes.
- See [16 ADRs](../architecture/ADR/README.md) and [Architecture Contract](../architecture/MODULE-BOUNDARIES.md).
