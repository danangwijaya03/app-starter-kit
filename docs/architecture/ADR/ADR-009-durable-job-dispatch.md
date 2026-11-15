# ADR-009 — Durable Job Dispatch

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Meminimalkan job hilang saat Redis outage; tidak bergantung pada exact-once semantics.

## Decision

API commit intent ke MySQL `system_jobs`; dispatcher mengirim BullMQ, worker idempotent; Redis/worker opsional.

## Consequences and constraints

Perlu lease/claim, replay dan reconciliation; restore tidak auto-retry.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Outage/crash tests menjaga intent dan side effects tunggal.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
