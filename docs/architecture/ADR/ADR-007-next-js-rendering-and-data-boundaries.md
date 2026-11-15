# ADR-007 — Next.js Rendering and Data Boundaries

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Menghindari backend ganda dan membatasi secrets di server.

## Decision

Server Components sebagai default, browser HTTP langsung Hono, server HTTP internal dengan selected session cookie.

## Consequences and constraints

Semua admin/API privat `no-store` dan query cache clear saat logout.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Cross-user SSR cache leak test dan permission changes observed next request.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
