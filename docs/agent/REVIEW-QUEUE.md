# Preview review queue

**Purpose:** asynchronous user feedback on actual development increments. This is *not* proof of successful tests, deployment, acceptance or approval.

| Increment / task | Commit | Mode | Preview URL and path | Verified by agent? | Technical evidence | User review | Notes |
|---|---|---|---|---|---|---|---|
| P00 baseline UI | `bc4c1f24dc2b` (initial static UI source) | Fixture / static | Local `http://localhost:3000/` when `npm run dev` is started | Not verified in this change | Existing Next.js scaffold only; run build/lint locally | pending_review | Static demo, no Hono API, MySQL, authentication or real dashboard yet |

## Append-only work convention

Record a new row when a slice becomes reviewable. Set user review to `pending_review`, `approved`, or `revision_requested` based on explicit feedback only. No approval is implied by time passing. A revision request references a bounded task and acceptance criteria; do not overwrite the original observation. Do not paste screenshots with private data or commit secrets.

When an agent cannot reach the local development server, say so plainly and record exact startup commands. Never label a mock feature as integrated or a static page as fully implemented.
