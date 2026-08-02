# Local Database Setup Options

## Option 1: Docker (Recommended) ⭐

**Best for: Production-like local environment**

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Or install [Docker Engine](https://docs.docker.com/engine/install/) + [Docker Compose](https://docs.docker.com/compose/install/)

### Setup
```bash
docker compose up -d
```

This automatically:
- Starts PostgreSQL 16
- Creates the `job_tracker` database
- Runs migrations from `supabase/migrations/`
- Exposes port 5432

### Connection
```
postgresql://dev:devpassword@localhost:5432/job_tracker
```

---

## Option 2: Local PostgreSQL Installation

**Best for: Native installation without Docker**

### macOS (using Homebrew)
```bash
# Install PostgreSQL
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Create database and user
createuser -P dev  # password: devpassword
createdb -U dev job_tracker

# Run migrations
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql
```

### Ubuntu/Debian
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Switch to postgres user
sudo -u postgres psql

# In psql:
CREATE USER dev WITH PASSWORD 'devpassword';
CREATE DATABASE job_tracker OWNER dev;
GRANT ALL PRIVILEGES ON DATABASE job_tracker TO dev;
\q

# Run migrations
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql
```

### Windows (using PostgreSQL installer)
1. Download from https://www.postgresql.org/download/windows/
2. Run installer, choose password `devpassword` for postgres user
3. Open PostgreSQL Shell and run:
```sql
CREATE USER dev WITH PASSWORD 'devpassword';
CREATE DATABASE job_tracker OWNER dev;
GRANT ALL PRIVILEGES ON DATABASE job_tracker TO dev;
```
4. Run migrations via SQL shell:
```sql
\c job_tracker dev
\i 'C:/path/to/supabase/migrations/001_initial_schema.sql'
```

### Connection
```
postgresql://dev:devpassword@localhost:5432/job_tracker
```

---

## Option 3: SQLite (Easiest Local Dev)

**Best for: Simplest local development, no external dependencies**

### Setup

1. **Install better-sqlite3**
```bash
npm install better-sqlite3 drizzle-orm
npm install --save-dev drizzle-kit
```

2. **Create `lib/db-local.ts`** (see SQLite setup below)

3. **Update your database access layer**
   - Create API routes that use the local DB
   - Or refactor components to use server actions

### Pros
- Zero external dependencies
- File-based (`.db` file in project)
- Fast for local dev
- Easy to reset: just delete the file

### Cons
- SQLite is single-process (not suitable for production)
- Some SQL features not available
- Limited concurrent access

---

## Option 4: Use Supabase Locally (Advanced)

**Best for: Exact production setup locally**

### Prerequisites
- Install [Supabase CLI](https://supabase.com/docs/guides/local-development/cli/getting-started)
- Docker (for running Supabase services)

### Setup
```bash
supabase init
supabase start
```

This starts a local Supabase instance with:
- PostgreSQL
- Auth system
- REST API
- Studio UI

Then connect to: `postgresql://postgres:postgres@localhost:54322/postgres`

---

## Recommended: Option 1 (Docker) → Option 4 (Supabase)

**My recommendation:**
1. **Start with Option 1** if you have Docker
   - Gives you PostgreSQL locally
   - Works with current app architecture
   - Easy to manage
   
2. **Upgrade to Option 4** when ready
   - Full Supabase experience locally
   - Exact production environment
   - Can test auth flows properly

---

## Environment Setup

Once you pick your option, update `.env.local`:

```env
# Replace with your chosen option's connection string
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker

# Keep or remove based on whether you use Supabase Auth
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

Then run:
```bash
npm run dev
```

---

## Which Option Should I Choose?

| Option | Easiest | Production-like | Fast | Zero deps |
|--------|---------|-----------------|------|-----------|
| Docker | ✓ | ✓✓ | ✓ | - |
| Local PostgreSQL | ✓✓ | ✓✓ | ✓ | - |
| SQLite | ✓✓✓ | - | ✓✓ | ✓ |
| Supabase Local | - | ✓✓✓ | ✓ | - |

**Quickest start:** Option 3 (SQLite)  
**Most similar to production:** Option 4 (Supabase)  
**Best balance:** Option 1 (Docker)  
**No infrastructure needed:** Option 3 (SQLite) or Option 2 (Local PostgreSQL)

Choose based on your setup and needs!
