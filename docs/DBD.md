# DBD — Design Brief Documentation

**ID:** DBD-1.0 | **Status:** Implementation baseline | **Style:** Salt & Pepper Minimalist SaaS

## DBD-01 Design direction

Functional admin dashboard uses shadcn/ui; Aceternity UI for selective public hero/feature visual effects and optionally restrained login animation. Do not apply intensive animation to data tables, role permissions or backup actions. Default preset is customizable per project (persist theme tokens), user can select color mode independently. Light is first-install default; support Light, Dark, System.

**Palette exactly from reference:**

| Token swatch | Hex | Role |
|---|---|---|
| White | `#FFFFFF` | Light background, dark foreground actions |
| Light gray | `#D4D4D4` | Borders, muted surfaces |
| Medium gray | `#B3B3B3` | Secondary surfaces, decorative hierarchy |
| Charcoal | `#2B2B2B` | Dark background, light foreground text and buttons |

Semantics may derive opacity/tints from these, e.g. white alpha on charcoal, but colored status danger/success/warning remain available for meaning and must include text/icon (not color alone). **Never use gray-on-white combinations that fail readability checks.**

## DBD-02 Semantic tokens

**Light:** `background=#FFFFFF`, `foreground=#2B2B2B`, `card=#FFFFFF`, `card-foreground=#2B2B2B`, `primary=#2B2B2B`, `primary-foreground=#FFFFFF`, `border=#D4D4D4`, `input=#D4D4D4`, `muted=#D4D4D4` (or translucent), `muted-foreground=#2B2B2B`, `sidebar=#FFFFFF`, `sidebar-foreground=#2B2B2B`, `ring` accessible.

**Dark:** `background=#2B2B2B`, `foreground=#FFFFFF`, `card=#FFFFFF0D` over charcoal, `card-foreground=#FFFFFF`, `primary=#FFFFFF`, `primary-foreground=#2B2B2B`, `border=#FFFFFF35`, `muted=#FFFFFF12`, `muted-foreground=#D4D4D4`, `sidebar=#2B2B2B`, `ring` accessible. Status token overrides must meet accessibility contrast.

Implement complete shadcn semantic variable set (`--background`, `--foreground`, `--card`, `--card-foreground`, `--popover`, `--primary`, `--secondary`, `--accent`, `--muted`, `--destructive`, `--border`, `--input`, `--ring`, `--sidebar-*`, chart tokens) and map to Tailwind. No palette hex hardcoded in feature components; preset registry and validated `theme_configs.tokens_json` own overrides.

## DBD-03 Typography and spacing

- Geist Sans as default UI font; Geist Mono for IDs/code/technical values. Consistent fallbacks.
- 4px spacing grid; base spacing 4/8/12/16/24/32, avoid arbitrary margins.
- Corners: 8px controls, 10–12px cards, pill badges; 1px quiet borders.
- Main sidebar 256px expanded / 72px collapsed; sticky topbar 64px; content max width around 1440px; desktop content padding 24–32px.
- Avoid multiple bold heading levels at once; primary page headings 24–30px, secondary 18–20px, body 14–16px.
- Focus indicator visible on keyboard; touch targets adequate on mobile; responsive tables use overflow or card mode per data density.

## DBD-04 Screen specifications

| Screen | Components | Key interaction states |
|---|---|---|
| Login | Centered logo, email/password form, show password, forgot link | Invalid, loading, rate-limited, forced password change |
| Dashboard | Header, permission-aware stat cards, recent activity, optional chart | Skeleton, empty, widget error, permission-based hide |
| Users | Search/filter, DataTable, add dialog, status/role forms | Pagination, 409, disabled role option, confirmation |
| Roles | Role list, system badge, grouped checkbox matrix, Select All | Dirty changes, 409 version conflict, readonly system role |
| Pages | List status filter, editor action, publish status | Draft/published distinction, validation |
| Page Editor | Left block palette, center canvas, right properties | Reorder, preview, undo/redo optional, save/publish separate |
| Media | Grid/list, upload progress, alt-text edit, reference indicator | Invalid file, in-use cannot delete, no preview |
| Navigation | Header/footer tabs, tree ordering, link picker | Invalid URL, max depth=2, broken unpublished page indicator |
| General | App name, logo/favicon preview, locale, timezone | Dirty state, upload validation, save/reset |
| Appearance | Preset selector, light/dark preview, semantic token editor | Contrast failure, Apply/Reset confirmation |
| Backup | Backup table, progress/status, details, gated restore dialog | Job failure, verification, maintenance, warnings |
| Audit | Server-paginated filters/table, detail drawer | Redacted before/after, empty state |

## DBD-05 Navigation behavior

Sidebar fixed top-level order: Dashboard; Manage Content (Pages/Media Library/Navigation); Manage User (Users/Roles & Permissions); Setting (General/Appearance/Backup & Restore/Audit Logs). Profile and logout in account dropdown. Collapse/expand persists locally for user preference; never modify permissions by local UI state. Group hidden if all children unauthorized. Active state from route, not click-only state.

## DBD-06 Responsive layout

- **Desktop ≥1024px:** sidebar full/collapsible, topbar, table, page editor 3 columns.
- **Tablet 768–1023px:** compact/drawer sidebar, page editor panels collapsible.
- **Mobile ≤767px:** navigation drawer, 1-column stats/cards, horizontal scroll permission matrix, page editor property drawer, accessible touch controls.
- Admin must remain usable at 320px CSS viewport without inaccessible fixed-width dialogs; use viewport-relative sizing and scrolling.

## DBD-07 Aceternity use and component library

shadcn/ui base: buttons, dialogs, inputs, tabs, dropdowns, sidebar, table, toast, card, form. Aceternity: vetted free hero, bento, background and interaction enhancements for public pages; animation off for `prefers-reduced-motion`. Component import via allowed registry/source, license tracked; no premium dependency for core product. Make reusable app-level components `PageHeader`, `DataTable`, `PermissionGuard`, `RolePermissionMatrix`, `ImageUploader`, `StatusBadge`, `ConfirmActionDialog`, `EmptyState`, `AuditTimeline`, `JobProgress`, `ThemePreview`.

## DBD-08 Accessibility and safety

- Target WCAG 2.2 AA: 4.5:1 regular text and 3:1 large text where applicable; 3:1 non-text critical control boundaries; contrast check programmed for editable themes.
- Focus management/dialog trap/escape and keyboard reorder alternative; screen reader labels on inputs and icon-only controls; errors associated with fields.
- Status communication via label/icon + color, no color-only state.
- Motion 150–250ms for lightweight transitions; respect user reduced-motion.
- Long tasks always show non-blocking progress and safe failure state; restore double confirmation clearly states risk and environment.

## DBD-09 Theme configuration model

Use two layers:
1. **Global project theme**: active preset + validated `tokens_json` light/dark, schema version, persisted in DB with source fallback. App administrator can edit via Settings Appearance.
2. **User color preference**: `light`, `dark` or `system`; does not modify global colors.

Public branding bootstrap should render safe values on server, apply tokens before first paint where feasible, and avoid theme flashing. A failed database theme load must fall back to source preset, not a blank page.

## DBD-10 Visual acceptance tests

Test all screens in light/dark on desktop/tablet/mobile; direct link refresh; keyboard-only form and permission matrix; reduced motion; dark mode dialogs and tables; 320px viewport; CMS content with missing media; role matrix with 100+ permission codes; loading/error/empty/conflict; accessible contrast after custom token change. Snapshot tests cannot substitute for actual accessibility behavior verification.