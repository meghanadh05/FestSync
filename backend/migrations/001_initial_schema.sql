-- FestSync Initial Database Schema
-- Migration 001: Create all base tables with constraints and indexes
-- Run this in Supabase SQL Editor

-- ============================================================================
-- PROFILES TABLE
-- ============================================================================
-- Extended user profile data. References Supabase auth.users table.
-- Stores user role (admin, vendor, user) for access control.

CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name VARCHAR(255),
  email VARCHAR(255) UNIQUE NOT NULL,
  phone_number VARCHAR(20),
  avatar_url TEXT,
  bio TEXT,
  role VARCHAR(50) NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'vendor', 'admin')),
  location VARCHAR(255),
  website_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_profiles_email ON profiles(email);
CREATE INDEX idx_profiles_role ON profiles(role);

-- ============================================================================
-- EVENTS TABLE
-- ============================================================================
-- User-created events (weddings, birthdays, corporate events, etc.)
-- Tracks event lifecycle: planning → ongoing → completed/cancelled

CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  event_type VARCHAR(50) NOT NULL CHECK (event_type IN (
    'wedding', 'birthday', 'corporate', 'college_fest', 'conference', 'custom'
  )),
  status VARCHAR(50) NOT NULL DEFAULT 'planning' CHECK (status IN (
    'planning', 'ongoing', 'completed', 'cancelled'
  )),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  location VARCHAR(255),
  estimated_guests INTEGER,
  budget DECIMAL(12, 2),
  currency VARCHAR(10) DEFAULT 'USD',
  thumbnail_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_start_date ON events(start_date);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_event_type ON events(event_type);
CREATE INDEX idx_events_user_status ON events(user_id, status);

-- ============================================================================
-- EVENT_PLANS TABLE
-- ============================================================================
-- AI-generated event plans stored as JSON for flexibility
-- Tracks plan versions and regenerations

CREATE TABLE event_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL UNIQUE REFERENCES events(id) ON DELETE CASCADE,
  plan_content JSONB NOT NULL,
  timeline JSONB,
  budget_breakdown JSONB,
  vendor_suggestions JSONB,
  generated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  regenerated_at TIMESTAMP WITH TIME ZONE,
  version INTEGER DEFAULT 1 NOT NULL
);

CREATE INDEX idx_event_plans_event_id ON event_plans(event_id);
CREATE INDEX idx_event_plans_generated_at ON event_plans(generated_at DESC);

-- ============================================================================
-- PLAN_SECTIONS TABLE
-- ============================================================================
-- Structured breakdown of event plan sections (timeline, checklist, budget)
-- Allows flexible organization and editing of plan components

CREATE TABLE plan_sections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_plan_id UUID NOT NULL REFERENCES event_plans(id) ON DELETE CASCADE,
  section_type VARCHAR(50) NOT NULL CHECK (section_type IN (
    'timeline', 'checklist', 'budget', 'vendors', 'guests', 'notes'
  )),
  title VARCHAR(255) NOT NULL,
  content TEXT,
  data JSONB,
  order_index INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_plan_sections_event_plan_id ON plan_sections(event_plan_id);
CREATE INDEX idx_plan_sections_section_type ON plan_sections(section_type);
CREATE INDEX idx_plan_sections_order ON plan_sections(event_plan_id, order_index);

-- ============================================================================
-- TASKS TABLE
-- ============================================================================
-- Event tasks/to-dos with assignment, priority, and status tracking
-- Categories: venue, catering, decoration, entertainment, transportation, etc.

CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN (
    'pending', 'in_progress', 'completed', 'cancelled'
  )),
  priority VARCHAR(20) NOT NULL DEFAULT 'medium' CHECK (priority IN (
    'low', 'medium', 'high', 'urgent'
  )),
  category VARCHAR(100),
  due_date DATE,
  assigned_to UUID REFERENCES profiles(id) ON DELETE SET NULL,
  tags TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_tasks_event_id ON tasks(event_id);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_event_status ON tasks(event_id, status);

-- ============================================================================
-- SUBTASKS TABLE
-- ============================================================================
-- Nested subtasks within parent tasks for granular task management

