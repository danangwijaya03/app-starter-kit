# ADR-003 — Better Auth and Application RBAC

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Mencegah ketidakcocokan dua RBAC dan memanfaatkan autentikasi vendor.

## Decision

Better Auth menangani identitas/sesi; app RBAC menjadi otoritas tunggal hak bisnis.

## Consequences and constraints

Lifecycle account status harus dijaga juga pada Better Auth endpoints.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Sign-in suspended diblok; next protected request setelah pencabutan role 403.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
