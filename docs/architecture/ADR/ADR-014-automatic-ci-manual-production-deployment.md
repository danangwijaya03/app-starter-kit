# ADR-014 — Automatic CI, Manual Production Deployment

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Kontrol operasional tanpa overengineering CD.

## Decision

CI otomatis pada PR; commit lulus harus disetujui sebelum operator deploy ke VPS aaPanel/Nginx/PM2.

## Consequences and constraints

Deployment dengan downtime singkat boleh, rollback code schema-compatible saja.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Release log dan smoke tests punya bukti.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
