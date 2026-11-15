# ADR-002 — Static Module Configuration

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Per clone sederhana; mengurangi state dinamis dan dependency rollback.

## Decision

Aktivasi modul melalui config TypeScript checked-in dan deploy ulang, bukan UI runtime.

## Consequences and constraints

Build Web/API harus konsisten; disable tidak menghapus data atau izin historis tanpa audit.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

CI menolak missing dependency, route yang nonaktif 404 dan grant tidak efektif.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
