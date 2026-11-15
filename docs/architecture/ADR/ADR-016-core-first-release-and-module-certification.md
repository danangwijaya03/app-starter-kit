# ADR-016 — Core-first Release and Module Certification

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Mempercepat adopsi clone sederhana dan memperjelas readiness.

## Decision

Core dapat release tanpa Media/CMS/Operations; modul opsional memiliki suite dan release gate sendiri.

## Consequences and constraints

Core tetap memerlukan settings, external backup, recovery dan deployment; P12/P14/P16 harus direbase.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Core-only Redis-free gate lulus, optional suites lulus untuk modul yang aktif.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
