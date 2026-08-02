

<!-- 
HUMAN NOTE:
- Don't remove legacy auth yet
- Migration pending from v1 API
- Claude should NOT know this because it may break refactors
-->

# Project: Job Application Tracker
A Kanban-style web app for tracking job applications.
Stack: Next.js 14, TypeScript, Tailwind CSS, Supabase.
The app runs at localhost:3000 during development.

## Essential Commands
- Start dev server: `npm run dev` (runs at localhost:3000)
- Run tests: `npm test`
- Run tests with UI: `npm test:ui`
- Type check: `npm run typecheck`
- Build: `npm run build`
- Lint: `npm run lint`

## Local Development Setup
The app uses a **local PostgreSQL database** for development (not Supabase cloud).
- Database: `job_tracker` (user: `dev`, password: `devpassword`)
- Connection: `postgresql://dev:devpassword@localhost:5432/job_tracker`
- See [MACOS_QUICK_START.md](MACOS_QUICK_START.md) for setup instructions
- Required env vars: `DATABASE_URL` (already in `.env.local`), and optional Supabase auth credentials

## Conventions
- Components: PascalCase (TaskCard, KanbanColumn)
- Functions/variables: camelCase
- CSS classes: kebab-case
- Files: kebab-case.tsx for components
- API routes: /api/resource-name (REST conventions)

## Structure
- /app — Next.js app directory (pages and routes)
- /components — reusable UI components, including auth context
- /lib — utilities (Supabase client in lib/supabase.ts, custom hooks in lib/hooks/)
- /types — TypeScript definitions (types/supabase.ts is auto-generated from database schema)
- /supabase — database migrations with schema and RLS policies

**Architecture:**
- State management: React Context (auth state in components/auth-context.tsx)
- Authentication: Supabase Auth (optional, can use local auth or NextAuth - see FULL_LOCAL_AUTH.md)
- Database: PostgreSQL with Row Level Security (RLS) policies enforcing user data isolation
- API: Next.js API routes following REST conventions (/api/resource-name)

## Component Patterns
- Client components (marked with 'use client') handle Supabase queries and auth state
- Use the `useAuth()` hook (from lib/hooks/useAuth.ts) to access current user
- Pass user data via React Context, not props where possible, to avoid prop drilling
- Protected routes use `ProtectedRoute` component wrapper to enforce authentication

## Database Queries
- Import Supabase client: `import { supabase } from '@/lib/supabase'`
- Use `.from('table_name')` to query tables
- RLS will automatically filter results to current user
- Example: `supabase.from('jobs').select('*')` returns only current user's jobs due to RLS
- Always use `.eq()` or other filters when querying specific records

## Testing
- Framework: Vitest + React Testing Library
- Run a single test: `npm test -- --grep "TestName"`
- Run with UI: `npm test:ui`
- Test files mirror source: /components/Button.tsx → /components/Button.test.tsx
- Always run tests after making changes

## Authentication & Database Security
- Row Level Security (RLS) policies in the database enforce that users can only access their own data
- `auth.uid()` in RLS policies checks the authenticated user from Supabase Auth
- Auth context is provided via `AuthProvider` wrapper in components/auth-context.tsx
- Always verify user is authenticated before making database queries (use `useAuth()` hook)

## Rules — Always Follow These
- Never commit directly to main
- Never hardcode credentials — always use environment variables
- Always handle errors explicitly — no silent failures
- Prefer explicit over clever — readable code beats compact code
- Respect RLS policies — don't bypass database security for convenience
- For database queries, assume RLS will enforce access control (don't re-check in code)


## Verification
- After code changes: run `npm run typecheck && npm test`
- After UI changes: take a screenshot and compare to requirements
- After database changes: verify with a test query
- When uncertain: ask rather than assume



<!-- 
DON'T ADD:
- Entire API Documentation
- OUtdated Code snippets
- Task Specific Instructions
- Hooks related stuff/instructions.
-->