# Local Environment Setup Guide

## Quick Start (Database Only)

### 1. Start PostgreSQL with Docker

```bash
docker-compose up -d
```

This starts a PostgreSQL container with:
- Database: `job_tracker`
- User: `dev`
- Password: `devpassword`
- Port: `5432`

The migrations in `supabase/migrations/` will run automatically.

### 2. Verify the database is running

```bash
docker-compose ps
```

### 3. Connect to the database (optional)

```bash
# Using psql
psql postgresql://dev:devpassword@localhost:5432/job_tracker

# Or using a GUI tool like DBeaver, pgAdmin, etc.
```

### 4. Run the app with Supabase Auth

Keep your existing `.env.local` with Supabase credentials and add the database URL:

```env
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

Then start the dev server:
```bash
npm run dev
```

---

## Full Local Setup (Database + Auth)

If you want a completely local development environment without Supabase:

### 1. Install dependencies for local auth

```bash
npm install bcryptjs next-auth
npm install --save-dev @types/bcryptjs
```

### 2. Update auth configuration

Create `lib/auth.ts` for local authentication (see FULL_LOCAL_AUTH.md).

### 3. Update environment variables

```env
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker
NEXTAUTH_SECRET=your-random-secret-key-min-32-chars
NEXTAUTH_URL=http://localhost:3000
```

### 4. Run migrations

Migrations run automatically when the Docker container starts.

---

## Database Management

### View database schema
```bash
docker-compose exec postgres psql -U dev -d job_tracker -c "\dt"
```

### Backup database
```bash
docker-compose exec postgres pg_dump -U dev job_tracker > backup.sql
```

### Restore database
```bash
docker-compose exec postgres psql -U dev job_tracker < backup.sql
```

### Stop database
```bash
docker-compose down
```

### Delete database (reset)
```bash
docker-compose down -v
docker-compose up -d
```

---

## Troubleshooting

### Port 5432 already in use
```bash
# Find process using port 5432
lsof -i :5432
# Kill it or use a different port in docker-compose.yml
```

### Migrations didn't run
```bash
# Manually run migrations
docker-compose exec postgres psql -U dev -d job_tracker -f /docker-entrypoint-initdb.d/001_initial_schema.sql
```

### Connection refused error
```bash
# Check if container is running
docker-compose ps

# View logs
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

---

## Next Steps

1. **For development with Supabase Auth:**
   - Keep using Supabase for authentication
   - Data will be stored in local PostgreSQL
   - Add `DATABASE_URL` to `.env.local`

2. **For fully local development:**
   - See FULL_LOCAL_AUTH.md for complete auth setup
   - This replaces Supabase entirely
