# ADR-008 — SSR First CMS Cache Strategy

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Menghapus kompleksitas invalidasi antarproses sampai memiliki kebutuhan terukur.

## Decision

Published CMS SSR tanpa persistent cache untuk MVP; admin/draft selalu no-store.

## Consequences and constraints

Public response bisa lebih berat pada DB; optimasi nanti perlu ADR.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Publish langsung terlihat pada SSR berikutnya, draft tak pernah publik.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
