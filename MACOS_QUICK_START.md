# macOS Quick Start: Local Database Setup

## Step 1: Install Homebrew (if not already installed)

Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

This will prompt for your password. Homebrew installation takes 2-5 minutes.

Verify installation:
```bash
brew --version
```

## Step 2: Install PostgreSQL 16

```bash
brew install postgresql@16
```

Verify installation:
```bash
brew --version
brew services list
```

## Step 3: Start PostgreSQL Service

```bash
brew services start postgresql@16
```

Verify it's running:
```bash
brew services list | grep postgresql
# Should show: postgresql@16 started
```

## Step 4: Create Database and User

Copy and paste this entire block into Terminal:

```bash
psql -U postgres << 'EOF'
-- Create user (ignore error if user already exists)
CREATE USER dev WITH PASSWORD 'devpassword';

-- Create database
CREATE DATABASE job_tracker OWNER dev;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE job_tracker TO dev;

\q
EOF
```

Or run these commands one by one:

```bash
# Create user
psql -U postgres -c "CREATE USER dev WITH PASSWORD 'devpassword';"

# Create database
psql -U postgres -c "CREATE DATABASE job_tracker OWNER dev;"

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE job_tracker TO dev;"
```

## Step 5: Run Database Migrations

```bash
cd /path/to/claude-job-tracker

psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql
```

Verify tables were created:
```bash
psql -U dev -d job_tracker -c "\dt"
```

You should see:
```
         List of relations
 Schema | Name  | Type  | Owner
--------+-------+-------+-------
 public | jobs  | table | dev
 public | users | table | dev
(2 rows)
```

## Step 6: Update Environment Variables

Your `.env.local` file has been created with:

```env
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

If using Supabase Auth, update the Supabase credentials.

## Step 7: Start the App

```bash
npm install  # if you haven't already
npm run dev
```

Visit: http://localhost:3000

---

## Troubleshooting

### "psql: command not found"
```bash
# Check PostgreSQL installation
brew services list | grep postgresql

# If not installed, run:
brew install postgresql@16

# Add psql to PATH (temporarily for current session):
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"

# For permanent fix, add to ~/.zshrc:
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "FATAL: database does not exist"
Ensure you ran Step 5 (migration):
```bash
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql
```

### "FATAL: role 'dev' does not exist"
Create the user:
```bash
psql -U postgres -c "CREATE USER dev WITH PASSWORD 'devpassword';"
```

### PostgreSQL not starting
```bash
# Check if it's running
brew services list | grep postgresql

# Restart it
brew services restart postgresql@16

# View logs
tail -50 ~/Library/Logs/Homebrew/postgresql@16/error.log
```

### Permission denied for user operations
If you get permission errors, ensure you're using the `dev` user:
```bash
psql -U dev -d job_tracker  # ✓ Correct
psql -U postgres -d job_tracker  # ✗ Wrong user for normal operations
```

---

## Common Commands

```bash
# Connect to your database
psql -U dev -d job_tracker

# View all tables
psql -U dev -d job_tracker -c "\dt"

# View table structure
psql -U dev -d job_tracker -c "\d jobs"

# Run a SQL query
psql -U dev -d job_tracker -c "SELECT COUNT(*) FROM jobs;"

# Backup database
pg_dump -U dev -d job_tracker > backup.sql

# Restore database
psql -U dev -d job_tracker < backup.sql

# Stop PostgreSQL (but keep data)
brew services stop postgresql@16

# Start PostgreSQL again
brew services start postgresql@16

# Delete everything and reset (careful!)
dropdb -U postgres job_tracker
dropuser -U postgres dev
# Then re-run Steps 4-5
```

---

## Next Steps

1. ✅ Database is set up and running
2. 📝 Update `.env.local` with your Supabase credentials (optional)
3. 🚀 Run `npm run dev` and visit http://localhost:3000
4. 🔐 Sign up with your email and test the app

You're all set! The app will now use your local PostgreSQL database.
