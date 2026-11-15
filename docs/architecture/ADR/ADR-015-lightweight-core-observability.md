# ADR-015 — Lightweight Core Observability

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Cukup untuk satu VPS tanpa stack metrics terpisah.

## Decision

Pino redacted JSON, transactional MySQL audit, health/readiness, PM2 rotation, external uptime monitoring.

## Consequences and constraints

Audit tetap tidak tahan DBA root; kebutuhan yang lebih berat nanti ADR.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Audit fail-closed, secrets tidak terekam, alert backup/uptime diuji.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
