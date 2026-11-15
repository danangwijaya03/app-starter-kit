# CMS & publishing — structured editor, immutable revisions (ADR-011/008)

References: [Celestia Starter](https://github.com/dev-celestia/celestia-starter) for editorial workflow; [Tiptap](https://tiptap.dev/docs) for bounded rich text JSON.

**Optional CMS module. Requires enabled and certified Media**; core-only clone has no CMS API/routes/menu and no CMS permissions. No full visual page builder or feature installer.

## Adaptation boundary

- Structured blocks with registered `{type, version, schema, editor, renderer}`. Initial block family: hero, rich text, image, feature grid, CTA, spacer. Validate JSON size, block count, schema versions, references and allowlisted rich text nodes/marks.
- CMS rows: `cms_pages` (slug, draft/published pointers) and `cms_page_revisions` (immutable snapshot, revision number, actor); schema lives in centralized Drizzle migration journal, regardless of module enablement.
- Each **Save Draft** generates an immutable revision with scoped `save_key` and input fingerprint; same key + same hash returns previous result, different hash conflicts. Lock page, check expected revision, insert revision + usages + audit transactionally. Stale concurrent editor receives `409`.
- Publish validates version compatibility, revision belongs to page, canonical/reserved slug, referenced media ready and public-eligible. Atomically change published pointer/slug and audit. Unpublish must never expose draft.
- Public renderer only reads published snapshot through Hono, rendered via SSR **without persistent cache** in MVP. Admin, preview, revisions and authenticated CMS responses `no-store`; no Hono→Next cache invalidation webhook until caching is deliberately introduced.
- Preview is authenticated, revision-authorized and never public; avoid portable preview tokens unless a separate review approves them. Old block versions must remain renderable or be migrated through reviewed, testable migration.
- Media usage includes every retained revision, not only published one. Reject physical delete while any retained revision refers to media.

## Exclude

Arbitrary HTML/JS/CSS from CMS data, freeform Webflow clone, scheduled publishing or live collaboration, PostgreSQL/feature installer imports, permanent public preview links.

## Tests

Draft isolation, revision immutability, duplicate save idempotency, stale editor `409`, slug uniqueness/reserved paths, unsupported block failure, publish atomicity, access to unpublished pages denied, preview RBAC/no-store, old revision rendering, delete prevention for media referenced in retained history, module disabled 404.

See [MEDIA.md](MEDIA.md), [UI-FORMS.md](UI-FORMS.md), [SECURITY.md](SECURITY.md).
