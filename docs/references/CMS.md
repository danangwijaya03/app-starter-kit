# CMS & publishing — incremental reference-driven adaptation

Sources: https://github.com/dev-celestia/celestia-starter (CMS editorial workflow) ; https://github.com/ueberdosis/tiptap (headless editor library).

**Adopt pattern:** page and immutable revision records, draft save, preview, publish/unpublish, slug conflict handling, SEO, public navigation, typed block registry, editor UX (Tiptap core optional). Keep the project's BSD/AFD schema canonical.

**Exclude initially:** full Celestia blog/feature installer, PostgreSQL migrations, unsplash/R2 credentials, real-time collaboration, arbitrary HTML/JS renderer, scheduled publishing unless explicitly added later.

**Security invariants:** public route reads only pointed published revision; save draft never changes published revision; published pointer updated atomically and references same page; preview uses authorized short-lived token, no-store and no public draft exposure; validated block schema and sanitized output; slug conflicts = 409; reference-safe media deletion.

**Tests:** draft isolation, publish/unpublish, unauthorized preview, duplicate slug, invalid blocks, concurrent edit expected version. Use fixture UI only when clearly marked DEMO.
