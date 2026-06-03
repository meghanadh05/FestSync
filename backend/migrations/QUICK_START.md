# FestSync Database Quick Start

**Goal:** Set up FestSync PostgreSQL database on Supabase in 5 minutes.

## Step-by-Step Setup

### 1. Create Supabase Project
```
1. Go to https://supabase.com
2. Sign in (or create account)
3. Click "New Project"
4. Select your organization
5. Fill in:
   - Project name: "festsync"
   - Database password: (save securely)
   - Region: (choose closest region)
   - Pricing plan: (Free tier works for development)
6. Click "Create new project"
7. Wait 2-3 minutes for setup
```

### 2. Note Your Connection Details
```
From Supabase Dashboard:
- Project Settings → Database
- Copy "Connection string" for later

Environment variables you'll need:
- DATABASE_URL (connection string)
- SUPABASE_URL (from Settings → API)
- SUPABASE_KEY (from Settings → API)
```

### 3. Run Migrations

**Via Supabase Dashboard (Easiest):**

1. Go to SQL Editor
2. Click "New Query"
3. Copy-paste **entire** content from `001_initial_schema.sql`
4. Click "Run"
5. Wait for completion (should see ✓)

Repeat for:
- `002_rls_policies.sql`
- `003_seed_vendors.sql` (optional, for sample data)

**Via Command Line (Alternative):**

```bash
# Install Supabase CLI
npm install -g supabase

# Link to your project
supabase link --project-ref your-project-id

# Push migrations
supabase db push

# Seed sample data
psql $DATABASE_URL < 003_seed_vendors.sql
```

### 4. Verify Setup
In Supabase Dashboard:
1. Go to Table Editor
2. Expand all tables in sidebar
3. You should see:
   - ✓ profiles
   - ✓ events
   - ✓ event_plans
   - ✓ plan_sections
   - ✓ tasks
   - ✓ subtasks
   - ✓ vendors (24 sample vendors)
   - ✓ vendor_services
   - ✓ vendor_images
   - ✓ saved_vendors
   - ✓ budget_items
   - ✓ guests
   - ✓ bookings
   - ✓ ai_generations
   - ✓ notifications

## Configuration

### Backend `.env` File
```bash
# Backend environment variables
DATABASE_URL=postgresql://postgres:PASSWORD@db.xxxxx.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc...
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secret-key
```

### Frontend `.env.local` File
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
```

## Common Tasks

### Test Data Access (SQL)
```sql
-- As authenticated user, view their events
SELECT * FROM events WHERE user_id = auth.uid();

-- View all vendors (public access)
SELECT * FROM vendors LIMIT 10;

-- Check RLS policies
SELECT * FROM pg_policies WHERE tablename = 'events';
```

### Reset Database (Development Only)
```bash
# ⚠️ Deletes all data!
supabase db reset

# Or via Dashboard:
# Project Settings → Database → Reset Database
```

### View Database Logs
```bash
# In Supabase Dashboard:
# Database → Logs → Slow Queries, Realtime, Edge Logs
```

### Connect via DBeaver (GUI)
1. Download [DBeaver Community](https://dbeaver.io)
2. New Database Connection → PostgreSQL
3. Host: `db.xxxxx.supabase.co`
4. Port: `5432`
5. Database: `postgres`
6. Username: `postgres`
7. Password: (from Supabase)

## Troubleshooting

### "Permission denied for schema public"
- Check RLS policies are enabled
- Verify user is logged in (has auth.uid())
- Try from service role (has full access)

### "Foreign key constraint violation"
- Parent record must exist first
- Check referenced IDs exist in parent table
- Verify CASCADE delete settings

### "Table does not exist"
- Migrations may not have run
- Check SQL Editor shows no errors
- Try running migrations again

### Connection Timeout
- Check internet connection
- Verify DATABASE_URL is correct
- Check Supabase project is active

## File Structure

```
backend/migrations/
├── 001_initial_schema.sql      ← Run first
├── 002_rls_policies.sql         ← Run second
├── 003_seed_vendors.sql         ← Run third (optional)
├── README.md                     ← Full documentation
└── QUICK_START.md               ← This file
```

## Next Steps

1. **Backend Setup**
   - Copy `.env` template
   - Set environment variables
   - Run `pip install -r requirements.txt`
   - Test database connection

2. **Frontend Setup**
   - Copy `.env.local` template
   - Set environment variables
   - Run `npm install`
   - Test Supabase connection

3. **Test Features**
   - Create test user
   - Create test event
   - Verify RLS policies work
   - Test vendor search

## Schema Overview

### Core Entities
```
Users (auth.users)
  ↓
Profiles (roles: user, vendor, admin)
  ├─ Events (planning, ongoing, completed, cancelled)
  │  ├─ Event Plans (AI-generated)
  │  │  └─ Plan Sections
  │  ├─ Tasks (with priority, assignment)
  │  │  └─ Subtasks
  │  ├─ Budget Items (expense tracking)
  │  ├─ Guests (RSVP tracking)
  │  ├─ Bookings (vendor bookings)
  │  └─ Saved Vendors (favorites)
  ├─ Vendors (24 sample vendors)
  │  ├─ Services
  │  └─ Images
  └─ Notifications
```

## Key Features

✅ **15 Tables:** Complete MVP schema
✅ **UUID Keys:** Modern, distributed-friendly
✅ **RLS Policies:** Built-in data security
✅ **Auto Timestamps:** Automatic created_at/updated_at
✅ **Foreign Keys:** Referential integrity
✅ **Indexes:** Query optimization
✅ **Sample Data:** 24 vendors ready for testing

## Performance Targets

- Event list query: <50ms
- Vendor search: <100ms (with pagination)
- Budget summary: <50ms
- All with proper indexes ✓

## Support

- Documentation: See [README.md](README.md)
- Schema Details: See [DATABASE_SCHEMA.md](/docs/DATABASE_SCHEMA.md)
- Supabase Docs: https://supabase.com/docs
- Slack: FestSync team channel

---

**Time to complete:** ~10 minutes including verification
**Ready to build!** 🚀
