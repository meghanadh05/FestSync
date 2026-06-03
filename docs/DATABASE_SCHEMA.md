# FestSync Database Schema

## Overview

FestSync uses PostgreSQL via Supabase for all data persistence. The schema is designed to support event planning, vendor management, budgeting, and team collaboration.

## Database Tables

### 1. users

Stores user account information and profile data.

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  full_name VARCHAR(255),
  phone_number VARCHAR(20),
  profile_image_url TEXT,
  bio TEXT,
  location VARCHAR(255),
  preferences JSONB,  -- User settings and preferences
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP  -- Soft delete
);

CREATE INDEX idx_users_email ON users(email);
```

**Fields**:
- `id`: Unique user identifier
- `email`: User email (managed by Supabase Auth)
- `full_name`: User's full name
- `phone_number`: Contact number
- `profile_image_url`: Avatar/profile picture URL
- `bio`: User bio
- `location`: Home location
- `preferences`: JSON object for user settings (theme, notifications, etc.)

---

### 2. events

Stores event information created by users.

```sql
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  event_type VARCHAR(50) NOT NULL,  -- 'wedding', 'birthday', 'corporate', 'college_fest', 'conference'
  status VARCHAR(50) DEFAULT 'planning',  -- 'planning', 'ongoing', 'completed', 'cancelled'
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  location VARCHAR(255),
  estimated_guests INTEGER,
  budget DECIMAL(12, 2),
  currency VARCHAR(10) DEFAULT 'USD',
  thumbnail_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP
);

CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_start_date ON events(start_date);
CREATE INDEX idx_events_status ON events(status);
```

**Fields**:
- `id`: Unique event identifier
- `user_id`: Owner of the event
- `title`: Event name
- `description`: Detailed event description
- `event_type`: Category of event
- `status`: Current event status
- `start_date`, `end_date`: Event duration
- `location`: Event location
- `estimated_guests`: Expected attendance
- `budget`: Total event budget
- `currency`: Budget currency code

---

### 3. event_ai_plans

Stores AI-generated event plans.

```sql
CREATE TABLE event_ai_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  plan_content JSONB NOT NULL,  -- Structured AI plan
  timeline JSONB,  -- Event timeline with milestones
  budget_breakdown JSONB,  -- Suggested budget allocation
  vendor_suggestions JSONB,  -- Suggested vendor categories
  generated_at TIMESTAMP DEFAULT NOW(),
  regenerated_at TIMESTAMP,
  version INTEGER DEFAULT 1
);

CREATE INDEX idx_event_ai_plans_event_id ON event_ai_plans(event_id);
```

**Fields**:
- `id`: Unique plan identifier
- `event_id`: Associated event
- `plan_content`: Full AI-generated plan (structured JSON)
- `timeline`: Timeline and milestones JSON
- `budget_breakdown`: Category-wise budget suggestions
- `vendor_suggestions`: Recommended vendor categories
- `version`: Plan version for regeneration tracking

---

### 4. tasks (To-Do Board)

Stores tasks/to-dos for each event.

```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'in_progress', 'completed', 'cancelled'
  priority VARCHAR(20) DEFAULT 'medium',  -- 'low', 'medium', 'high', 'urgent'
  category VARCHAR(100),  -- e.g., 'venue', 'catering', 'decoration', 'entertainment'
  due_date DATE,
  assigned_to UUID REFERENCES users(id),
  tags TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);

