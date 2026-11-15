# ADR-011 — Structured Versioned CMS

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Lebih stabil daripada freeform builder untuk berbagai aplikasi.

## Decision

CMS opsional memerlukan Media; block schema/version + immutable revision + atomic published pointer.

## Consequences and constraints

Perlu migrasi versi blok, media refs, dan optimistic concurrency.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Draft/publish conflict, slug race dan historic renderer lulus.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
