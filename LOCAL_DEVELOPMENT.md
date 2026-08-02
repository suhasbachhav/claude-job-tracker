# Local Development Setup

Your job tracker app is now ready for local development with a local database. Choose your setup method below.

## 🚀 Quick Start (Recommended for macOS)

Follow **MACOS_QUICK_START.md** for step-by-step instructions to:
1. Install Homebrew (if needed)
2. Install PostgreSQL 16
3. Create local database
4. Run migrations
5. Start developing

**Time needed:** 10-15 minutes  
**Prerequisites:** Administrator access on macOS

---

## 📋 Setup Options

See **SETUP_OPTIONS.md** for all available methods:

| Method | Setup Time | Best For | Requirements |
|--------|-----------|----------|--------------|
| **Docker** | 5 min | Production-like environment | Docker Desktop |
| **macOS (Homebrew)** | 10 min | Native macOS setup | Homebrew, admin access |
| **Local PostgreSQL** | 15 min | Any OS with PostgreSQL | PostgreSQL installed |
| **SQLite** | 2 min | Zero dependencies | Node.js only |
| **Supabase Local** | 10 min | Exact production setup | Docker + Supabase CLI |

---

## 🔧 What's Been Created

### Files Added
- **`.env.local`** — Environment variables (already filled with defaults)
- **`docker-compose.yml`** — Docker configuration for PostgreSQL
- **`setup-local-db.sh`** — Automated setup script (macOS)
- **`MACOS_QUICK_START.md`** — Step-by-step macOS guide
- **`SETUP_OPTIONS.md`** — All setup methods explained
- **`LOCAL_AUTH_SETUP.md`** — Database + Supabase Auth setup
- **`FULL_LOCAL_AUTH.md`** — Database + NextAuth (no Supabase) setup

### Existing Structure Used
- **`supabase/migrations/001_initial_schema.sql`** — Database schema
  - Creates `users` table
  - Creates `jobs` table with relationships
  - Sets up indexes and triggers

---

## ✅ Current Architecture

```
Job Tracker App
├── Frontend (Next.js 14 + React 19)
├── Authentication: Supabase Auth (or NextAuth for full local)
├── Database: PostgreSQL (local)
└── API: Next.js API routes
```

### What Works Now
✓ Local PostgreSQL database  
✓ Database schema ready  
✓ Supabase Auth connected (keep credentials in `.env.local`)  
✓ Development environment configured  

### What You Need To Do
1. Set up PostgreSQL locally (pick your method)
2. Start the dev server: `npm run dev`
3. Visit http://localhost:3000

---

## 🎯 Recommended Path

### For Quick Development
1. **Follow MACOS_QUICK_START.md** (if on macOS)
2. Update `.env.local` with Supabase credentials
3. Run `npm run dev`
4. Done! Use the app with local DB + Supabase Auth

### For Full Local Setup (No Supabase)
1. Follow MACOS_QUICK_START.md to set up PostgreSQL
2. Install NextAuth: `npm install next-auth bcryptjs`
3. Follow FULL_LOCAL_AUTH.md for auth configuration
4. Update authentication pages to use NextAuth
5. Remove Supabase from dependencies (optional)

### For Docker Users
1. Install Docker Desktop
2. Run: `docker compose up -d`
3. Done! PostgreSQL running with migrations applied

---

## 🗄️ Database Connection

**Local PostgreSQL:**
```
URL: postgresql://dev:devpassword@localhost:5432/job_tracker
Host: localhost
Port: 5432
Database: job_tracker
User: dev
Password: devpassword
```

Use this in `.env.local`:
```env
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker
```

---

## 📝 Environment Variables

Your `.env.local` file:

```env
# Required: Local Database Connection
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker

# Optional: Supabase Authentication
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

To get Supabase credentials:
1. Go to https://app.supabase.com
2. Create a project or use existing one
3. Get URL from Project Settings → General
4. Get anon key from Project Settings → API

---

## 🚀 Running the App

### Start Development Server
```bash
npm run dev
```

### Run Tests
```bash
npm test
```

### Type Check
```bash
npm run typecheck
```

### Build for Production
```bash
npm run build
npm start
```

---

## 🗺️ Database Management

### Connect with psql
```bash
psql -U dev -d job_tracker
```

### View Tables
```bash
psql -U dev -d job_tracker -c "\dt"
```

### View Jobs
```bash
psql -U dev -d job_tracker -c "SELECT * FROM jobs;"
```

### Backup Database
```bash
pg_dump -U dev job_tracker > backup.sql
```

### Reset Database
```bash
# Stop PostgreSQL
brew services stop postgresql@16

# Delete old data
dropdb -U postgres job_tracker

# Recreate and migrate
psql -U postgres -c "CREATE DATABASE job_tracker OWNER dev;"
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql

# Start PostgreSQL
brew services start postgresql@16
```

---

## 🔗 Related Files

- [CLAUDE.md](CLAUDE.md) — Project structure and conventions
- [PLAN.md](PLAN.md) — Development plan and architecture
- [AGENTS.md](AGENTS.md) — Claude Code agents setup
- [README.md](README.md) — Project overview

---

## ❓ Troubleshooting

**"Port 5432 already in use"**
```bash
lsof -i :5432
# Kill the process or change port in setup
```

**"Connection refused"**
- Check PostgreSQL is running: `brew services list | grep postgresql`
- Check database credentials in `.env.local`
- Check `.env.local` has correct `DATABASE_URL`

**"Tables not created"**
- Run migrations manually: `psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql`

**"Supabase auth not working"**
- Verify credentials in `.env.local`
- Check NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY are set
- Go to Supabase dashboard and create a project if needed

---

## 📚 Next Steps

1. **Choose your setup method** (MACOS_QUICK_START.md or SETUP_OPTIONS.md)
2. **Install database** locally
3. **Update `.env.local`** with Supabase credentials
4. **Run `npm run dev`**
5. **Visit http://localhost:3000**
6. **Start developing!**

Questions? Check MACOS_QUICK_START.md or SETUP_OPTIONS.md for your OS/method.

Happy coding! 🎉
