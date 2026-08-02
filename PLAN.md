# Project Implementation Plan: Job Application Tracker

## Executive Summary
Build a **Kanban-style job application tracker** as a full-stack Next.js 14 application with TypeScript, Tailwind CSS, and Supabase. The MVP will enable users to create accounts, manage job applications across 4 status columns (Applied → Interview → Offer → Rejected), perform CRUD operations, and drag jobs between columns. Full test coverage and type safety required.

**Timeline:** 7 sequential phases, each with clear deliverables and verification steps.

---

## Context & Constraints
- **Repository:** Greenfield (only CLAUDE.md exists, no code)
- **Tech Stack (from CLAUDE.md):** Next.js 14, TypeScript, Tailwind CSS, Supabase, React Context, Vitest + React Testing Library
- **Conventions:** PascalCase components, camelCase functions, kebab-case files, REST API routes
- **Rules:** Never commit to main, no hardcoded credentials, explicit error handling, readable > clever
- **Development:** `npm run dev` runs at localhost:3000

---

# PHASE 1: Project Setup & Tooling

## Goal
Initialize a production-ready Next.js 14 project with TypeScript, testing framework, and proper configuration.

## Detailed Steps

### 1.1 Initialize Next.js Project
```bash
npx create-next-app@latest . --typescript --tailwind --eslint --yes
```

**Options to select:**
- ✓ TypeScript
- ✓ Tailwind CSS
- ✓ ESLint
- ✓ App Router (default, must confirm)
- ✓ Use `@` for imports (recommended)

### 1.2 Update package.json
**Expected dependencies (will vary slightly based on create-next-app version):**

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "test:ui": "vitest --ui"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@supabase/supabase-js": "^2.38.0"
  },
  "devDependencies": {
    "typescript": "^5.2.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.50.0",
    "eslint-config-next": "^14.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/user-event": "^14.5.0",
    "vitest": "^0.34.0",
    "@vitest/ui": "^0.34.0",
    "@vitest/coverage-v8": "^0.34.0",
    "jsdom": "^22.1.0"
  }
}
```

**Post-install steps:**
```bash
npm install @supabase/supabase-js
npm install -D vitest @vitest/ui @vitest/coverage-v8 jsdom
```

### 1.3 Configure TypeScript
**File: `tsconfig.json`**
- Ensure `strict: true`
- Set `target: "ES2020"`
- Set `moduleResolution: "bundler"`
- Add path alias: `"@/*": ["./*"]` (Next.js handles this by default)

**Verification:**
```bash
npm run typecheck  # Should pass with no errors
```

### 1.4 Configure Vitest
**File: `vitest.config.ts`** (create new file)

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
})
```

**File: `vitest.setup.ts`** (create new file)

```typescript
import '@testing-library/jest-dom'
```

### 1.5 Create Directory Structure

```
claude-job-tracker/
├── app/
│   ├── layout.tsx
│   ├── page.tsx (landing/auth gate)
│   ├── api/
│   │   └── jobs/
│   │       ├── route.ts (POST, GET)
│   │       └── [id]/
│   │           └── route.ts (GET, PATCH, DELETE)
│   ├── auth/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── signup/
│   │   │   └── page.tsx
│   │   └── callback/
│   │       └── route.ts (OAuth callback, if needed later)
│   └── dashboard/
│       └── page.tsx (main app)
├── components/
│   ├── kanban-board.tsx
│   ├── job-card.tsx
│   ├── job-form.tsx
│   ├── header.tsx
│   ├── auth-context.tsx
│   ├── protected-route.tsx
│   └── __tests__/
│       ├── kanban-board.test.tsx
│       ├── job-card.test.tsx
│       ├── job-form.test.tsx
│       └── header.test.tsx
├── lib/
│   ├── supabase.ts (client initialization)
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useJobs.ts
│   │   └── useJob.ts
│   ├── context/
│   │   └── job-context.tsx
│   └── utils/
│       ├── date-formatter.ts
│       └── error-handler.ts
├── types/
│   ├── index.ts (main types)
│   └── supabase.ts (auto-generated)
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql
├── public/
│   └── favicon.ico (default)
├── styles/
│   └── globals.css (Tailwind imports)
├── .env.local.example
├── .gitignore (auto-generated, verify it includes .env.local)
├── tsconfig.json
├── next.config.js
├── tailwind.config.ts
├── vitest.config.ts
├── vitest.setup.ts
├── package.json
├── package-lock.json
├── CLAUDE.md (existing)
└── PLAN.md (this file)
```

