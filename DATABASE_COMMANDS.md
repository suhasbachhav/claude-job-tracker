# Database Commands Reference

Quick reference for common PostgreSQL commands for local development.

## Connection

```bash
# Connect with dev user
psql -U dev -d job_tracker

# Connect with postgres user (admin)
psql -U postgres

# Connect and run command
psql -U dev -d job_tracker -c "SELECT * FROM jobs;"

# Connect and run file
psql -U dev -d job_tracker -f migrations.sql
```

## Inspect Database

```bash
# List all databases
\l

# List all tables in job_tracker database
\dt

# Show table structure
\d jobs

# Show table columns
\d+ jobs

# List indexes
\di

# List all users/roles
\du
```

## Query Data

```bash
-- View all users
SELECT * FROM users;

-- View all jobs
SELECT * FROM jobs;

-- Count jobs by status
SELECT status, COUNT(*) as count FROM jobs GROUP BY status;

-- Find jobs for a user
SELECT * FROM jobs WHERE user_id = 'user-id-here';

-- View recently created jobs
SELECT company, position, applied_date FROM jobs ORDER BY created_at DESC LIMIT 10;

-- Join users and jobs
SELECT u.email, j.company, j.position, j.status 
FROM jobs j 
JOIN users u ON j.user_id = u.id 
ORDER BY j.created_at DESC;
```

## Modify Data

```bash
-- Create a test user
INSERT INTO users (email) VALUES ('test@example.com');

-- Create a test job
INSERT INTO jobs (user_id, company, position, status, applied_date) 
VALUES (
  (SELECT id FROM users LIMIT 1),
  'Tech Company',
  'Software Engineer',
  'applied',
  CURRENT_DATE
);

-- Update job status
UPDATE jobs SET status = 'interview' WHERE company = 'Tech Company';

-- Delete a job
DELETE FROM jobs WHERE id = 'job-id-here';

-- Clear all jobs (careful!)
DELETE FROM jobs;

-- Clear all data (careful!)
TRUNCATE jobs, users;
```

## Database Maintenance

```bash
-- Show database size
SELECT pg_size_pretty(pg_database_size('job_tracker'));

-- Show table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
WHERE schemaname != 'pg_catalog' 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Analyze table
ANALYZE jobs;

-- Vacuum table (clean up)
VACUUM ANALYZE jobs;
```

## Export & Import

```bash
# Export entire database
pg_dump -U dev job_tracker > backup.sql

# Export specific table
pg_dump -U dev -t jobs job_tracker > jobs_backup.sql

# Export with data only (no schema)
pg_dump -U dev --data-only job_tracker > data.sql

# Import data
psql -U dev job_tracker < backup.sql

# Import specific table
psql -U dev job_tracker < jobs_backup.sql
```

## User Management

```bash
# Create new user
CREATE USER newuser WITH PASSWORD 'password123';

-- Grant permissions on database
GRANT ALL PRIVILEGES ON DATABASE job_tracker TO newuser;

-- Grant permissions on specific table
GRANT SELECT, INSERT, UPDATE, DELETE ON jobs TO newuser;

-- Remove user
DROP USER newuser;

-- Show current user
SELECT current_user;

-- List all users
\du
```

## Migrations

```bash
# Run migrations
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql

# Check migration status
psql -U dev -d job_tracker -c "\d"

# Run migration with output
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql -v

# Dry run (view the SQL without running)
cat supabase/migrations/001_initial_schema.sql
```

## Common Operations

```bash
# Reset database (delete all data, keep schema)
TRUNCATE jobs CASCADE;

-- Reset database (delete everything and recreate schema)
-- 1. In bash:
dropdb -U postgres job_tracker
psql -U postgres -c "CREATE DATABASE job_tracker OWNER dev;"
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql

# View query execution plan
EXPLAIN SELECT * FROM jobs WHERE status = 'applied';

# View detailed execution plan
EXPLAIN ANALYZE SELECT * FROM jobs WHERE status = 'applied';

# Check for locks
SELECT * FROM pg_locks;

-- View recent queries (requires logging enabled)
SELECT query, query_start FROM pg_stat_activity WHERE query NOT LIKE '%pg_stat_activity%';
```

## Service Management (macOS)

```bash
# Start PostgreSQL service
brew services start postgresql@16

# Stop PostgreSQL service
brew services stop postgresql@16

# Restart PostgreSQL service
brew services restart postgresql@16

# Check service status
brew services list | grep postgresql

# View PostgreSQL logs
tail -50 ~/Library/Logs/Homebrew/postgresql@16/error.log
```

## Exit psql

```bash
\q        # Quit
Ctrl+D    # Also quits
```

## Useful Tips

- **Prefix psql commands with backslash** (`\`) — these are psql-specific, not SQL
- **SQL statements must end with semicolon** (`;`)
- **Use `\d table_name`** to see table structure before querying
- **Use `LIMIT`** when exploring data to avoid large result sets
- **Use `EXPLAIN ANALYZE`** to see query performance
- **Always backup** before running destructive commands like `TRUNCATE` or `DROP`

## Example Workflow

```bash
# 1. Connect to database
psql -U dev -d job_tracker

# 2. Check tables exist
\dt

# 3. View data
SELECT * FROM jobs LIMIT 5;

-- 4. Make changes
INSERT INTO jobs (...) VALUES (...);

-- 5. Verify changes
SELECT * FROM jobs ORDER BY created_at DESC LIMIT 1;

-- 6. Exit
\q
```

---

## Need Help?

- **psql not found?** → Check DATABASE_SETUP.md troubleshooting
- **Connection refused?** → Ensure PostgreSQL service is running
- **Permission denied?** → Use correct user (`dev`) and password (`devpassword`)
- **Table doesn't exist?** → Run migrations with the correct path
