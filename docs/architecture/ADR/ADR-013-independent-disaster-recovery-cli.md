# ADR-013 — Independent Disaster Recovery CLI

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Aplikasi mungkin tidak berfungsi saat perlu pemulihan.

## Decision

Backup offsite terenkripsi sebagai prereq production; restore production hanya CLI di lingkungan staging lalu cutover operator.

## Consequences and constraints

Perlu offsite credentials terpisah, backup/GC coordination, drill.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Recovery dari VPS kosong lulus tanpa Hono/MySQL prod/Redis.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