### 1.6 Configure Tailwind
**File: `tailwind.config.ts`** (already set up by create-next-app, verify)

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        status: {
          applied: '#3b82f6',    // blue
          interview: '#f59e0b',   // amber
          offer: '#10b981',       // emerald
          rejected: '#ef4444',    // red
        },
      },
    },
  },
  plugins: [],
}
export default config
```

### 1.7 Set Up Global Styles
**File: `app/globals.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition;
  }
  .btn-secondary {
    @apply px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition;
  }
  .card {
    @apply bg-white border border-gray-200 rounded-lg shadow-sm;
  }
}
```

### 1.8 Create Environment Template
**File: `.env.local.example`**

```env
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

**Add to `.gitignore`:**
```
.env.local
.env.local.backup
```

### 1.9 Verify Phase 1
```bash
npm run dev        # Should start on localhost:3000 with Next.js default page
npm run typecheck  # Should pass with no errors
npm run lint       # Should pass (might have some default warnings)
npm test           # Should pass with 0 tests (no tests yet)
```

---

# PHASE 2: Database Schema & Supabase Setup

## Goal
Design and configure the Supabase backend with user management and job tracking schema.

## Detailed Steps

### 2.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create new project (or use existing)
3. Copy **Project URL** and **Anon Key**
4. Paste into `.env.local`:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
   ```

### 2.2 Create Database Migrations
**File: `supabase/migrations/001_initial_schema.sql`**

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (Supabase Auth manages this, but we can extend it)
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  company TEXT NOT NULL,
  position TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'applied' CHECK (status IN ('applied', 'interview', 'offer', 'rejected')),
  notes TEXT,
  applied_date DATE NOT NULL DEFAULT CURRENT_DATE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, company, position) -- Prevent exact duplicates
);

-- Indexes for common queries
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);

-- Enable RLS (Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
CREATE POLICY "Users can read own data" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (auth.uid() = id);

-- RLS Policies for jobs table
CREATE POLICY "Users can read own jobs" ON jobs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create jobs" ON jobs
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own jobs" ON jobs
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own jobs" ON jobs
  FOR DELETE USING (auth.uid() = user_id);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_jobs_updated_at
BEFORE UPDATE ON jobs
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();
```

**Manual steps in Supabase Dashboard:**
1. Go to **SQL Editor**
2. Paste and execute the migration
3. Verify tables and policies are created

**Alternative: Use Supabase CLI**
```bash
npm install -g supabase
supabase init
supabase migration new initial_schema
# (paste migration into new file)
supabase db push
```

### 2.3 Generate TypeScript Types
**File: `types/supabase.ts`** (auto-generated from Supabase schema)

```bash
# Using Supabase CLI
supabase gen types typescript --project-id your-project-id > types/supabase.ts
```

**Or manually create from schema:**

```typescript
// types/supabase.ts
export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json }
  | Json[]

export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          email: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          email?: string
          created_at?: string
          updated_at?: string
        }
      }
      jobs: {
        Row: {
          id: string
          user_id: string
          company: string
          position: string
          status: 'applied' | 'interview' | 'offer' | 'rejected'
          notes: string | null
          applied_date: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          company: string
          position: string
          status?: 'applied' | 'interview' | 'offer' | 'rejected'
          notes?: string | null
          applied_date?: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          company?: string
          position?: string
          status?: 'applied' | 'interview' | 'offer' | 'rejected'
          notes?: string | null
          applied_date?: string
          created_at?: string
          updated_at?: string
        }
      }
    }
    Views: {}
    Functions: {}
    Enums: {}
  }
}
```

### 2.4 Create Supabase Client
**File: `lib/supabase.ts`**

```typescript
import { createClient } from '@supabase/supabase-js'
import type { Database } from '@/types/supabase'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey)
```

### 2.5 Create Base Types
**File: `types/index.ts`**

```typescript
export type JobStatus = 'applied' | 'interview' | 'offer' | 'rejected'

export interface Job {
  id: string
  user_id: string
  company: string
  position: string
  status: JobStatus
  notes: string | null
  applied_date: string
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  email: string
  created_at: string
  updated_at: string
}

export interface AuthUser {
  id: string
  email?: string
}
```

