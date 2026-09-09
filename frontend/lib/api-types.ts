// API types — mirrors backend Pydantic schemas exactly.
// Frontend's types/index.ts keeps UI-layer types; this file is the API contract.

export type EventTypeAPI =
  | 'WEDDING' | 'BIRTHDAY' | 'COLLEGE_FEST' | 'CORPORATE_EVENT'
  | 'CONFERENCE' | 'RECEPTION' | 'ENGAGEMENT' | 'CONCERT' | 'OTHER';

export type EventStatusAPI = 'PLANNING' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';

export type TaskStatusAPI = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
export type TaskPriorityAPI = 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';

export type VendorCategoryAPI =
  | 'CATERING' | 'VENUE' | 'PHOTOGRAPHY' | 'VIDEOGRAPHY' | 'DECORATION'
  | 'MUSIC' | 'DJ' | 'FLORIST' | 'BAKERY' | 'TRANSPORT' | 'MAKEUP'
  | 'ATTIRE' | 'EVENT_PLANNER' | 'SECURITY' | 'LIGHTING' | 'OTHER';

export type WorkspaceRoleAPI = 'OWNER' | 'ADMIN' | 'PLANNER' | 'MEMBER' | 'VIEWER';

// ---- Workspaces ------------------------------------------------------------

export interface APIWorkspace {
  id: string;
  name: string;
  organization: string | null;
  country: string;
  currency: string;
  timezone: string;
  created_by: string;
  created_at: string;
  updated_at: string;
  role: WorkspaceRoleAPI;
}

export interface APIWorkspaceList {
  total: number;
  items: APIWorkspace[];
}

export interface CreateWorkspacePayload {
  name: string;
  organization?: string;
  country?: string;
  currency?: string;
  timezone?: string;
}

// ---- Events ----------------------------------------------------------------

