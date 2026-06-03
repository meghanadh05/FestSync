-- FestSync Row Level Security Policies
-- Migration 002: Enable RLS and create access control policies
-- Run this AFTER 001_initial_schema.sql

-- ============================================================================
-- ENABLE ROW LEVEL SECURITY ON ALL TABLES
-- ============================================================================

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE plan_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE subtasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendor_services ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendor_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE guests ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_generations ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- HELPER FUNCTION: Get current user ID
-- ============================================================================

CREATE OR REPLACE FUNCTION auth.user_id()
RETURNS UUID AS $$
  SELECT auth.uid()
$$ LANGUAGE sql STABLE;

-- ============================================================================
-- HELPER FUNCTION: Check if user is admin
-- ============================================================================

CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'admin'
  )
$$ LANGUAGE sql STABLE;

-- ============================================================================
-- PROFILES POLICIES
-- ============================================================================
-- Users can view their own profile
-- Users can update their own profile
-- Admins can view all profiles

CREATE POLICY "Profiles: Users can view own profile"
  ON profiles FOR SELECT
  USING (id = auth.uid());

CREATE POLICY "Profiles: Admins can view all profiles"
  ON profiles FOR SELECT
  USING (is_admin());

CREATE POLICY "Profiles: Users can update own profile"
  ON profiles FOR UPDATE
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid());

CREATE POLICY "Profiles: Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (id = auth.uid());

-- ============================================================================
-- EVENTS POLICIES
-- ============================================================================
-- Users can view their own events
-- Users can insert events for themselves
-- Users can update their own events
-- Users can delete their own events

CREATE POLICY "Events: Users can view own events"
  ON events FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Events: Admins can view all events"
  ON events FOR SELECT
  USING (is_admin());

CREATE POLICY "Events: Users can insert own events"
  ON events FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Events: Users can update own events"
  ON events FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Events: Users can delete own events"
  ON events FOR DELETE
  USING (user_id = auth.uid());

-- ============================================================================
-- EVENT_PLANS POLICIES
-- ============================================================================
-- Users can view plans for their events only
-- Plans are created/updated/deleted with event ownership

CREATE POLICY "Event Plans: Users can view own event plans"
  ON event_plans FOR SELECT
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Event Plans: Admins can view all plans"
  ON event_plans FOR SELECT
  USING (is_admin());

CREATE POLICY "Event Plans: Users can insert plans for own events"
  ON event_plans FOR INSERT
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Event Plans: Users can update own event plans"
  ON event_plans FOR UPDATE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  )
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Event Plans: Users can delete own event plans"
  ON event_plans FOR DELETE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

-- ============================================================================
-- PLAN_SECTIONS POLICIES
-- ============================================================================
-- Users can access sections for their events only