### 2.6 Verify Phase 2
- [ ] Supabase project created and API keys copied
- [ ] Tables created in Supabase (check SQL Editor)
- [ ] RLS policies enabled and visible
- [ ] `.env.local` has correct API keys
- [ ] `types/supabase.ts` generated or created
- [ ] `lib/supabase.ts` imports without errors
- [ ] Run `npm run typecheck` — should pass

---

# PHASE 3: Authentication

## Goal
Implement secure user signup, login, and session management with Supabase Auth.

## Detailed Steps

### 3.1 Create Auth Context
**File: `components/auth-context.tsx`**

```typescript
'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import type { AuthUser } from '@/types'

interface AuthContextType {
  user: AuthUser | null
  loading: boolean
  error: string | null
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Check initial session
    const getSession = async () => {
      const { data, error: err } = await supabase.auth.getSession()
      if (err) {
        setError(err.message)
      } else if (data.session) {
        setUser({
          id: data.session.user.id,
          email: data.session.user.email,
        })
      }
      setLoading(false)
    }

    getSession()

    // Subscribe to auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session?.user) {
        setUser({
          id: session.user.id,
          email: session.user.email,
        })
      } else {
        setUser(null)
      }
    })

    return () => subscription?.unsubscribe()
  }, [])

  const logout = async () => {
    const { error: err } = await supabase.auth.signOut()
    if (err) {
      setError(err.message)
    } else {
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, error, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### 3.2 Create useAuth Hook
**File: `lib/hooks/useAuth.ts`**

```typescript
import { useContext } from 'react'
import { AuthContext } from '@/components/auth-context'

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### 3.3 Create Login Page
**File: `app/auth/login/page.tsx`**

```typescript
'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const { error: err } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (err) {
      setError(err.message)
      setLoading(false)
    } else {
      router.push('/dashboard')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-6">Login</h1>
        
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-800 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <Link href="/auth/signup" className="text-blue-600 hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}
```

### 3.4 Create Signup Page
**File: `app/auth/signup/page.tsx`**

```typescript
'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    setLoading(true)

    const { error: err } = await supabase.auth.signUp({
      email,
      password,
    })

    if (err) {
      setError(err.message)
      setLoading(false)
    } else {
      router.push('/auth/login?message=Check+your+email+to+verify+your+account')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-6">Sign Up</h1>
        
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-800 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSignup} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/auth/login" className="text-blue-600 hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  )
}
```

### 3.5 Create Protected Route Component
**File: `components/protected-route.tsx`**

```typescript
'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/auth/login')
    }
  }, [user, loading, router])

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  if (!user) {
    return null
  }

  return <>{children}</>
}
```

### 3.6 Update Root Layout
**File: `app/layout.tsx`**

```typescript
import type { Metadata } from 'next'
import { AuthProvider } from '@/components/auth-context'
import './globals.css'

export const metadata: Metadata = {
  title: 'Job Application Tracker',
  description: 'Track your job applications with ease',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
```

### 3.7 Verify Phase 3
- [ ] Navigate to `/auth/signup` — form loads
- [ ] Create account with valid email/password
- [ ] Verify email confirmation (check Supabase dashboard)
- [ ] Navigate to `/auth/login` — form loads
- [ ] Login with created account
- [ ] Session persists on page reload
- [ ] Protected pages redirect to login when unauthenticated
- [ ] `npm run typecheck` passes

---

# PHASE 4: Core UI Components

## Goal
Build reusable, well-tested UI components for the Kanban board.

### 4.1 Create Header Component
**File: `components/header.tsx`**

```typescript
'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import { useRouter } from 'next/navigation'

export function Header() {
  const { user, logout } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    await logout()
    router.push('/auth/login')
  }

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">Job Tracker</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">{user?.email}</span>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}
```

### 4.2 Create Job Card Component
**File: `components/job-card.tsx`**