export interface APIEvent {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  event_type: EventTypeAPI;
  status: EventStatusAPI;
  start_date: string;
  end_date: string;
  location: string | null;
  estimated_guests: number | null;
  budget: number | null;
  currency: string;
  thumbnail_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface APIEventList {
  total: number;
  skip: number;
  limit: number;
  items: APIEvent[];
}

export interface APIEventDashboard {
  event: APIEvent;
  tasks_total: number;
  tasks_completed: number;
  tasks_completion_percentage: number;
  budget_total: number;
  budget_spent: number;
  budget_remaining: number;
  budget_percentage_used: number;
  vendors_saved: number;
  guests_count: number;
  days_remaining: number;
  progress_percentage: number;
}

export interface CreateEventPayload {
  title: string;
  event_type: EventTypeAPI;
  start_date: string;
  end_date: string;
  description?: string;
  location?: string;
  estimated_guests?: number;
  budget?: number;
  currency?: string;
  thumbnail_url?: string;
}

export interface UpdateEventPayload extends Partial<CreateEventPayload> {
  status?: EventStatusAPI;
}

// ---- Tasks -----------------------------------------------------------------

export interface APISubtask {
  id: string;
  task_id: string;
  title: string;
  description: string | null;
  status: TaskStatusAPI;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface APITask {
  id: string;
  event_id: string;
  title: string;
  description: string | null;
  status: TaskStatusAPI;
  priority: TaskPriorityAPI;
  category: string | null;
  due_date: string | null;
  assigned_to: string | null;
  ai_generated: boolean;
  created_at: string;
  updated_at: string;
  subtasks: APISubtask[];
}

export interface APITaskList {
  total: number;
  skip: number;
  limit: number;
  items: APITask[];
}

export interface APIKanbanBoard {
  pending: APITask[];
  in_progress: APITask[];
  completed: APITask[];
}

export interface CreateTaskPayload {
  title: string;
  description?: string;
  priority?: TaskPriorityAPI;
  category?: string;
  due_date?: string;
  assigned_to?: string;
}

export interface UpdateTaskPayload extends Partial<CreateTaskPayload> {
  status?: TaskStatusAPI;
}

// ---- Budget ----------------------------------------------------------------

export interface APIBudgetItem {
  id: string;
  event_id: string;
  category: string;
  planned_amount: number;
  actual_amount: number;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface APIBudgetList {
  total: number;
  skip: number;
  limit: number;
  items: APIBudgetItem[];
}

export interface APIOverBudgetCategory {
  category: string;
  planned_amount: number;
  actual_amount: number;
  overage: number;
}

export interface APIBudgetSummary {
  total_budget: number;
  total_planned: number;
  total_actual: number;
  remaining_budget: number;
  budget_percentage_used: number;
  over_budget_categories: APIOverBudgetCategory[];
  budget_health_status: 'GOOD' | 'WARNING' | 'OVER_BUDGET';
  currency: string;
}

export interface CreateBudgetItemPayload {
  category: string;
  planned_amount: number;
  actual_amount?: number;
  notes?: string;
}

export interface UpdateBudgetItemPayload {
  category?: string;
  planned_amount?: number;
  actual_amount?: number;
  notes?: string;
}

// ---- Vendors ---------------------------------------------------------------

export interface APIVendorService {
  id: string;
  vendor_id: string;
  name: string;
  description: string | null;
  price: number | null;
  unit: string | null;
  created_at: string;
  updated_at: string;
}

export interface APIVendorImage {
  id: string;
  vendor_id: string;
  url: string;
  caption: string | null;
  is_primary: boolean;
}

export interface APIVendorCard {
  id: string;
  business_name: string;
  category: VendorCategoryAPI;
  location: string;
  city: string | null;
  starting_price: number | null;
  currency: string;
  rating: number;
  review_count: number;
  verified: boolean;
  primary_image_url: string | null;
  match_score: number;
  match_reason: string;
}

export interface APIVendorFull extends APIVendorCard {
  owner_user_id: string | null;
  description: string | null;
  state: string | null;
  country: string | null;
  email: string | null;
  phone: string | null;
  website: string | null;
  supported_event_types: string[] | null;
  active: boolean;
  created_at: string;
  updated_at: string;
  services: APIVendorService[];
  images: APIVendorImage[];
}

export interface APIVendorSearch {
  total: number;
  skip: number;
  limit: number;
  items: APIVendorCard[];
}

export interface APISavedVendor {
  id: string;
  event_id: string;
  vendor_id: string;
  user_id: string;
  notes: string | null;
  created_at: string;
  vendor: APIVendorCard;
}

export interface APISavedVendorList {
  total: number;
  items: APISavedVendor[];
}

// ---- AI --------------------------------------------------------------------

export interface AIGenerationMeta {
  generation_id: string;
  agent_type: string;
  model_used: string | null;
  created_at: string;
}

export interface AIPlanSection {
  title: string;
  content: string;
  section_type: string;
}

export interface AITimelineItem {
  title: string;
  due_date: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface APIEventPlanResult {
  summary: string;
  plan_sections: AIPlanSection[];
  timeline: AITimelineItem[];
  vendor_categories_needed: string[];
  risk_notes: string[];
}

export interface APITaskGeneratorResult {
  tasks: {
    title: string;
    description: string | null;
    category: string | null;
    priority: TaskPriorityAPI;
    due_date: string | null;
  }[];
}

export interface APIBudgetAdviceResult {
  budget_split: { category: string; recommended_amount: number; reason: string }[];
  warnings: string[];
  saving_tips: string[];
}

export interface APIVendorRecommendationResult {
  recommendations: {
    vendor_id: string;
    match_score: number;
    reason: string;
    pros: string[];
    cons: string[];
  }[];
}

export interface APIChatResult {
  message: string;
  suggestions: string[];
}

// Generic AI response wrapper
export interface AIResponse<T> {
  meta: AIGenerationMeta;
  result: T;
}

// ---- Errors ----------------------------------------------------------------

export interface APIError {
  detail: string;
}
