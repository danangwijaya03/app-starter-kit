# Security — official middleware, ASVS verification, no shortcut

References: https://asvs.owasp.org/ (ASVS 5.0) ; https://hono.dev/docs/middleware/builtin/csrf ; https://hono.dev/docs/middleware/builtin/secure-headers ; https://better-auth.com/docs/plugins/admin .

**Prefer official security primitives** over copied ad-hoc JWT/CSRF/session middleware. For browser cookie-based auth, review CSRF for every unsafe route and validate trusted origins/forwarded headers. Use strict cookie flags and appropriate CORS; secure headers, MIME checks, size limits and rate limiting by threat model.

**Authorization:** server API enforces deny-by-default for private routes. Direct API calls must be rejected independently of frontend menu. No SQL string interpolation for untrusted input, arbitrary file path or dynamic code eval. Query scope must prevent horizontal access.

**Secrets:** env server-only, permissions restrictive; never write token, cookie or admin password to Git, diagnostic response, snapshot or logs. All destructive DB operations run only in isolated test resources unless operator explicitly approves production execution.

**Minimum negative test matrix:** no-session 401, missing grant 403, invalid CSRF/origin denied as configured, brute-force/rate limit, stale/revoked session denied, forged upload MIME/path rejected, private draft inaccessible, secret log redaction, migration fails closed on wrong DB. Link cases to relevant OWASP ASVS controls at implementation time.

**Review rule:** selected coding agent may implement. Independent qualified reviewer checks actual diff + tests before high-risk completion; more test cases do not turn self-review into independent review.