```typescript
'use client'

import { Job, JobStatus } from '@/types'
import { useState } from 'react'
import { JobForm } from './job-form'

const statusColors: Record<JobStatus, string> = {
  applied: 'bg-blue-50 border-blue-200',
  interview: 'bg-amber-50 border-amber-200',
  offer: 'bg-emerald-50 border-emerald-200',
  rejected: 'bg-red-50 border-red-200',
}

interface JobCardProps {
  job: Job
  onEdit: (job: Job) => void
  onDelete: (jobId: string) => void
  onDragStart: (e: React.DragEvent, job: Job) => void
}

export function JobCard({ job, onEdit, onDelete, onDragStart }: JobCardProps) {
  const [showEditForm, setShowEditForm] = useState(false)

  const handleDelete = () => {
    if (window.confirm(`Delete "${job.company}" - "${job.position}"?`)) {
      onDelete(job.id)
    }
  }

  if (showEditForm) {
    return (
      <JobForm
        initialJob={job}
        onSubmit={(updated) => {
          onEdit(updated)
          setShowEditForm(false)
        }}
        onCancel={() => setShowEditForm(false)}
      />
    )
  }

  return (
    <div
      draggable
      onDragStart={(e) => onDragStart(e, job)}
      className={`card p-4 cursor-move hover:shadow-md transition ${statusColors[job.status]} border-l-4`}
    >
      <h3 className="font-semibold text-gray-900">{job.company}</h3>
      <p className="text-sm text-gray-600">{job.position}</p>
      <p className="text-xs text-gray-500 mt-2">Applied: {new Date(job.applied_date).toLocaleDateString()}</p>
      
      {job.notes && (
        <p className="text-sm text-gray-700 mt-2 italic">"{job.notes}"</p>
      )}

      <div className="mt-4 flex gap-2">
        <button
          onClick={() => setShowEditForm(true)}
          className="flex-1 px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-100 rounded"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="flex-1 px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-100 rounded"
        >
          Delete
        </button>
      </div>
    </div>
  )
}
```

### 4.3 Create Job Form Component
**File: `components/job-form.tsx`**

```typescript
'use client'

import { Job, JobStatus } from '@/types'
import { useState } from 'react'

interface JobFormProps {
  initialJob?: Job
  onSubmit: (job: Partial<Job>) => void
  onCancel: () => void
}

export function JobForm({ initialJob, onSubmit, onCancel }: JobFormProps) {
  const [company, setCompany] = useState(initialJob?.company || '')
  const [position, setPosition] = useState(initialJob?.position || '')
  const [status, setStatus] = useState<JobStatus>(initialJob?.status || 'applied')
  const [appliedDate, setAppliedDate] = useState(
    initialJob?.applied_date || new Date().toISOString().split('T')[0]
  )
  const [notes, setNotes] = useState(initialJob?.notes || '')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      company,
      position,
      status,
      applied_date: appliedDate,
      notes: notes || null,
    })
  }

  return (
    <div className="card p-6 max-w-md">
      <h2 className="text-lg font-bold mb-4">
        {initialJob ? 'Edit Job' : 'Add New Job'}
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Company</label>
          <input
            type="text"
            required
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Position</label>
          <input
            type="text"
            required
            value={position}
            onChange={(e) => setPosition(e.target.value)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Status</label>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value as JobStatus)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="applied">Applied</option>
            <option value="interview">Interview</option>
            <option value="offer">Offer</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Applied Date</label>
          <input
            type="date"
            required
            value={appliedDate}
            onChange={(e) => setAppliedDate(e.target.value)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Notes</label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows={3}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="flex gap-2">
          <button
            type="submit"
            className="btn-primary flex-1"
          >
            {initialJob ? 'Update' : 'Create'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="btn-secondary flex-1"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
```

### 4.4 Create Kanban Board Component
**File: `components/kanban-board.tsx`**

