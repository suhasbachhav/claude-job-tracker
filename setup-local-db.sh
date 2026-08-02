#!/bin/bash

# Job Tracker Local Database Setup Script
# This script sets up a local PostgreSQL database for development

set -e

echo "🚀 Job Tracker Local Database Setup"
echo "===================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo ""
fi

# Install PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "📦 Installing PostgreSQL 16..."
    brew install postgresql@16
    echo ""
fi

# Start PostgreSQL service
echo "🗄️  Starting PostgreSQL..."
brew services start postgresql@16 || brew services restart postgresql@16
echo ""

# Create database and user
echo "📝 Creating database and user..."

# Create user if not exists
psql -U postgres -tc "SELECT 1 FROM pg_user WHERE usename = 'dev'" | grep -q 1 || psql -U postgres -c "CREATE USER dev WITH PASSWORD 'devpassword';"

# Create database if not exists
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'job_tracker'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE job_tracker OWNER dev;"

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE job_tracker TO dev;"
echo ""

# Run migrations
echo "📚 Running database migrations..."
psql -U dev -d job_tracker -f supabase/migrations/001_initial_schema.sql > /dev/null 2>&1 || true
echo ""

# Verify setup
echo "✅ Verifying database setup..."
psql -U dev -d job_tracker -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public';" | grep -E "(users|jobs)" > /dev/null && echo "✓ Tables created successfully" || echo "✗ Warning: Could not verify tables"
echo ""

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "📄 Creating .env.local..."
    cat > .env.local << 'EOF'
# Local PostgreSQL Database
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker

# Supabase Auth (keep for authentication)
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
EOF
    echo "✓ Created .env.local"
    echo ""
fi

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your Supabase credentials to .env.local (optional, for auth)"
echo "2. Run: npm run dev"
echo "3. Visit: http://localhost:3000"
echo ""
echo "Database connection: postgresql://dev:devpassword@localhost:5432/job_tracker"
echo ""
echo "Useful commands:"
echo "  psql -U dev -d job_tracker          # Connect to database"
echo "  brew services stop postgresql@16   # Stop PostgreSQL"
echo "  brew services start postgresql@16  # Start PostgreSQL"
