export type UserRole = 'user' | 'vendor' | 'admin';

export type EventType = 'wedding' | 'birthday' | 'corporate' | 'college_fest' | 'conference' | 'custom';

export type EventStatus = 'planning' | 'ongoing' | 'completed' | 'cancelled';

export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled';

export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent';

export type VendorType =
  | 'catering'
  | 'venue'
  | 'photography'
  | 'decoration'
  | 'music'
  | 'event_planner'
  | 'transportation'
  | 'accommodation'
  | 'invitations'
  | 'cake'
  | 'florist'
  | 'entertainment';

export type PriceRange = 'budget' | 'mid-range' | 'premium';

export type SavedVendorStatus = 'saved' | 'contacted' | 'quoted' | 'booked' | 'rejected';

export type BookingStatus = 'pending' | 'confirmed' | 'completed' | 'cancelled';

export type PaymentStatus = 'pending' | 'partial' | 'full';

export interface User {
  id: string;
  email: string;
  full_name: string;
  phone_number?: string;
  avatar_url?: string;
  bio?: string;
  role: UserRole;
  location?: string;
  website_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Event {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  event_type: EventType;
  status: EventStatus;
  start_date: string;
  end_date: string;
  location?: string;
  estimated_guests?: number;
  budget?: number;
  currency: string;
  thumbnail_url?: string;
  created_at: string;
  updated_at: string;
}

export interface EventPlan {
  id: string;
  event_id: string;
  plan_content: Record<string, unknown>;
  timeline?: Record<string, unknown>;
  budget_breakdown?: Record<string, number>;
  vendor_suggestions?: string[];
  generated_at: string;
  regenerated_at?: string;
  version: number;
}

export interface Task {
  id: string;
  event_id: string;
  user_id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  category?: string;
  due_date?: string;
  assigned_to?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface Subtask {
  id: string;
  task_id: string;
  title: string;
  completed: boolean;
  order_index: number;
  created_at: string;
  updated_at: string;
}

export interface Vendor {
  id: string;
  user_id?: string;
  name: string;
  description?: string;
  vendor_type: VendorType;
  location?: string;
  city?: string;
  state?: string;
  country?: string;
  phone_number?: string;
  email?: string;
  website_url?: string;
  social_media?: Record<string, string>;
  price_range?: PriceRange;
  min_price?: number;
  max_price?: number;
  rating: number;
  review_count: number;
  total_bookings: number;
  response_time_hours?: number;
  availability_status: string;
  certifications?: string[];
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface VendorService {
  id: string;
  vendor_id: string;
  name: string;
  description?: string;
  price?: number;
  duration?: string;
  available: boolean;
  created_at: string;
  updated_at: string;
}

export interface VendorImage {
  id: string;
  vendor_id: string;
  image_url: string;
  caption?: string;
  order_index: number;
  created_at: string;
}

export interface SavedVendor {
  id: string;
  user_id: string;
  vendor_id: string;
  event_id: string;
  notes?: string;
  price_quote?: number;
  status: SavedVendorStatus;
  created_at: string;
  updated_at: string;
}

export interface BudgetItem {
  id: string;
  event_id: string;
  user_id: string;
  vendor_id?: string;
  category: string;
  description?: string;
  amount: number;
  currency: string;
  transaction_type: 'expense' | 'income';
  status: 'pending' | 'paid' | 'refunded';
  payment_method?: string;
  paid_date?: string;
  due_date?: string;
  receipt_url?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Guest {
  id: string;
  event_id: string;
  name: string;
  email?: string;
  phone?: string;
  dietary_restrictions?: string;
  rsvp_status: 'pending' | 'accepted' | 'declined' | 'maybe';
  plus_ones: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Booking {
  id: string;
  event_id: string;
  vendor_id: string;
  user_id: string;
  service_id?: string;
  booking_date: string;
  service_date: string;
  status: BookingStatus;
  amount: number;
  deposit_paid: boolean;
  deposit_amount?: number;
  balance_amount?: number;
  payment_status: PaymentStatus;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  type?: 'event' | 'task' | 'vendor' | 'budget' | 'booking' | 'system';
  related_entity_type?: string;
  related_entity_id?: string;
  is_read: boolean;
  read_at?: string;
  created_at: string;
}
