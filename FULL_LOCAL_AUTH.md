# Full Local Setup: Database + Authentication

This guide sets up the app with a local PostgreSQL database and NextAuth.js for authentication (no Supabase required).

## Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ installed

## Installation Steps

### 1. Start PostgreSQL

```bash
docker-compose up -d
```

### 2. Install authentication libraries

```bash
npm install bcryptjs next-auth
npm install --save-dev @types/bcryptjs
```

### 3. Update environment variables

Create/update `.env.local`:

```env
# Database
DATABASE_URL=postgresql://dev:devpassword@localhost:5432/job_tracker

# NextAuth configuration
NEXTAUTH_SECRET=your-random-secret-key-must-be-at-least-32-characters-long
NEXTAUTH_URL=http://localhost:3000
```

Generate a secure NEXTAUTH_SECRET:
```bash
openssl rand -base64 32
```

### 4. Create NextAuth configuration

Create `lib/nextauth.ts`:

```typescript
import { type NextAuthConfig } from 'next-auth'
import Credentials from 'next-auth/providers/credentials'
import { sql } from '@vercel/postgres'
import bcrypt from 'bcryptjs'

const verifyCredentials = async (email: string, password: string) => {
  const user = await sql`
    SELECT id, email FROM users WHERE email = ${email}
  `
  
  if (!user.rows.length) return null
  
  // In production, store password hash in database
  // For now, demo users
  const isValid = password === 'demo123'
  if (!isValid) return null
  
  return { id: user.rows[0].id, email: user.rows[0].email }
}

export const authConfig: NextAuthConfig = {
  providers: [
    Credentials({
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null
        
        const user = await verifyCredentials(
          credentials.email as string,
          credentials.password as string
        )
        
        return user || null
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
      }
      return session
    },
  },
}
```

### 5. Create auth API route

Create `app/api/auth/[...nextauth]/route.ts`:

```typescript
import NextAuth from 'next-auth'
import { authConfig } from '@/lib/nextauth'

export const { handlers, auth } = NextAuth(authConfig)
export const GET = handlers.GET
export const POST = handlers.POST
```

### 6. Update authentication pages

See separate implementation guide in this repo's components.

## Security Notes

**Demo Setup:**
- Password verification is simplified for local development
- Use `demo123` as password for demo users
- **DO NOT** use this in production

**Production Setup:**
- Hash passwords with bcryptjs before storing
- Use proper secret rotation
- Enable HTTPS
- Use environment variables for sensitive data

## Testing Local Auth

1. Start the app: `npm run dev`
2. Navigate to http://localhost:3000/auth/signup
3. Create a user account
4. Check database:

```bash
docker-compose exec postgres psql -U dev -d job_tracker
SELECT * FROM users;
```

## Migrating from Supabase

If you previously used Supabase:

1. Export your data from Supabase
2. Import into local PostgreSQL
3. Update signup/login components to use NextAuth instead of Supabase
4. Remove `@supabase/supabase-js` dependency (optional)

## Further Customization

- Add OAuth providers (GitHub, Google, etc.)
- Implement email verification
- Add password reset functionality
- Set up database-backed sessions

Refer to [NextAuth.js documentation](https://next-auth.js.org/) for advanced features.
