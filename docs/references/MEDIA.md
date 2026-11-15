# Media & storage — LocalFs with S3-ready adapter (ADR-010)

Research: [Celestia Starter](https://github.com/dev-celestia/celestia-starter) media adapter patterns, [Hono docs](https://hono.dev/docs/), [Sharp docs](https://sharp.pixelplumbing.com/) for bounded processing.

**Media is optional and independent of CMS**; CMS depends on Media, not vice versa. Core-only uses built-in static logo/favicon fallback.

## Adopt

- StorageAdapter methods `put/read/stat/delete` with server-generated opaque storage keys; LocalFs lives outside webroot and is the MVP provider. A future S3-compatible adapter must not alter business APIs.
- Separate upload validation: auth/RBAC, request stream size, allowlisted content signatures + decode, safe dimensions (initial 10 MiB / 20 megapixels / JPEG/PNG/WebP; configurable), checksum and randomized path. Reject SVG/HTML/executable, symlink and traversal escape. Apply Nginx and Hono limits; no browser-provided filesystem paths.
- Lifecycle: `pending → ready → deleted` plus `failed`. Stage in private temp path, persist pending metadata, atomically rename within same filesystem, mark ready; reconciliation handles orphan temp/final files after crash.
- Separate **public delivery** by explicitly public, ready asset; **private delivery** requires session, permission and resource checks. Private responses `Cache-Control: private, no-store`; safe content type and `nosniff` for both.
- Store `media_usages` for CMS revision history, settings and business references. Delete uses consistent locks/reference checks; no physical deletion while referenced by **any retained revision**. GC holds during production backup snapshot.
- Synchronous bounded processing permitted without Redis. Heavy transformations are explicit jobs and require approved worker capability.

## Exclude

Direct uploads signed by client without reviewed policy, default public upload folders, trust in `Content-Type`/extension, unconditional thumbnail jobs, S3/R2 credentials in browser, implicit CMS dependency.

## Tests

Forbidden/private reads; MIME spoof, pixel bomb, oversized streams, traversal/symlink, duplicate keys; kill between metadata/rename/ready and verify reconciliation; concurrent add-reference versus delete; old revision media retained; Core-only fallback; media-disabled routes 404.