CREATE TABLE subtasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  order_index INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_subtasks_task_id ON subtasks(task_id);
CREATE INDEX idx_subtasks_completed ON subtasks(completed);

-- ============================================================================
-- VENDORS TABLE
-- ============================================================================
-- Vendor profiles with ratings, pricing, and availability info
-- Can be created by platform (public vendors) or by vendor users

CREATE TABLE vendors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  vendor_type VARCHAR(50) NOT NULL CHECK (vendor_type IN (
    'catering', 'venue', 'photography', 'decoration', 'music', 'event_planner',
    'transportation', 'accommodation', 'invitations', 'cake', 'florist', 'entertainment'
  )),
  location VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  phone_number VARCHAR(20),
  email VARCHAR(255),
  website_url TEXT,
  social_media JSONB,
  price_range VARCHAR(50) CHECK (price_range IN ('budget', 'mid-range', 'premium')),
  min_price DECIMAL(12, 2),
  max_price DECIMAL(12, 2),
  rating DECIMAL(3, 2) DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
  review_count INTEGER DEFAULT 0,
  total_bookings INTEGER DEFAULT 0,
  response_time_hours INTEGER,
  availability_status VARCHAR(50) DEFAULT 'available' CHECK (availability_status IN (
    'available', 'partially_available', 'unavailable'
  )),
  certifications TEXT[],
  is_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_vendors_vendor_type ON vendors(vendor_type);
CREATE INDEX idx_vendors_city ON vendors(city);
CREATE INDEX idx_vendors_rating ON vendors(rating DESC);
CREATE INDEX idx_vendors_user_id ON vendors(user_id);
CREATE INDEX idx_vendors_availability ON vendors(availability_status);
CREATE INDEX idx_vendors_name_city_type ON vendors(name, city, vendor_type);

-- ============================================================================
-- VENDOR_SERVICES TABLE
-- ============================================================================
-- Specific services offered by each vendor with pricing and availability

CREATE TABLE vendor_services (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(12, 2),
  duration VARCHAR(100),
  available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_vendor_services_vendor_id ON vendor_services(vendor_id);
CREATE INDEX idx_vendor_services_available ON vendor_services(available);

-- ============================================================================
-- VENDOR_IMAGES TABLE
-- ============================================================================
-- Portfolio/portfolio images for vendors displayed in search and detail views

CREATE TABLE vendor_images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  caption TEXT,
  order_index INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_vendor_images_vendor_id ON vendor_images(vendor_id);
CREATE INDEX idx_vendor_images_order ON vendor_images(vendor_id, order_index);

-- ============================================================================
-- SAVED_VENDORS TABLE
-- ============================================================================
-- User's saved/favorite vendors for specific events
-- Tracks interaction status: saved, contacted, quoted, booked, rejected

CREATE TABLE saved_vendors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  notes TEXT,
  price_quote DECIMAL(12, 2),
  status VARCHAR(50) DEFAULT 'saved' CHECK (status IN (
    'saved', 'contacted', 'quoted', 'booked', 'rejected'
  )),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  UNIQUE(user_id, vendor_id, event_id)
);

CREATE INDEX idx_saved_vendors_user_id ON saved_vendors(user_id);
CREATE INDEX idx_saved_vendors_vendor_id ON saved_vendors(vendor_id);
CREATE INDEX idx_saved_vendors_event_id ON saved_vendors(event_id);
CREATE INDEX idx_saved_vendors_status ON saved_vendors(status);
CREATE INDEX idx_saved_vendors_user_event ON saved_vendors(user_id, event_id);

-- ============================================================================
-- BUDGET_ITEMS TABLE
-- ============================================================================
-- Expense tracking with payment status and optional vendor linkage
-- Categories: venue, catering, decoration, photography, music, transportation, etc.

