# Testing references — evidence is stronger than self-review

References: https://vitest.dev/ ; https://playwright.dev/ ; https://asvs.owasp.org/ .

**Test method:** select scoped unit tests (Vitest), integration tests using isolated MySQL and Redis, API contract tests, negative authorization tests, and Playwright browser checks for changed UI. A screenshot or passing lint is not sufficient for mutation/authorization safety.

**Risk-sensitive cases:** session revoke, 401/403; last super-admin concurrency in actual MySQL; migration replay/drift on disposable DB; CMS draft isolation, invalid blocks/publish conflicts; upload traversal/MIME; worker job retry/idempotency; backup checksum+restore into separate disposable target; manual production config validation without deploying.

**Reviewer:** independent qualified person/agent reads the diff and test assertions and records outcome under the existing high-risk review mechanism. Implementer selected coding agent can prepare all artifacts, but must not self-sign. Availability of a more expensive model is not mandatory.

**Progress:** as each bounded task completes, record real exit codes, source fingerprint and last validated commit. Do not assume a test passed because a doc proposes it.
