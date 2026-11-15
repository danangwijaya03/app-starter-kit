# ADR-010 — LocalFs with S3-ready Adapter

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Sesuai VPS tunggal dan mencegah ekspos storage key.

## Decision

Media disimpan private LocalFs di luar webroot, dibaca melalui Hono; abstract adapter untuk S3 nanti.

## Consequences and constraints

Perlu lifecycle filesystem/DB dan referential retention.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Path traversal, MIME spoof, orphan, access policy diuji.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
