# Media & storage — local-first and safe by default

Sources: https://github.com/dev-celestia/celestia-starter (media-R2 feature for design pattern); https://hono.dev/docs/ .

**MVP:** local filesystem adapter under private server path, server-owned storage keys, validated MIME/signature/size, explicit max uploads, metadata in MySQL, immutable reference/use records, prevent delete for published usages. API must enforce grants; never trust browser-provided filename/path as filesystem path.

**Optional later:** S3-compatible/R2 adapter (never mandatory), transformations/thumbnails, direct upload with signed URLs after threat model. Cloud credentials only server-side.

**Tests:** happy upload/read, forbidden upload, forged MIME, path traversal, oversized stream, reused key collision, published-reference-safe delete, orphan cleanup. No media under public dir before rules are defined.