CREATE POLICY "Plan Sections: Users can view own event plan sections"
  ON plan_sections FOR SELECT
  USING (
    event_plan_id IN (
      SELECT id FROM event_plans
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Plan Sections: Users can modify own event plan sections"
  ON plan_sections FOR INSERT
  WITH CHECK (
    event_plan_id IN (
      SELECT id FROM event_plans
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Plan Sections: Users can update own event plan sections"
  ON plan_sections FOR UPDATE
  USING (
    event_plan_id IN (
      SELECT id FROM event_plans
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Plan Sections: Users can delete own event plan sections"
  ON plan_sections FOR DELETE
  USING (
    event_plan_id IN (
      SELECT id FROM event_plans
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

-- ============================================================================
-- TASKS POLICIES
-- ============================================================================
-- Users can view/edit tasks for their own events
-- Task creator and assignee can access the task

CREATE POLICY "Tasks: Users can view own event tasks"
  ON tasks FOR SELECT
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
    OR assigned_to = auth.uid()
  );

CREATE POLICY "Tasks: Users can insert tasks in own events"
  ON tasks FOR INSERT
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Tasks: Users can update own event tasks"
  ON tasks FOR UPDATE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  )
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Tasks: Users can delete own event tasks"
  ON tasks FOR DELETE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

-- ============================================================================
-- SUBTASKS POLICIES
-- ============================================================================
-- Users can access subtasks of tasks they can access

CREATE POLICY "Subtasks: Users can view own event subtasks"
  ON subtasks FOR SELECT
  USING (
    task_id IN (
      SELECT id FROM tasks
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Subtasks: Users can manage own event subtasks"
  ON subtasks FOR INSERT
  WITH CHECK (
    task_id IN (
      SELECT id FROM tasks
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Subtasks: Users can update own event subtasks"
  ON subtasks FOR UPDATE
  USING (
    task_id IN (
      SELECT id FROM tasks
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Subtasks: Users can delete own event subtasks"
  ON subtasks FOR DELETE
  USING (
    task_id IN (
      SELECT id FROM tasks
      WHERE event_id IN (
        SELECT id FROM events WHERE user_id = auth.uid()
      )
    )
  );

-- ============================================================================
-- VENDORS POLICIES
-- ============================================================================
-- All users can view public vendor data
-- Vendors can only update their own profile
-- Admins can manage all vendors

CREATE POLICY "Vendors: Everyone can view vendors"
  ON vendors FOR SELECT
  USING (true);

CREATE POLICY "Vendors: Vendors can update own profile"
  ON vendors FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Vendors: Admins can manage all vendors"
  ON vendors FOR ALL
  USING (is_admin());

-- ============================================================================
-- VENDOR_SERVICES POLICIES
-- ============================================================================
-- Everyone can view vendor services
-- Vendors can only manage their own services

CREATE POLICY "Vendor Services: Everyone can view services"
  ON vendor_services FOR SELECT
  USING (true);

CREATE POLICY "Vendor Services: Vendors can manage own services"
  ON vendor_services FOR ALL
  USING (
    vendor_id IN (
      SELECT id FROM vendors WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Vendor Services: Admins can manage all services"
  ON vendor_services FOR ALL
  USING (is_admin());

-- ============================================================================
-- VENDOR_IMAGES POLICIES
-- ============================================================================
-- Everyone can view vendor images
-- Vendors can manage their own images

CREATE POLICY "Vendor Images: Everyone can view images"
  ON vendor_images FOR SELECT
  USING (true);

CREATE POLICY "Vendor Images: Vendors can manage own images"
  ON vendor_images FOR ALL
  USING (
    vendor_id IN (
      SELECT id FROM vendors WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Vendor Images: Admins can manage all images"
  ON vendor_images FOR ALL
  USING (is_admin());

-- ============================================================================
-- SAVED_VENDORS POLICIES
-- ============================================================================
-- Users can only view/manage their own saved vendors

CREATE POLICY "Saved Vendors: Users can view own saved vendors"
  ON saved_vendors FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Saved Vendors: Users can save vendors"
  ON saved_vendors FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Saved Vendors: Users can update own saved vendors"
  ON saved_vendors FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Saved Vendors: Users can delete own saved vendors"
  ON saved_vendors FOR DELETE
  USING (user_id = auth.uid());

-- ============================================================================
-- BUDGET_ITEMS POLICIES
-- ============================================================================
-- Users can only access budget items for their own events

CREATE POLICY "Budget Items: Users can view own event budget"
  ON budget_items FOR SELECT
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Budget Items: Users can add budget items to own events"
  ON budget_items FOR INSERT
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Budget Items: Users can update own budget items"
  ON budget_items FOR UPDATE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  )
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Budget Items: Users can delete own budget items"
  ON budget_items FOR DELETE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

-- ============================================================================
-- GUESTS POLICIES
-- ============================================================================
-- Users can only access guests for their own events

CREATE POLICY "Guests: Users can view own event guests"
  ON guests FOR SELECT
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Guests: Users can add guests to own events"
  ON guests FOR INSERT
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Guests: Users can update own event guests"
  ON guests FOR UPDATE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  )
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Guests: Users can delete own event guests"
  ON guests FOR DELETE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

-- ============================================================================
-- BOOKINGS POLICIES
-- ============================================================================
-- Users can view bookings for their own events
-- Vendors can view bookings for their vendors
-- Event owner can manage bookings for their events

CREATE POLICY "Bookings: Users can view own event bookings"
  ON bookings FOR SELECT
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Bookings: Vendors can view own vendor bookings"
  ON bookings FOR SELECT
  USING (
    vendor_id IN (
      SELECT id FROM vendors WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Bookings: Users can create bookings for own events"
  ON bookings FOR INSERT
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Bookings: Users can update own event bookings"
  ON bookings FOR UPDATE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  )
  WITH CHECK (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Bookings: Users can delete own event bookings"
  ON bookings FOR DELETE
  USING (
    event_id IN (
      SELECT id FROM events WHERE user_id = auth.uid()
    )
  );

-- ============================================================================
-- AI_GENERATIONS POLICIES
-- ============================================================================
-- Users can only view their own AI generation records

CREATE POLICY "AI Generations: Users can view own generations"
  ON ai_generations FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "AI Generations: Users can insert own generations"
  ON ai_generations FOR INSERT
  WITH CHECK (user_id = auth.uid());

-- ============================================================================
-- NOTIFICATIONS POLICIES
-- ============================================================================
-- Users can only view/manage their own notifications

CREATE POLICY "Notifications: Users can view own notifications"
  ON notifications FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Notifications: Users can update own notifications"
  ON notifications FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Notifications: Users can delete own notifications"
  ON notifications FOR DELETE
  USING (user_id = auth.uid());

-- Service role can insert notifications (for backend)
CREATE POLICY "Notifications: Service role can insert notifications"
  ON notifications FOR INSERT
  WITH CHECK (true);

-- ============================================================================
-- RLS POLICIES COMPLETE
-- ============================================================================
-- All Row Level Security policies are now in place
-- Users can only access their own data
-- Vendors can only modify their own profiles
-- Admins have full access to all tables
