# Settings, Theme and Branding — v2

Core contains `app_settings` typed registry, `theme_configs` immutable semantic snapshots and `user_preferences`. App bootstrap uses default Salt & Pepper preset. Never store secrets/DB URL/keys in settings DB.

## Configuration classification

| Category | Source | Mutable via dashboard? |
|---|---|---|
| Infrastructure (DB URL, secrets, storage path) | private process env | No |
| Static modules | `packages/config` code | No; review/deploy |
| Global general/appearance settings | MySQL `app_settings` | Yes, RBAC |
| User preference `light/dark/system` | MySQL `user_preferences` | User's own preference |
| Brand assets | built-in static default; Media IDs only if Media enabled | Yes when Media active |

`app_settings` general = app name, short name, description, locale/timezone, static fallback logo/favicon, optional media references. Public branding endpoint outputs allowlisted safe fields, never internal settings. Media disabled => ensure branding has no unresolved media references through preflight/controlled fallback.

## Immutable theme change

1. Admin fetches `app_settings.appearance` with `version`.
2. Client previews semantic token values; do not let user store arbitrary CSS, JS, URL or Tailwind class strings.
3. Backend validates typed light+dark tokens, syntax, and WCAG 2.2 AA contrast pairs (normal text 4.5:1, large text and UI nontext 3:1), required token count.
4. Within MySQL transaction insert `theme_configs` new immutable row (unique custom preset_key) and atomically update active pointer only if `app_settings.version==expectedVersion`; audit and bump version; else 409.
5. Existing row stays immutable; rollback = point to previous snapshot in new audited transaction. The Salt & Pepper system preset is never modified directly.

Default resolution: authenticated user preference > public `app_settings.appearance.defaultColorMode`; `"system"` follows OS. SSR must render deterministic initial mode with safe preference cookie (not authorization source) to avoid hydration flash. Theme applied via CSS variables; Tailwind classes remain statically compiled. Public and admin use same semantic tokens globally.

## Test gates

Contrast validation for every token pairing, unknown tokens rejected, invalid CSS rejected, concurrent edit 409, preset protected, rollback snapshot works, Core-only without Media fallback assets render, SSR mode stable, public branding update appears on subsequent request without rebuild/persistent caching.
