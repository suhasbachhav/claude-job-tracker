# 🚀 Job Tracker - Local Development Quick Start

## TL;DR - Get Running in 5 Minutes

You're on macOS. Run these commands in your terminal:

```bash
# 1. Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install PostgreSQL
brew install postgresql@16

# 3. Start PostgreSQL
brew services start postgresql@16

# 4. Create database and user
psql -U postgres << 'EOF'
CREATE USER dev WITH PASSWORD 'devpassword';
CREATE DATABASE job_tracker OWNER dev;
GRANT ALL PRIVILEGES ON DATABASE job_tracker TO dev;
\q
EOF

# 5. Run migrations
cd /path/to/claude-job-tracker
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql

# 6. Start the app
npm run dev
```

Then visit: **http://localhost:3000**

---

## ✅ What's Already Set Up

- ✓ Database schema ready (`supabase/migrations/001_initial_schema.sql`)
- ✓ Environment variables configured (`.env.local`)
- ✓ Docker support if needed (`docker-compose.yml`)
- ✓ Comprehensive guides for all setup methods

---

## 📚 Detailed Guides (Pick Your Path)

### Just Want It Working?
👉 **Read: [MACOS_QUICK_START.md](MACOS_QUICK_START.md)**
- Step-by-step instructions
- Troubleshooting tips
- Takes 10-15 minutes

### Want to Use Docker?
👉 **Read: [SETUP_OPTIONS.md](SETUP_OPTIONS.md) → Option 1**
- Just run: `docker compose up -d`
- Done in 2 minutes

### Want a Fully Local Setup?
👉 **Read: [FULL_LOCAL_AUTH.md](FULL_LOCAL_AUTH.md)**
- No Supabase needed
- Local database + NextAuth

### Need Database Commands?
👉 **Read: [DATABASE_COMMANDS.md](DATABASE_COMMANDS.md)**
- psql commands reference
- Query examples
- Data management

### Overview of All Options?
👉 **Read: [SETUP_OPTIONS.md](SETUP_OPTIONS.md)**
- Docker, PostgreSQL, SQLite, Supabase
- Compare pros/cons

---

## 🎯 Your Database Connection Info

```
Type:     PostgreSQL
Host:     localhost
Port:     5432
Database: job_tracker
User:     dev
Password: devpassword
URL:      postgresql://dev:devpassword@localhost:5432/job_tracker
```

This is already in `.env.local` - no changes needed!

---

## 🔐 Authentication

### Using Supabase (Recommended for Quick Start)
1. Get credentials from https://app.supabase.com
2. Add to `.env.local`:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your-url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-key
   ```
3. Done! Auth works with local database

### Using Local Auth (No Supabase)
- Follow [FULL_LOCAL_AUTH.md](FULL_LOCAL_AUTH.md)
- Removes Supabase dependency
- Uses NextAuth + local database

---

## 📁 Files That Were Created

```
├── .env.local                    # Environment variables (not committed)
├── docker-compose.yml            # Docker setup for PostgreSQL
├── setup-local-db.sh             # Automated setup script
├── START_HERE.md                 # This file
├── LOCAL_DEVELOPMENT.md          # Complete development guide
├── MACOS_QUICK_START.md          # Step-by-step macOS setup
├── SETUP_OPTIONS.md              # All setup methods explained
├── LOCAL_AUTH_SETUP.md           # Database + Supabase Auth
├── FULL_LOCAL_AUTH.md            # Database + NextAuth (no Supabase)
└── DATABASE_COMMANDS.md          # PostgreSQL commands reference
```

---

## 🚀 Start Developing

### Step 1: Set Up Database
Follow **[MACOS_QUICK_START.md](MACOS_QUICK_START.md)** or use Docker

### Step 2: Configure Auth (Optional)
If using Supabase, add credentials to `.env.local`

### Step 3: Start Dev Server
```bash
npm run dev
```

### Step 4: Open in Browser
http://localhost:3000

---

## 💡 Common Tasks

### Start/Stop Database
```bash
brew services start postgresql@16   # Start
brew services stop postgresql@16    # Stop
brew services restart postgresql@16 # Restart
```

### Connect to Database
```bash
psql -U dev -d job_tracker
```

### View Your Data
```bash
psql -U dev -d job_tracker -c "SELECT * FROM jobs;"
```

### Reset Database (Delete All Data)
```bash
psql -U dev -d job_tracker -c "TRUNCATE jobs CASCADE;"
```

### Full Database Reset
See troubleshooting section in [MACOS_QUICK_START.md](MACOS_QUICK_START.md)

---

## ❓ Stuck?

1. **Database won't start?**
   - Check: `brew services list | grep postgresql`
   - Restart: `brew services restart postgresql@16`
   - See: [MACOS_QUICK_START.md#troubleshooting](MACOS_QUICK_START.md)

2. **Connection refused?**
   - Ensure PostgreSQL is running
   - Check `.env.local` has correct `DATABASE_URL`

3. **Authentication not working?**
   - Add Supabase credentials to `.env.local`
   - Or follow [FULL_LOCAL_AUTH.md](FULL_LOCAL_AUTH.md)

4. **Need more help?**
   - See [MACOS_QUICK_START.md](MACOS_QUICK_START.md) troubleshooting
   - Or [SETUP_OPTIONS.md](SETUP_OPTIONS.md) for your OS

---

## 🎉 You're Ready!

1. Pick your setup method
2. Follow the guide
3. Run `npm run dev`
4. Start building!

**Questions?** Check the detailed guides above. Everything is documented!

---

## Next Steps After Setup

1. ✅ Database running locally
2. ✅ App configured with `.env.local`
3. ✅ `npm run dev` starts the dev server
4. 🔄 Start coding! The database handles all data persistence locally

Happy coding! 🚀
