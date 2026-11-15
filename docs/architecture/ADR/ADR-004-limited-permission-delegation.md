# ADR-004 — Limited Permission Delegation

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Role editor tetap dapat dipakai harian tanpa hak super-admin tak terbatas.

## Decision

Administrator hanya mendelegasikan permission dengan metadata delegable dan yang dimilikinya, bukan protected/sensitive, serta tidak dapat self-escalate.

## Consequences and constraints

Metadata source immutable registry, transaksi/locking untuk last-superadmin.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Eskalasi berantai, self-grant, dan concurrent last-holder test ditolak.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