```typescript
'use client'

import { Job, JobStatus } from '@/types'
import { useState } from 'react'
import { JobCard } from './job-card'
import { JobForm } from './job-form'

const statusGroups: JobStatus[] = ['applied', 'interview', 'offer', 'rejected']
const statusLabels: Record<JobStatus, string> = {
  applied: 'Applied',
  interview: 'Interview',
  offer: 'Offer',
  rejected: 'Rejected',
}

interface KanbanBoardProps {
  jobs: Job[]
  onCreateJob: (job: Omit<Job, 'id' | 'created_at' | 'updated_at' | 'user_id'>) => void
  onUpdateJob: (job: Job) => void
  onDeleteJob: (jobId: string) => void
}

export function KanbanBoard({
  jobs,
  onCreateJob,
  onUpdateJob,
  onDeleteJob,
}: KanbanBoardProps) {
  const [draggedJob, setDraggedJob] = useState<Job | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)

  const handleDragStart = (e: React.DragEvent, job: Job) => {
    setDraggedJob(job)
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleDrop = (e: React.DragEvent, status: JobStatus) => {
    e.preventDefault()
    if (draggedJob && draggedJob.status !== status) {
      onUpdateJob({
        ...draggedJob,
        status,
      })
    }
    setDraggedJob(null)
  }

  const getJobsByStatus = (status: JobStatus) =>
    jobs.filter((job) => job.status === status)

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">Job Applications</h2>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary"
          >
            + Add Job
          </button>
        </div>

        {showAddForm && (
          <div className="mb-6">
            <JobForm
              onSubmit={(job) => {
                onCreateJob(job as Omit<Job, 'id' | 'created_at' | 'updated_at' | 'user_id'>)
                setShowAddForm(false)
              }}
              onCancel={() => setShowAddForm(false)}
            />
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {statusGroups.map((status) => (
            <div
              key={status}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, status)}
              className="bg-white rounded-lg shadow-sm p-4 min-h-96 border-t-4 border-gray-300"
            >
              <h3 className="font-bold text-gray-900 mb-4">
                {statusLabels[status]}
              </h3>
              <div className="space-y-3">
                {getJobsByStatus(status).map((job) => (
                  <JobCard
                    key={job.id}
                    job={job}
                    onEdit={onUpdateJob}
                    onDelete={onDeleteJob}
                    onDragStart={handleDragStart}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

### 4.5 Create Component Tests (Example)
**File: `components/__tests__/job-card.test.tsx`**

```typescript
import { render, screen } from '@testing-library/react'
import { JobCard } from '../job-card'
import { Job } from '@/types'

