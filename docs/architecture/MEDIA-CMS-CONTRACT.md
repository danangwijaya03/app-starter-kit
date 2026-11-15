# Media, CMS & Page Builder Contract — v2

## Media module

Module `media` is independently usable; `cms` requires `media`. Adopt permission codes `media.view`, `media.upload`, `media.update`, `media.delete`, replacing `cms.media.*` through reviewed registry migration. Never leave alias grants with effective access after migration; mapping only for deliberate one-time data conversion.

### Upload and lifecycle

1. Hono validates `media.upload`, request size, extension, actual MIME/signature, image decoder, dimensions, and rate limit.
2. Default allowed JPEG, PNG, WebP; max 10 MiB, max 20 MP, one upload/request. Reject SVG, HTML, executables and polyglots not passing safe decoder. Apply server and Nginx body limits; streaming limit must not buffer unbounded requests.
3. Write random-key temporary file outside webroot; normalize and decode to known safe output if configured; calculate SHA-256.
4. Insert MySQL `media_assets(status=pending, visibility=private)` and associated metadata.
5. Atomically move/rename to final key on **same filesystem**; update DB `status=ready`, `ready_at` after durable file validation. If crash: pending record not visible; reconciler checks filesystem metadata and safely finalizes/cleans. Don't claim DB+FS atomicity.
6. Public file is available **only if** `ready AND visibility=public AND not deleted`, and public use is authorized by policy. Private file checks session, RBAC and resource scoping; `Cache-Control: private,no-store`. Serve with `nosniff`, trusted content type, content-disposition appropriate to risk.
7. Soft-delete denied while referenced by any retained CMS revision or settings, and physical deletion deferred. Cleanup must re-check references under compatible lock and not run during backups retaining objects.
8. LocalFs root not writable by web/public user. Reject traversal and symlink escape (verify resolved file path stays inside root, use safe open flags when available); never derive path directly from original filename. S3 implementation deferred, adapter interface in MVP.

### Suggested API

- `GET /api/v1/media` permission `media.view`.
- `POST /api/v1/media` `media.upload`; returns 201 when ready; failure must not return ready metadata.
- `PATCH /api/v1/media/:id` `media.update`; metadata only.
- `DELETE /api/v1/media/:id` `media.delete`; 409 for referenced file.
- `GET /api/v1/media/:id/file` private file RBAC/resource policy.
- `GET /api/v1/public/media/:id` public safe version, no direct key path.

## CMS module

Structured editor, **not freeform pixel/HTML page builder**. Versioned registry provides:
```ts
type Block = {
  id: string;           // UUID per instance
  type: "hero" | "richText" | "image" | "featureGrid" | "cta" | "spacer";
  version: number;      // versioned props format
  props: unknown;       // validated by registry Zod
};
```
Block registry has `{type,version,schema,defaults,editor,renderer,migrations?}`; server loads only schema definitions, never React renderer/editor. Store rich-text as validated Tiptap JSON; URLs use allowlist of schemes; never execute stored HTML/CSS/JS. Bound number and depth of blocks, text lengths, JSON bytes. When a published block version lacks renderer, deployment compatibility check must fail rather than serving executable fallback.

### Immutable revisions and save algorithm

- `cms_pages` stores published pointer and slug; `cms_page_revisions` stores `revision_no`, content JSON, SEO and candidate slug.
- `POST /api/v1/cms/pages/:id/revisions` carries `saveKey` (request UUID), `expectedRevisionNo`, validated content. Within txn: lock page; check same key + payload hash (replay returns original); compare expected latest revision; on mismatch 409; insert next immutable revision with unique `(page_id,revision_no)` and media_usages; audit; commit.
- No silent last-writer-wins or server autosave requirement in MVP. Save draft does not change live pointer.
- `POST .../publish` takes `revisionId,expectedPublishedRevisionId`, validates same-page revision, slug uniqueness/reserved prefixes, renderer compatibility, referenced `ready/public` media, then atomically moves `(published_revision_id, published_slug)` with audit. On race 409.
- `unpublish` sets both pointer/slug NULL transactionally; revision stays. `restore-revision` *creates new draft*, never edits history.
- Public `/api/v1/public/pages?slug=...` returns published pointer only; Next SSR no persistent cache MVP. Preview requires signed short-lived token bound to user/session+revision and active session, always no-store.
- Slugs lowercase slash-leading canonical; disallow reserved `/api`, `/admin`, `/_next`, login/system paths. Changed slugs return 404 at old path in MVP; redirects deferred.
- Public navigation max 2 levels, stable ordered links, exclude unpublished target, validate cycle and cross-menu parent.

## Media reference race and backup

Every retained revision registers media_usages, including drafts and historical published revisions; removing revision requires explicit retention policy and usage cleanup in same txn. Media delete and usage assignment use consistent locking. Final media file content is immutable: replacement creates new key. Independent backup can record DB snapshot, derive media manifest, block garbage collection until selected files are copied, then verify checksum.

## Acceptance tests

Duplicate save idempotent; concurrent editors 409; unpublished draft never leaks; old renderer compatibility retained; publish/slug conflict 409; private media denied public; MIME spoof/path traversal denial; missing file reconciled; historical revision image cannot be physically removed; CMS disabled cannot serve any CMS route.
