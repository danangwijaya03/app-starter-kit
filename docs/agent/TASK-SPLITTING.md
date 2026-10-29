# Splitting Large Tasks — Operator/Agent Procedure

**Ditujukan untuk: CODING AGENT (task design), reviewer approves changes.** The task registry is authoritative. Do not split after editing the task source.

## When to split

A task needs splitting if it requests more than one independently testable responsibility, spans several unrelated modules, requires a premature database/service change, or cannot be completed and tested within one bounded agent unit.

## Command (review plan before running)

1. Parent must be **pending**, not started. If already in progress, checkpoint, reconcile code, and have a reviewer decide how to replan; do not discard work.
2. Write a temporary JSON plan file outside the repository (or non-secret temporary directory) using **2–9 children**. Example:

\`\`\`json
{
  "children": [
    {
      "title": "Create config schema",
      "scope": ["packages/config/src/env.ts"],
      "steps": ["Define typed Zod schema", "Write negative validation tests"],
      "output_artifact": "packages/config/src/env.ts",
      "acceptance_criteria": ["Invalid URL rejected", "No secret exposed to browser"],
      "test_cases": {
        "positive": ["Valid local config loads without logging secrets"],
        "negative": ["Missing required value rejects with clear error"]
      }
    },
    {
      "title": "Connect config to API",
      "scope": ["apps/api/src/config.ts"],
      "steps": ["Import the shared config", "Test initialization failures"],
      "output_artifact": "apps/api/src/config.ts",
      "acceptance_criteria": ["API uses validated settings"],
      "test_cases": {
        "positive": ["API loads validated settings"],
        "negative": ["API refuses invalid settings"]
      }
    }
  ]
}
\`\`\`

3. Run \`python3 tools/agent_tasks.py split <PARENT_ID> --plan /path/to/plan.json\`. This invokes \`tools/split_agent_task.py\`.
4. Review generated child cards, parent integration checkpoint, phase index, metadata count and DAG using \`python3 tools/validate_plan.py\` and \`git diff --check\`.
5. Commit split-plan changes separately from code work. The original parent ID remains an **integration checkpoint**; existing downstream tasks keep depending on it. New child IDs are \`<PARENT>-S01\`, \`-S02\`, etc. Each child has positive/negative scenarios; parent is completed only after all children and an integration check.
6. Tool cannot undo all filesystem writes atomically if interrupted. On interrupted split, inspect \`git status\` and generated files; never use \`git reset --hard\` blindly.

## Boundaries

Do not auto-split high-risk task to bypass independent review. Children inherit the higher of the original declared risk and automatic phase/keyword classification. The parent remains subject to the same review gate.

Splitting does **not** automatically mark any child or parent completed, does not run database commands, and does not make scripts or tests appear in the app. Adapt acceptance cases to the *real task*, do not copy the example without review.