CREATE INDEX idx_tasks_event_id ON tasks(event_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

**Fields**:
- `id`: Unique task identifier
- `event_id`: Associated event
- `user_id`: Task creator
- `title`: Task title
- `description`: Task details
- `status`: Completion status
- `priority`: Priority level
- `category`: Task category
- `due_date`: Deadline
- `assigned_to`: Assigned team member

---

### 5. vendors

Stores vendor information searchable by event type and location.

```sql
CREATE TABLE vendors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  vendor_type VARCHAR(100),  -- 'catering', 'venue', 'photography', 'decoration', 'entertainment', 'transportation', 'accommodation'
  location VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  phone_number VARCHAR(20),
  email VARCHAR(255),
  website_url TEXT,
  social_media JSONB,  -- Instagram, Facebook URLs
  price_range VARCHAR(50),  -- 'budget', 'mid-range', 'premium'
  min_price DECIMAL(12, 2),
  max_price DECIMAL(12, 2),
  rating DECIMAL(3, 2) DEFAULT 0,  -- Average rating 0-5
  review_count INTEGER DEFAULT 0,
  total_bookings INTEGER DEFAULT 0,
  response_time_hours INTEGER,  -- Avg response time
  availability_status VARCHAR(50) DEFAULT 'available',  -- 'available', 'partially_available', 'unavailable'
  portfolio_images TEXT[],  -- Image URLs
  certifications TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vendors_vendor_type ON vendors(vendor_type);
CREATE INDEX idx_vendors_location ON vendors(city, state);
CREATE INDEX idx_vendors_rating ON vendors(rating DESC);
CREATE INDEX idx_vendors_name_search ON vendors USING GIN(to_tsvector('english', name || ' ' || COALESCE(description, '')));
```

**Fields**:
- `id`: Unique vendor identifier
- `name`: Vendor business name
- `vendor_type`: Type of service provided
- `location`: Full address
- `city`, `state`, `country`: Geographic info
- `price_range`: Budget category
- `min_price`, `max_price`: Price bounds
- `rating`: Average rating (0-5)
- `review_count`: Number of reviews
- `availability_status`: Current availability
- `portfolio_images`: Sample work images
- `certifications`: Professional certifications

---

### 6. vendor_reviews

Customer reviews and ratings for vendors.

```sql
CREATE TABLE vendor_reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  event_id UUID REFERENCES events(id),
  rating INTEGER NOT NULL,  -- 1-5 scale
  title VARCHAR(255),
  review_text TEXT,
  helpfulness_score INTEGER DEFAULT 0,  -- Upvote count
  verified_booking BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vendor_reviews_vendor_id ON vendor_reviews(vendor_id);
CREATE INDEX idx_vendor_reviews_rating ON vendor_reviews(rating);
```

**Fields**:
- `id`: Unique review identifier
- `vendor_id`: Reviewed vendor
- `user_id`: Review author
- `event_id`: Associated event
- `rating`: Star rating (1-5)
- `title`: Review headline
- `review_text`: Detailed review
- `verified_booking`: Whether reviewer booked vendor

---

### 7. saved_vendors (User Favorites)

Stores user's saved/favorite vendors.

```sql
CREATE TABLE saved_vendors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
  event_id UUID REFERENCES events(id),
  notes TEXT,
  price_quote DECIMAL(12, 2),
  status VARCHAR(50) DEFAULT 'saved',  -- 'saved', 'contacted', 'quoted', 'booked', 'rejected'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, vendor_id, event_id)
);

CREATE INDEX idx_saved_vendors_user_id ON saved_vendors(user_id);
CREATE INDEX idx_saved_vendors_event_id ON saved_vendors(event_id);
```

**Fields**:
- `id`: Unique saved vendor record
- `user_id`: User who saved vendor
- `vendor_id`: Saved vendor
- `event_id`: Associated event
- `notes`: User's personal notes
- `price_quote`: Quoted price from vendor
- `status`: Vendor interaction status

---

### 8. budget_transactions

Tracks all expense entries for event budgeting.

```sql
CREATE TABLE budget_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  vendor_id UUID REFERENCES vendors(id),
  category VARCHAR(100) NOT NULL,  -- 'venue', 'catering', 'decoration', etc.
  description VARCHAR(255),
  amount DECIMAL(12, 2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  transaction_type VARCHAR(20) DEFAULT 'expense',  -- 'expense', 'income'
  status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'paid', 'refunded'
  payment_method VARCHAR(50),  -- 'cash', 'card', 'check', 'bank_transfer'
  paid_date DATE,
  due_date DATE,
  notes TEXT,
  receipt_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_budget_transactions_event_id ON budget_transactions(event_id);
CREATE INDEX idx_budget_transactions_category ON budget_transactions(category);
CREATE INDEX idx_budget_transactions_status ON budget_transactions(status);
```

**Fields**:
- `id`: Unique transaction identifier
- `event_id`: Associated event
- `user_id`: Entered by user
- `vendor_id`: Optional vendor link
- `category`: Expense category
- `amount`: Transaction amount
- `status`: Payment status
- `payment_method`: How payment was made
- `receipt_url`: Proof of payment

---

### 9. event_collaborators

Team members and permissions for events.

```sql
CREATE TABLE event_collaborators (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(50) DEFAULT 'collaborator',  -- 'owner', 'admin', 'collaborator', 'viewer'
  can_edit BOOLEAN DEFAULT false,
  can_delete BOOLEAN DEFAULT false,
  can_manage_budget BOOLEAN DEFAULT false,
  can_manage_vendors BOOLEAN DEFAULT false,
  invited_at TIMESTAMP DEFAULT NOW(),
  joined_at TIMESTAMP,
  deleted_at TIMESTAMP,
  UNIQUE(event_id, user_id)
);

CREATE INDEX idx_event_collaborators_event_id ON event_collaborators(event_id);
CREATE INDEX idx_event_collaborators_user_id ON event_collaborators(user_id);
```

**Fields**:
- `id`: Unique collaboration record
- `event_id`: Associated event
- `user_id`: Collaborator
- `role`: Permission level
- `can_*`: Specific permissions
- `invited_at`: When invited
- `joined_at`: When accepted invite

---

### 10. vendor_comparisons

Stores vendor comparison snapshots for user reference.

```sql
CREATE TABLE vendor_comparisons (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  vendor_ids UUID[] NOT NULL,  -- Array of vendor IDs
  name VARCHAR(255),  -- User-named comparison
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vendor_comparisons_user_id ON vendor_comparisons(user_id);
CREATE INDEX idx_vendor_comparisons_event_id ON vendor_comparisons(event_id);
```

**Fields**:
- `id`: Unique comparison record
- `user_id`: Comparison creator
- `event_id`: Associated event
- `vendor_ids`: Array of compared vendors
- `name`: User-provided name for comparison
- `notes`: Comparison notes

---

### 11. notifications

Stores in-app and email notification logs.

```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  notification_type VARCHAR(50),  -- 'event', 'task', 'vendor', 'budget', 'system'
  related_entity_type VARCHAR(50),  -- 'event', 'task', 'vendor'
  related_entity_id UUID,
  is_read BOOLEAN DEFAULT false,
  read_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);
```

---

## Relationships Diagram

```
users (1) ──→ (many) events
     ├──→ (many) tasks
     ├──→ (many) vendor_reviews
     ├──→ (many) saved_vendors
     └──→ (many) budget_transactions

events (1) ──→ (many) event_ai_plans
      ├──→ (many) tasks
      ├──→ (many) budget_transactions
      ├──→ (many) saved_vendors
      ├──→ (many) event_collaborators
      └──→ (many) vendor_comparisons

vendors (1) ──→ (many) vendor_reviews
       ├──→ (many) saved_vendors
       └──→ (many) budget_transactions

event_collaborators links users ←→ events (many-to-many with roles)
vendor_comparisons links vendors ←→ events (many-to-many)
```

## Row-Level Security (RLS) Policies

### users table
- Users can only read/update their own profile
- Admin can read all users

### events table
- Users can only access events they created or collaborate on
- Collaborators have read access (or edit based on role)

### tasks table
- Only event collaborators can view/modify tasks
- Assignee receives notifications

### saved_vendors, budget_transactions
- Users can only access records for their own events

### vendors table
- Public read access for all users
- Only admin/vendor can modify

### vendor_reviews
- Users can read all reviews
- Users can only write/modify their own reviews

## Indexing Strategy

```
Primary Indices:
- idx_users_email (B-tree) - Auth lookups
- idx_events_user_id (B-tree) - User's events
- idx_events_start_date (B-tree) - Timeline queries
- idx_events_status (B-tree) - Filter by status
- idx_tasks_event_id (B-tree) - Event's tasks
- idx_tasks_status (B-tree) - Task filtering
- idx_vendors_vendor_type (B-tree) - Type filtering
- idx_vendors_location (B-tree) - Location search
- idx_vendors_rating (B-tree DESC) - Top vendors
- idx_vendors_name_search (GIN) - Full-text search

Secondary Indices:
- Foreign key indices (automatic in PostgreSQL)
- Timestamp indices for sorting
- Status/state column indices
```

## Future Schema Enhancements

- **Audit Trail**: audit_logs table for compliance
- **File Storage**: files table for vendor portfolios
- **Real-time Chat**: messages table for vendor communication
- **Payment Integration**: payment_records table for transactions
- **Analytics**: event_metrics table for data warehouse
- **Integrations**: external_integrations table for third-party services
