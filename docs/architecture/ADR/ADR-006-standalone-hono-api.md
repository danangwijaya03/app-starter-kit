# ADR-006 — Standalone Hono API

**Status:** Accepted (design) · **Date:** 2026-11-14 · **Implementation:** Pending

## Context

Mendukung web dan calon mobile client dengan kontrak API yang sama.

## Decision

Hono di :4000, Nginx same-origin `/api/*` ke Hono, business routes versioned; Next tidak menduplikasi business API.

## Consequences and constraints

CSRF, cookie forwarding, dan route registry harus ketat.

## Alternatives considered

Alternatif fitur lebih dinamis/terintegrasi tinggi atau infrastruktur yang lebih kompleks dipertimbangkan, namun ditunda karena menambah dependensi dan memperlebar cakupan MVP. Revisi keputusan memerlukan ADR baru, pemeriksaan migrasi kompatibilitas, dan pembaruan task graph.

## Verification

Browser/client SSR auth sesuai dan disabled module route 404.

## Related specifications

- [Unified SPEC](../../../SPEC-001-app-starter-kit-modular-core.md) (dalam paket; setelah disalin ke repo, SPEC berada pada root).
- [Architecture index](../README.md).
