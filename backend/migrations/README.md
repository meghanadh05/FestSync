# FestSync Database Migrations

This directory contains SQL migration files for setting up the FestSync PostgreSQL database on Supabase.

## Migration Files

### 1. `001_initial_schema.sql`
**Creates all base tables and indexes**

Tables created:
- `profiles` - User profiles with roles (user, vendor, admin)
- `events` - User-created events with status tracking
- `event_plans` - AI-generated event plans
- `plan_sections` - Structured plan components
- `tasks` - Event to-do items with priority and assignment
- `subtasks` - Nested tasks
- `vendors` - Vendor profiles and services
- `vendor_services` - Specific services offered
- `vendor_images` - Portfolio images
- `saved_vendors` - User's favorite vendors per event
- `budget_items` - Expense tracking
- `guests` - Event guest list with RSVP
- `bookings` - Vendor bookings with payment tracking
- `ai_generations` - AI API call logging
- `notifications` - User notifications

**Features:**
- UUID primary keys for all tables
- Foreign keys with CASCADE delete where appropriate
- CHECK constraints for enums (status, priority, roles, etc.)
- Comprehensive indexing for query performance
- `created_at` and `updated_at` timestamps with automatic triggers
- Detailed SQL comments explaining each table

**Run first:** Yes, this is the base schema

### 2. `002_rls_policies.sql`
**Enables Row Level Security (RLS) policies for data access control**

**Policies implemented:**
- ✅ Users can only access their own events, tasks, budgets
- ✅ Users can only see saved vendors for their events
- ✅ Vendors can only update their own profiles and services
- ✅ Vendors can view bookings for their vendors
- ✅ Admins have full access to all data
- ✅ Public read access to vendor data
- ✅ Service role can insert notifications (for backend)

**Security features:**
- Row-level filtering based on user ID
- Role-based access control (user, vendor, admin)
- Prevents unauthorized access to other users' data
- Helper functions: `is_admin()`, `auth.user_id()`

**Run after:** 001_initial_schema.sql

### 3. `003_seed_vendors.sql`
**Populates database with sample vendor data**

**Sample vendors by category:**
- **Catering (4):** Premium, mid-range, budget, and specialized options
- **Venue (4):** Ballroom, loft, outdoor estate, business center
- **Photography (4):** Artistic, videography, documentary, corporate
- **Decoration (4):** Premium, contemporary, budget-friendly, lighting specialist
- **Music/DJ (4):** Professional DJ, live band, budget DJ, DJ+lighting combo
- **Event Planner (4):** Premium, mid-range, budget, corporate specialist

**Additional data:**
- 24 vendors with full profiles
- 12 vendor services with pricing
- 8 sample portfolio images
- Realistic ratings, reviews, and availability status
- Contact information and certifications

**Run after:** 001_initial_schema.sql and 002_rls_policies.sql

## Setup Instructions

### For Supabase Project:

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note your project URL and API keys

2. **Run migrations in order:**

   **Step 1: Initial Schema**
   - Go to SQL Editor in Supabase Dashboard
   - Copy contents of `001_initial_schema.sql`
   - Paste into SQL Editor
   - Click "Run"

   **Step 2: RLS Policies**
   - Copy contents of `002_rls_policies.sql`
   - Paste into SQL Editor
   - Click "Run"

   **Step 3: Seed Data** (Optional, for development)
   - Copy contents of `003_seed_vendors.sql`
   - Paste into SQL Editor
   - Click "Run"

3. **Verify Tables**
   - Go to "Table Editor" in Supabase
   - Confirm all 15 tables are created
   - Verify profiles, events, vendors have sample data

### For Local PostgreSQL Testing:

```bash
# Connect to your PostgreSQL database
psql -U postgres -d festsync

# Run migrations in order
\i 001_initial_schema.sql
\i 002_rls_policies.sql
\i 003_seed_vendors.sql

# Verify
\dt  # List all tables
```

## Data Models

### Key Relationships

```
auth.users (1) ──→ (1) profiles
profiles (1) ──→ (many) events
profiles (1) ──→ (many) tasks, budget_items, saved_vendors, notifications

events (1) ──→ (1) event_plans
event_plans (1) ──→ (many) plan_sections
events (1) ──→ (many) tasks, budget_items, guests, bookings

vendors (1) ──→ (many) vendor_services, vendor_images, bookings, saved_vendors
tasks (1) ──→ (many) subtasks
```