CREATE TABLE budget_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  vendor_id UUID REFERENCES vendors(id) ON DELETE SET NULL,
  category VARCHAR(100) NOT NULL,
  description VARCHAR(255),
  amount DECIMAL(12, 2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  transaction_type VARCHAR(20) DEFAULT 'expense' CHECK (transaction_type IN (
    'expense', 'income'
  )),
  status VARCHAR(50) DEFAULT 'pending' CHECK (status IN (
    'pending', 'paid', 'refunded'
  )),
  payment_method VARCHAR(50) CHECK (payment_method IN (
    'cash', 'card', 'check', 'bank_transfer', 'other'
  )),
  paid_date DATE,
  due_date DATE,
  receipt_url TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_budget_items_event_id ON budget_items(event_id);
CREATE INDEX idx_budget_items_user_id ON budget_items(user_id);
CREATE INDEX idx_budget_items_category ON budget_items(category);
CREATE INDEX idx_budget_items_status ON budget_items(status);
CREATE INDEX idx_budget_items_event_category ON budget_items(event_id, category);
CREATE INDEX idx_budget_items_paid_date ON budget_items(paid_date);

-- ============================================================================
-- GUESTS TABLE
-- ============================================================================
-- Event guest list with RSVP tracking and dietary restrictions

CREATE TABLE guests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(20),
  dietary_restrictions TEXT,
  rsvp_status VARCHAR(50) DEFAULT 'pending' CHECK (rsvp_status IN (
    'pending', 'accepted', 'declined', 'maybe'
  )),
  plus_ones INTEGER DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_guests_event_id ON guests(event_id);
CREATE INDEX idx_guests_rsvp_status ON guests(rsvp_status);
CREATE INDEX idx_guests_email ON guests(email);

-- ============================================================================
-- BOOKINGS TABLE
-- ============================================================================
-- Vendor bookings for events with payment tracking
-- Tracks deposit and balance payment status separately

CREATE TABLE bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  service_id UUID REFERENCES vendor_services(id) ON DELETE SET NULL,
  booking_date DATE NOT NULL,
  service_date DATE NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN (
    'pending', 'confirmed', 'completed', 'cancelled'
  )),
  amount DECIMAL(12, 2) NOT NULL,
  deposit_paid BOOLEAN DEFAULT FALSE,
  deposit_amount DECIMAL(12, 2),
  balance_amount DECIMAL(12, 2),
  payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN (
    'pending', 'partial', 'full'
  )),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_bookings_event_id ON bookings(event_id);
CREATE INDEX idx_bookings_vendor_id ON bookings(vendor_id);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_payment_status ON bookings(payment_status);
CREATE INDEX idx_bookings_service_date ON bookings(service_date);

-- ============================================================================
-- AI_GENERATIONS TABLE
-- ============================================================================
-- Track AI API calls for analytics, cost monitoring, and debugging

CREATE TABLE ai_generations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL CHECK (type IN (
    'event_plan', 'recommendation', 'timeline', 'budget_suggestion', 'other'
  )),
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  total_tokens INTEGER,
  model VARCHAR(100),
  cost DECIMAL(10, 6),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_ai_generations_event_id ON ai_generations(event_id);
CREATE INDEX idx_ai_generations_user_id ON ai_generations(user_id);
CREATE INDEX idx_ai_generations_created_at ON ai_generations(created_at DESC);
CREATE INDEX idx_ai_generations_type ON ai_generations(type);

-- ============================================================================
-- NOTIFICATIONS TABLE
-- ============================================================================
-- In-app notifications for events, tasks, vendor communications, etc.

CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  type VARCHAR(50) CHECK (type IN (
    'event', 'task', 'vendor', 'budget', 'booking', 'system'
  )),
  related_entity_type VARCHAR(50),
  related_entity_id UUID,
  is_read BOOLEAN DEFAULT FALSE,
  read_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);
CREATE INDEX idx_notifications_user_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================================================
-- Automatically update the updated_at timestamp on row modification

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = TIMEZONE('utc'::text, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_event_plans_updated_at BEFORE UPDATE ON event_plans
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_plan_sections_updated_at BEFORE UPDATE ON plan_sections
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subtasks_updated_at BEFORE UPDATE ON subtasks
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vendors_updated_at BEFORE UPDATE ON vendors
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vendor_services_updated_at BEFORE UPDATE ON vendor_services
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_saved_vendors_updated_at BEFORE UPDATE ON saved_vendors
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_budget_items_updated_at BEFORE UPDATE ON budget_items
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_guests_updated_at BEFORE UPDATE ON guests
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================
-- All tables created successfully with proper constraints and indexes
-- Next step: Run 002_rls_policies.sql for Row Level Security setup
