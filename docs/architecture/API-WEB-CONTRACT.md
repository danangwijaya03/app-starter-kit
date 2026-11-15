# Hono API, Next.js Frontend & Caching — v2

## Route namespaces

- `/api/auth/*`: mounted Better Auth native handler; it owns native schemas/response.
- `/api/v1/*`: Hono OpenAPI/Zod validated business API, all private endpoints RBAC protected.
- `/api/v1/public/*`: allowlisted read-only public projection; do not expose draft/admin metadata.
- `/api/health/live`, `/api/health/ready`: operations; `/api/health/subsystems`: protected subsystem report.
- `/`: Next.js SSR, `/admin/*` protected route groups, CMS published-only catchall below system routes.

Nginx routes `/api/*` to Hono `127.0.0.1:4000`, everything else to Next `127.0.0.1:3000`, preserving exact request path and same-origin cookies. Never implement duplicate business routes as Next Server Actions/Route Handlers.

## Hono middleware, errors, and routes

Order (details vary per public/Better Auth group): request ID & redacted log → body/rate limits → safe-method CSRF/Origin (for unsafe cookie-auth browser calls) → session/account status → module/permission guard → Zod input validation → service+repository → audit+response. Better Auth's own handler requires separate lifecycle control, not the business RBAC pipeline.

Business item envelope:
```json
{"data":{"id":"example"},"meta":{"requestId":"req_123"}}
```
Error:
```json
{"error":{"code":"PERMISSION_DENIED","message":"Insufficient permission","details":null},"meta":{"requestId":"req_123"}}
```
List `meta`: `page` default 1, `limit` default 20 max 100, `total`,`totalPages`,`requestId`; deterministic sort with ID tiebreaker. 401 missing session, 403 unauthorized, 404 disabled/nonexistent module, 409 optimistic conflict, 422 invalid payload (normalize chosen Zod status), 429 rate limiting, 5xx redacted. Error code stable API contract.

### Route composition

```ts
const app = new OpenAPIHono();
// Better Auth handler registered under /api/auth/*
app.route("/api/v1", coreRoutes);
if (modules.media) app.route("/api/v1", mediaRoutes);
if (modules.cms) app.route("/api/v1", cmsRoutes);
if (modules.operations) app.route("/api/v1", operationsRoutes);
// Exclude inactive routes from generated OpenAPI document.
```

This is architecture pseudocode; don't treat import names as current source. Avoid top-level side effects before config validation. `controller.ts` is **optional** (not mandatory); `routes.ts` coordinates HTTP/Zod, `service.ts` invariants/transactions, `repository.ts` DB queries.

## Internal SSR HTTP and client HTTP

Browser:
```ts
fetch("/api/v1/me", { credentials: "same-origin", cache: "no-store" })
```

Next Server Components:
```ts
import "server-only";
fetch(`${process.env.API_INTERNAL_ORIGIN}/api/v1/me`, {
  headers: { cookie: trustedAuthCookiesOnly },
  redirect: "manual",
  cache: "no-store"
});
```

`trustedAuthCookiesOnly` is a server helper extracting only Better Auth cookie names per actual installed version; filter or reconstruct, never forward untrusted proxy auth headers wholesale. Backend recomputes authorization per request. Do not put session bearer tokens in `localStorage`. Expose only browser-safe config variables to client.

## Cache and data boundary matrix

| Resource | Server data/cache | HTTP cache header |
|---|---|---|
| Auth/session/roles/users/audit | `no-store` | `private, no-store` |
| Admin dashboards/tables/settings | `no-store` | `private, no-store` |
| CMS draft/preview | `no-store` | `private, no-store` |
| Public CMS published page | SSR `no-store` MVP (no persistent data cache) | `no-store` MVP |
| Public branding/theme | SSR latest typed projection | conservative no-store MVP |
| Hash-versioned JS/CSS/image static asset | immutable static cache | `public,max-age=31536000,immutable` if content hash |

`cacheComponents:true` in the existing Next config must not result in private data leaking to another user. Avoid `use cache` around user-specific data. Public CMS persistent cache/webhook revalidation postponed explicitly. After React Query mutation invalidate associated keys, refresh server view as needed; after logout or identity switch clear query cache and refresh navigation.

## Module-specific pages

Next file-system routing remains built even when feature disabled: run **server-side** `requireEnabledModule` guard to return 404. Hiding sidebar alone is not enforcement. Public CMS route parser rejects `/api`, `/admin`, `/_next`, auth paths and reserved prefixes; defined routes take precedence.

## Idempotency

Use unique persisted key with payload hash for operations such as invite/job creation, and CMS save. Same key+same payload returns existing resource; same key+different payload gives 409. Transactions and locks resolve concurrent requests. Never rely on HTTP retry behavior alone.

## Acceptance tests

Cross-account SSR leak, revoked role immediately 403, signed-out query cache empty, protected route noncacheable, inactive modules 404 at Hono + Next, CSRF mutation denied, pagination max enforced, OpenAPI does not expose disabled routes.