### Enums (CHECK Constraints)

**Roles:**
- `user` - Regular user
- `vendor` - Vendor/business owner
- `admin` - Platform admin

**Event Status:**
- `planning` - Event being planned
- `ongoing` - Event in progress
- `completed` - Event finished
- `cancelled` - Event cancelled

**Task Status:**
- `pending` - Not started
- `in_progress` - Being worked on
- `completed` - Finished
- `cancelled` - Cancelled

**Task Priority:**
- `low` - Low priority
- `medium` - Normal priority
- `high` - High priority
- `urgent` - Urgent

**Vendor Type:**
- catering, venue, photography, decoration, music, event_planner, transportation, accommodation, invitations, cake, florist, entertainment

**Booking Status:**
- `pending` - Awaiting confirmation
- `confirmed` - Confirmed booking
- `completed` - Service completed
- `cancelled` - Cancelled

**Payment Status:**
- `pending` - Not paid
- `partial` - Partially paid
- `full` - Fully paid

## Indexing Strategy

The schema includes strategic indexes for performance:

```
Profiles:
  - email (authentication lookups)
  - role (filtering admins/vendors)

Events:
  - user_id (user's events)
  - status, event_type (filtering)
  - start_date (timeline queries)
  - user_id + status (common filter)

Tasks:
  - event_id, status, priority (filtering)
  - assigned_to (user's assigned tasks)
  - due_date (upcoming tasks)

Vendors:
  - vendor_type, city (search)
  - rating (finding top vendors)
  - name search via TSVECTOR (full-text)

Budget Items:
  - event_id, category, status (reporting)

Saved Vendors:
  - user_id, event_id (user's favorites)
  - status (booked vs. saved)
```

## Automatic Timestamp Updates

All tables with `updated_at` have automatic triggers that update the timestamp on row modification:

```sql
CREATE TRIGGER update_[table_name]_updated_at BEFORE UPDATE ON [table_name]
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

This ensures `updated_at` is always accurate without manual updates.

## Row Level Security (RLS)

RLS is enabled on all tables. Key policies:

- **User Data Isolation:** Users can only see/modify their own records
- **Event Access:** Limited to event owner
- **Vendor Read Access:** Public for all users
- **Admin Override:** Admins bypass RLS for management tasks
- **Service Role:** Backend can insert notifications

To query as specific user in development:
```sql
-- Set auth claims for testing
SELECT set_config('request.jwt.claims', '{"sub":"uuid-here"}', false);
```

## Sample Data

The seed file includes realistic sample data:

**Vendors:** 24 vendors across 6 categories with:
- Full contact information
- Pricing (budget, mid-range, premium)
- Ratings and review counts
- Certifications and qualifications
- Portfolio images
- Services with pricing

**Services:** 12 sample services showing pricing and duration

**Images:** 8 sample portfolio images for vendors

This data is ideal for:
- UI/UX development
- Testing search/filter functionality
- Building the vendor comparison feature
- Testing booking workflows

## Modifying Schema

### Adding a New Table

1. Create migration file: `004_add_[feature_name].sql`
2. Include full CREATE TABLE statement
3. Add indexes for frequently queried columns
4. Add RLS policies
5. Update this README

### Modifying Existing Tables

1. Use ALTER TABLE statements
2. Be careful with data migrations
3. Test in development first
4. Document changes

## Backups

Supabase automatically backs up your database. To manually backup:

**Via Supabase Dashboard:**
1. Project Settings → Backups
2. Click "Request manual backup"

**Via CLI:**
```bash
supabase db pull # Download schema
```

## Troubleshooting

### RLS Blocking Access
If you can't see data after enabling RLS:
- Check RLS policies are set up correctly
- Verify `auth.uid()` is returning correct user ID
- Check user exists in `profiles` table

### Foreign Key Errors
- Ensure parent record exists before inserting child
- Check ON DELETE CASCADE settings
- Verify UUIDs are correctly formatted

### Performance Issues
- Check indexes exist on frequently queried columns
- Use EXPLAIN ANALYZE to find slow queries
- Consider pagination for large result sets

## Support Resources

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [FestSync Documentation](/docs/DATABASE_SCHEMA.md)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-03 | Initial schema with 15 tables, RLS, and sample vendors |

---

**Last Updated:** June 2026
