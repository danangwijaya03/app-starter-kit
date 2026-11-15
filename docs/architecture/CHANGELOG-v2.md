# Architecture Documentation v2 Changelog

2026-11-14 — Accepted design revision, implementation pending.

- Core/MUST separated from Media/CMS/Operations optional release modules.
- Static module dependency/permission sync; one centralized schema.
- Limited RBAC delegation, invited accounts, transaction audit and last-holder concurrency.
- Direct Hono behind Nginx same-origin, SSR internal HTTP; admin no-store, CMS public SSR no persistent cache.
- Durable job intent MySQL, dispatcher, optional BullMQ.
- LocalFs Media public/private delivery and crash-safe lifecycle.
- CMS versioned blocks and immutable revisions with save dedupe.
- Immutable semantic theme snapshots, fallback branding, per-user color mode.
- Independent restic offsite backup and operator CLI restore; no dashboard production restore endpoint.
- Pino/health/external uptime; approved SHA CI/manual deployment.
- Core release checkpoint cross-phase, optional certification, registry 156 original task IDs protected.
- No code or database migration applied to GitHub by this documentation package.
