# ADR-001 — Modular Monolith Core

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Meminimalkan overhead operasional dan memberi isolasi kode domain melalui module boundaries.

## Decision

Gunakan aplikasi single-tenant per clone dengan satu Hono domain backend, satu Next web, MySQL bersama; bukan microservices.

## Consequences and constraints

Package boundary dan semua authorisasi di API harus diuji; satu database masih coupling deploy.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Core dapat berjalan tanpa media/CMS/operations; login/RBAC/settings tetap sehat.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
