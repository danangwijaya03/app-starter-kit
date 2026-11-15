# ADR-012 — Unified Semantic Theme

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Brand consistency dan rollback aman tanpa rebuild.

## Decision

Satu semantic token theme global public/admin, immutable snapshots dan per-user color mode.

## Consequences and constraints

Fallback branding wajib tanpa Media; CSS arbitrary ditolak.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

WCAG contrast, 409 concurrent edit, SSR mode dan rollback test.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
