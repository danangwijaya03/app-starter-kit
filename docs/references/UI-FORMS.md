# UI, forms & reusable components

Sources: https://ui.shadcn.com/ ; https://tanstack.com/table/latest ; https://react-hook-form.com/ ; https://zod.dev/ ; https://github.com/ueberdosis/tiptap .

**Prefer official libraries with narrow use:** shadcn/ui primitives/style samples as candidates, TanStack Table for pagination/filter grids, React Hook Form for interactive forms, Zod shared schema for API contracts, Tiptap for CMS editor. Preserve DBD Salt & Pepper semantic token palette and four top-level menu groups.

**Preview-first:** build responsive shell/fixture early, explicitly label mock state and do not fake successful persisted operations. All actual form submissions require Hono API validation even if client schema exists.

**Tests:** keyboard navigation, contrast, validation errors, loading/empty/denied states, mobile width, optimistic update rollback, cross-site/unsafe input cases where applicable.

**Scope control:** no wholesale component-library or marketing-template import unless specifically justified in task and license check.
