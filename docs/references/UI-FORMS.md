# UI, forms, caching and unified branding (ADR-007/008/012)

References: [Next.js App Router](https://nextjs.org/docs/app), [shadcn/ui](https://ui.shadcn.com/), [TanStack Table](https://tanstack.com/table/latest), [React Hook Form](https://react-hook-form.com/), [Zod](https://zod.dev/), [Tiptap](https://tiptap.dev/docs) for CMS only.

## Core implementation

- Use Next.js Server Components by default; Client Components for forms, editors, interactive grids. Use shared Zod DTOs; Hono **revalidates** every request.
- Browser API client calls relative `/api/v1/*` with same-origin credentials; Next.js server client calls internal Hono origin and forwards selected auth cookies. Do not implement duplicate business routes in Next.js.
- `no-store` for profile, admin dashboard, RBAC, drafts, private media, previews, sessions and all private data. Public CMS is SSR without persistent data cache in MVP. Versioned assets may have bounded cache.
- TanStack Query used on interactive admin lists; invalidate relevant queries on mutation; clear private query cache when identity switches or session ends; `router.refresh()` is **not** persistent-cache invalidation.
- Core Settings and unified semantic theme work without Media: static logo/favicon fallback. Theme snapshots immutable, active pointer switched transactionally, user prefers `light/dark/system`, global branding dynamic on SSR.
- No arbitrary CSS from DB. Validate allowlisted theme tokens and accessible color contrast; use stable class names and CSS variables, not CSS string injection.
- Optional module nav links and pages follow static config and RBAC. Server guard `notFound()` for disabled module; menu hiding alone does not enforce permission.
- Keep existing Salt & Pepper visual language and accessible primitives; references are inspiration, not a full copied design system.

## Tests

Keyboard/focus/contrast; loading/empty/denied; mobile layout; validation; SSR no cross-user leakage; logout/login cache clearance; simultaneous theme update conflict; safe branding fallback when media off; CMS-disabled route 404; forms not claiming persisted success for mock data.