describe('JobCard', () => {
  const mockJob: Job = {
    id: '1',
    user_id: 'user-1',
    company: 'Acme Corp',
    position: 'Senior Engineer',
    status: 'applied',
    notes: 'Great company',
    applied_date: '2024-01-15',
    created_at: '2024-01-15T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  }

  it('renders job card with company and position', () => {
    render(
      <JobCard
        job={mockJob}
        onEdit={() => {}}
        onDelete={() => {}}
        onDragStart={() => {}}
      />
    )
    
    expect(screen.getByText('Acme Corp')).toBeInTheDocument()
    expect(screen.getByText('Senior Engineer')).toBeInTheDocument()
  })

  it('renders edit and delete buttons', () => {
    render(
      <JobCard
        job={mockJob}
        onEdit={() => {}}
        onDelete={() => {}}
        onDragStart={() => {}}
      />
    )
    
    expect(screen.getByText('Edit')).toBeInTheDocument()
    expect(screen.getByText('Delete')).toBeInTheDocument()
  })
})
```

### 4.6 Verify Phase 4
- [ ] Components render without errors
- [ ] Forms capture input correctly
- [ ] Kanban board displays all 4 columns
- [ ] Component tests pass: `npm test components`
- [ ] `npm run typecheck` passes
- [ ] No console errors

---

# PHASE 5: API Routes (CRUD)

## Goal
Implement secure RESTful API endpoints for job CRUD operations.

### 5.1 Create POST /api/jobs (Create)
**File: `app/api/jobs/route.ts`**

```typescript
import { supabase } from '@/lib/supabase'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const session = await supabase.auth.getSession()
    if (!session.data.session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const userId = session.data.session.user.id
    const { company, position, status = 'applied', applied_date, notes } = await req.json()

    if (!company || !position) {
      return NextResponse.json(
        { error: 'Company and position are required' },
        { status: 400 }
      )
    }

    const { data, error } = await supabase
      .from('jobs')
      .insert([
        {
          user_id: userId,
          company,
          position,
          status,
          applied_date: applied_date || new Date().toISOString().split('T')[0],
          notes,
        },
      ])
      .select()

    if (error) {
      return NextResponse.json(
        { error: error.message },
        { status: 400 }
      )
    }

    return NextResponse.json(data[0], { status: 201 })
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function GET(req: NextRequest) {
  try {
    const session = await supabase.auth.getSession()
    if (!session.data.session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const userId = session.data.session.user.id

    const { data, error } = await supabase
      .from('jobs')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })

    if (error) {
      return NextResponse.json(
        { error: error.message },
        { status: 400 }
      )
    }

    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### 5.2 Create GET/PATCH/DELETE /api/jobs/[id]
**File: `app/api/jobs/[id]/route.ts`**

```typescript
import { supabase } from '@/lib/supabase'
import { NextRequest, NextResponse } from 'next/server'

async function getAuthUserId(req: NextRequest) {
  const session = await supabase.auth.getSession()
  const userId = session.data.session?.user?.id
  if (!userId) {
    throw new Error('Unauthorized')
  }
  return userId
}

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const userId = await getAuthUserId(req)

    const { data, error } = await supabase
      .from('jobs')
      .select('*')
      .eq('id', params.id)
      .eq('user_id', userId)
      .single()

    if (error || !data) {
      return NextResponse.json(
        { error: 'Job not found' },
        { status: 404 }
      )
    }

    return NextResponse.json(data)
  } catch (error) {
    if ((error as Error).message === 'Unauthorized') {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function PATCH(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const userId = await getAuthUserId(req)

    // Verify job belongs to user
    const { data: existingJob, error: fetchError } = await supabase
      .from('jobs')
      .select('user_id')
      .eq('id', params.id)
      .single()

    if (fetchError || !existingJob || existingJob.user_id !== userId) {
      return NextResponse.json(
        { error: 'Job not found or unauthorized' },
        { status: 404 }
      )
    }

    const updates = await req.json()

    const { data, error } = await supabase
      .from('jobs')
      .update(updates)
      .eq('id', params.id)
      .select()

    if (error) {
      return NextResponse.json(
        { error: error.message },
        { status: 400 }
      )
    }

    return NextResponse.json(data[0])
  } catch (error) {
    if ((error as Error).message === 'Unauthorized') {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const userId = await getAuthUserId(req)

    // Verify job belongs to user
    const { data: existingJob, error: fetchError } = await supabase
      .from('jobs')
      .select('user_id')
      .eq('id', params.id)
      .single()

    if (fetchError || !existingJob || existingJob.user_id !== userId) {
      return NextResponse.json(
        { error: 'Job not found or unauthorized' },
        { status: 404 }
      )
    }

    const { error } = await supabase
      .from('jobs')
      .delete()
      .eq('id', params.id)

    if (error) {
      return NextResponse.json(
        { error: error.message },
        { status: 400 }
      )
    }

    return NextResponse.json({ success: true }, { status: 204 })
  } catch (error) {
    if ((error as Error).message === 'Unauthorized') {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### 5.3 Verify Phase 5
- [ ] POST /api/jobs creates a job
- [ ] GET /api/jobs retrieves user's jobs
- [ ] GET /api/jobs/[id] retrieves single job
- [ ] PATCH /api/jobs/[id] updates job
- [ ] DELETE /api/jobs/[id] deletes job
- [ ] Unauthorized requests return 401
- [ ] API validates required fields

---

# PHASE 6: State Management & Data Fetching

## Goal
Implement React Context for global job state and custom hooks for data operations.

### 6.1 Create Job Context
**File: `lib/context/job-context.tsx`**

```typescript
'use client'

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { Job } from '@/types'

interface JobContextType {
  jobs: Job[]
  loading: boolean
  error: string | null
  createJob: (job: Omit<Job, 'id' | 'created_at' | 'updated_at' | 'user_id'>) => Promise<void>
  updateJob: (job: Job) => Promise<void>
  deleteJob: (jobId: string) => Promise<void>
  fetchJobs: () => Promise<void>
}

const JobContext = createContext<JobContextType | undefined>(undefined)

export function JobProvider({ children }: { children: React.ReactNode }) {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchJobs = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/jobs')
      if (!res.ok) throw new Error('Failed to fetch jobs')
      const data = await res.json()
      setJobs(data)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }, [])

  const createJob = useCallback(async (job) => {
    setError(null)
    try {
      const res = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(job),
      })
      if (!res.ok) throw new Error('Failed to create job')
      const newJob = await res.json()
      setJobs((prev) => [newJob, ...prev])
    } catch (err) {
      setError((err as Error).message)
      throw err
    }
  }, [])

  const updateJob = useCallback(async (job) => {
    setError(null)
    try {
      const res = await fetch(`/api/jobs/${job.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(job),
      })
      if (!res.ok) throw new Error('Failed to update job')
      const updated = await res.json()
      setJobs((prev) => prev.map((j) => (j.id === job.id ? updated : j)))
    } catch (err) {
      setError((err as Error).message)
      throw err
    }
  }, [])

  const deleteJob = useCallback(async (jobId) => {
    setError(null)
    try {
      const res = await fetch(`/api/jobs/${jobId}`, {
        method: 'DELETE',
      })
      if (!res.ok) throw new Error('Failed to delete job')
      setJobs((prev) => prev.filter((j) => j.id !== jobId))
    } catch (err) {
      setError((err as Error).message)
      throw err
    }
  }, [])

  useEffect(() => {
    fetchJobs()
  }, [fetchJobs])

  return (
    <JobContext.Provider
      value={{
        jobs,
        loading,
        error,
        createJob,
        updateJob,
        deleteJob,
        fetchJobs,
      }}
    >
      {children}
    </JobContext.Provider>
  )
}

export function useJobs() {
  const context = useContext(JobContext)
  if (!context) {
    throw new Error('useJobs must be used within JobProvider')
  }
  return context
}
```

### 6.2 Create Dashboard Page
**File: `app/dashboard/page.tsx`**

```typescript
'use client'

import { ProtectedRoute } from '@/components/protected-route'
import { Header } from '@/components/header'
import { KanbanBoard } from '@/components/kanban-board'
import { useJobs } from '@/lib/context/job-context'

export default function DashboardPage() {
  const { jobs, createJob, updateJob, deleteJob } = useJobs()

  return (
    <ProtectedRoute>
      <Header />
      <KanbanBoard
        jobs={jobs}
        onCreateJob={createJob}
        onUpdateJob={updateJob}
        onDeleteJob={deleteJob}
      />
    </ProtectedRoute>
  )
}
```

### 6.3 Update Root Layout to Include JobProvider
**File: `app/layout.tsx` (Updated)**

```typescript
import type { Metadata } from 'next'
import { AuthProvider } from '@/components/auth-context'
import { JobProvider } from '@/lib/context/job-context'
import './globals.css'

export const metadata: Metadata = {
  title: 'Job Application Tracker',
  description: 'Track your job applications with ease',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <JobProvider>
            {children}
          </JobProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
```

### 6.4 Create Root Page (Landing)
**File: `app/page.tsx`**

```typescript
'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import Link from 'next/link'

export default function LandingPage() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && user) {
      router.push('/dashboard')
    }
  }, [user, loading, router])

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  if (user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Job Application Tracker
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Organize and track your job applications effortlessly
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/auth/login"
            className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700"
          >
            Login
          </Link>
          <Link
            href="/auth/signup"
            className="px-6 py-3 bg-white border border-blue-600 text-blue-600 font-semibold rounded-lg hover:bg-blue-50"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  )
}
```

### 6.5 Verify Phase 6
- [ ] Landing page shows for unauthenticated users
- [ ] Dashboard auto-fetches jobs on load
- [ ] Jobs display in Kanban board
- [ ] Create job adds to board immediately (optimistic update)
- [ ] Update job (drag between columns) syncs to Supabase
- [ ] Delete job removes from board
- [ ] Page refresh persists data from Supabase
- [ ] `npm run typecheck` passes

---

# PHASE 7: Integration & Testing

## Goal
Complete test coverage and end-to-end verification.

### 7.1 Add Integration Tests
**File: `app/api/jobs/__tests__/route.test.ts`**

```typescript
import { describe, it, expect, vi } from 'vitest'

// Mock Supabase
vi.mock('@/lib/supabase', () => ({
  supabase: {
    auth: {
      getSession: vi.fn(),
    },
    from: vi.fn(),
  },
}))

describe('POST /api/jobs', () => {
  it('should create a job with valid data', async () => {
    // Test implementation
  })

  it('should reject unauthenticated requests', async () => {
    // Test implementation
  })
})
```

### 7.2 Run Full Test Suite
```bash
npm test                    # Run all tests
npm run typecheck          # Type check
npm run lint               # Lint
npm run build              # Build test (verifies Next.js build works)
```

### 7.3 Manual End-to-End Verification

**Test Flow:**

1. **Start dev server:**
   ```bash
   npm run dev
   ```

2. **Navigate to localhost:3000:**
   - Should show landing page with Login/Sign Up buttons

3. **Sign up:**
   - Click "Sign Up", enter email/password
   - Should redirect to login with success message
   - Check Supabase Auth dashboard for new user

4. **Log in:**
   - Enter credentials
   - Should redirect to dashboard

5. **Create job:**
   - Click "+ Add Job"
   - Fill form: Company="TechCorp", Position="Engineer", Date=today, Notes="Interesting role"
   - Click Create
   - Job appears in "Applied" column

6. **Move job between columns:**
   - Drag job from "Applied" to "Interview"
   - Status updates immediately
   - Refresh page—job stays in "Interview" column

7. **Edit job:**
   - Click "Edit" on card
   - Change notes
   - Click Update
   - Card reflects changes

8. **Delete job:**
   - Click "Delete" on card
   - Confirm deletion
   - Job removed from board

9. **Logout:**
   - Click "Logout" button
   - Redirected to landing page

10. **Return to dashboard:**
    - Try to navigate to /dashboard directly
    - Should redirect to login

### 7.4 Verification Checklist

- [ ] All scripts run successfully
  - [ ] `npm run dev` starts at localhost:3000
  - [ ] `npm run build` completes without errors
  - [ ] `npm test` passes all tests
  - [ ] `npm run typecheck` passes
  - [ ] `npm run lint` passes (or only minor warnings)

- [ ] Auth flows work
  - [ ] Sign up creates account
  - [ ] Login with correct credentials succeeds
  - [ ] Login with wrong credentials fails
  - [ ] Logout clears session
  - [ ] Protected routes redirect to login

- [ ] Job CRUD operations work
  - [ ] Create: New job appears in correct column
  - [ ] Read: Jobs persist on page reload
  - [ ] Update: Drag-drop changes status, form edits work
  - [ ] Delete: Job removed from board and DB

- [ ] Drag-drop functionality
  - [ ] Jobs are draggable between columns
  - [ ] Status updates in Supabase on drop
  - [ ] Visual feedback during drag

- [ ] Error handling
  - [ ] Network errors show error messages
  - [ ] Invalid inputs rejected
  - [ ] Unauthorized requests blocked

- [ ] Type safety
  - [ ] No `any` types used
  - [ ] TypeScript strict mode enabled
  - [ ] All APIs properly typed

- [ ] Performance
  - [ ] No console errors or warnings
  - [ ] Pages load quickly
  - [ ] No unnecessary re-renders

---

# Deployment Preparation (After MVP)

Once MVP is verified, prepare for production:

1. **Environment variables:**
   - Set `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` in deployment platform (Vercel, etc.)

2. **Database backups:**
   - Enable automated backups in Supabase

3. **Security audit:**
   - Review RLS policies
   - Ensure no secrets in code
   - Verify HTTPS enforcement

4. **Performance optimization:**
   - Add image optimization
   - Code splitting for large components
   - Lazy loading for routes

---

# Quick Reference: Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Production build
npm start            # Start production server

# Quality
npm run typecheck    # TypeScript type check
npm run lint         # ESLint
npm test             # Run all tests
npm test -- --watch  # Watch mode

# Database
supabase migration new <name>    # Create migration
supabase db push                 # Apply migrations
supabase gen types typescript    # Generate types
```

---

# Architecture Summary

```
┌─────────────────────────────────────────┐
│         Next.js 14 Frontend              │
│  (React Components, Tailwind CSS)        │
├─────────────────────────────────────────┤
│  React Context (Auth + Job State)        │
├─────────────────────────────────────────┤
│  Next.js API Routes (/api/jobs)          │
├─────────────────────────────────────────┤
│  Supabase Auth + PostgreSQL Database     │
│  (Users, Jobs, RLS Policies)             │
└─────────────────────────────────────────┘
```

---

# Critical Success Factors

1. **Type Safety:** Strict TypeScript throughout
2. **Error Handling:** Explicit errors, no silent failures
3. **Security:** RLS policies + auth checks on every API route
4. **Testing:** Tests pass, 70%+ coverage by end of Phase 7
5. **User Experience:** Optimistic updates, clear feedback
6. **Code Quality:** No hardcoded values, readable > clever, conventions followed
