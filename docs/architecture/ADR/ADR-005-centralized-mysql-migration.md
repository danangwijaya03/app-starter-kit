# ADR-005 — Centralized MySQL Migration

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Menghindari drift schema dan lifecycle migration per modul.

## Decision

Satu schema semua modul dan satu Drizzle migration journal untuk setiap clone.

## Consequences and constraints

Tabel opsional tetap ada walau modul disabled; MySQL DDL tidak selalu transactional.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Fresh dan upgrade migration pada MySQL 8.4 lulus, no `push` production.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
