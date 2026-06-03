// Centralized API client — all backend calls go through here.
// Auth token is injected automatically from Supabase session.

import { supabase } from './supabase';
import type {
  APIEvent, APIEventList, APIEventDashboard, CreateEventPayload, UpdateEventPayload,
  APITask, APITaskList, APIKanbanBoard, CreateTaskPayload, UpdateTaskPayload, APISubtask,
  APIBudgetItem, APIBudgetList, APIBudgetSummary, CreateBudgetItemPayload, UpdateBudgetItemPayload,
  APIVendorFull, APIVendorSearch, APISavedVendor, APISavedVendorList,
  AIResponse, APIEventPlanResult, APITaskGeneratorResult,
  APIBudgetAdviceResult, APIVendorRecommendationResult, APIChatResult,
} from './api-types';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

async function getAuthHeaders(): Promise<HeadersInit> {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session?.access_token) throw new APIError(401, 'Not authenticated');
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${session.access_token}`,
  };
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  requireAuth = true
): Promise<T> {
  const headers: HeadersInit = requireAuth
    ? await getAuthHeaders()
    : { 'Content-Type': 'application/json' };

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    try {
      const err = await res.json();
      message = err.detail ?? message;
    } catch {}
    throw new APIError(res.status, message);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

// ---- Events ----------------------------------------------------------------

export const eventsApi = {
  list: (params?: { skip?: number; limit?: number; search?: string; status?: string }) =>
    request<APIEventList>(`/events?${new URLSearchParams(params as Record<string, string>)}`),

  get: (id: string) =>
    request<APIEvent>(`/events/${id}`),

  dashboard: (id: string) =>
    request<APIEventDashboard>(`/events/${id}/dashboard`),

  create: (payload: CreateEventPayload) =>
    request<APIEvent>('/events', { method: 'POST', body: JSON.stringify(payload) }),

  update: (id: string, payload: UpdateEventPayload) =>
    request<APIEvent>(`/events/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),

  delete: (id: string) =>
    request<void>(`/events/${id}`, { method: 'DELETE' }),
};

// ---- Tasks -----------------------------------------------------------------

export const tasksApi = {
  list: (eventId: string, params?: { status?: string; priority?: string; category?: string; search?: string }) =>
    request<APITaskList>(`/events/${eventId}/tasks?${new URLSearchParams(params as Record<string, string>)}`),

  kanban: (eventId: string, params?: { priority?: string; category?: string; search?: string }) => {
    const qs = new URLSearchParams({ group_by_status: 'true', ...(params as Record<string, string>) });
    return request<APIKanbanBoard>(`/events/${eventId}/tasks?${qs}`);
  },

  create: (eventId: string, payload: CreateTaskPayload) =>
    request<APITask>(`/events/${eventId}/tasks`, { method: 'POST', body: JSON.stringify(payload) }),

  update: (taskId: string, payload: UpdateTaskPayload) =>
    request<APITask>(`/tasks/${taskId}`, { method: 'PATCH', body: JSON.stringify(payload) }),

  updateStatus: (taskId: string, status: string) =>
    request<APITask>(`/tasks/${taskId}/status`, { method: 'PATCH', body: JSON.stringify({ status }) }),

  delete: (taskId: string) =>
    request<void>(`/tasks/${taskId}`, { method: 'DELETE' }),

  createSubtask: (taskId: string, title: string) =>
    request<APISubtask>(`/tasks/${taskId}/subtasks`, { method: 'POST', body: JSON.stringify({ title }) }),
};

// ---- Budget ----------------------------------------------------------------

export const budgetApi = {
  list: (eventId: string, params?: { skip?: number; limit?: number; category?: string }) =>
    request<APIBudgetList>(`/events/${eventId}/budget?${new URLSearchParams(params as Record<string, string>)}`),

  summary: (eventId: string) =>
    request<APIBudgetSummary>(`/events/${eventId}/budget/summary`),

  create: (eventId: string, payload: CreateBudgetItemPayload) =>
    request<APIBudgetItem>(`/events/${eventId}/budget`, { method: 'POST', body: JSON.stringify(payload) }),

  update: (itemId: string, payload: UpdateBudgetItemPayload) =>
    request<APIBudgetItem>(`/budget/${itemId}`, { method: 'PATCH', body: JSON.stringify(payload) }),

  delete: (itemId: string) =>
    request<void>(`/budget/${itemId}`, { method: 'DELETE' }),
};

// ---- Vendors ---------------------------------------------------------------

export const vendorsApi = {
  search: (params: {
    category?: string; location?: string; event_type?: string;
    min_price?: number; max_price?: number; min_rating?: number;
    verified_only?: boolean; event_budget?: number; skip?: number; limit?: number;
  }) => {
    const qs = Object.entries(params)
      .filter(([, v]) => v !== undefined && v !== null && v !== '')
      .reduce((acc, [k, v]) => { acc[k] = String(v); return acc; }, {} as Record<string, string>);
    return request<APIVendorSearch>(`/vendors/search?${new URLSearchParams(qs)}`, {}, false);
  },

  get: (id: string) =>
    request<APIVendorFull>(`/vendors/${id}`, {}, false),

  saveToEvent: (eventId: string, vendorId: string, notes?: string) =>
    request<APISavedVendor>(`/events/${eventId}/vendors/save`, {
      method: 'POST',
      body: JSON.stringify({ vendor_id: vendorId, notes }),
    }),

  getSaved: (eventId: string) =>
    request<APISavedVendorList>(`/events/${eventId}/vendors/saved`),

  unsave: (eventId: string, vendorId: string) =>
    request<void>(`/events/${eventId}/vendors/${vendorId}/unsave`, { method: 'DELETE' }),
};

// ---- AI --------------------------------------------------------------------

export const aiApi = {
  generatePlan: (eventId: string, instructions?: string) =>
    request<AIResponse<APIEventPlanResult>>(`/ai/events/${eventId}/generate-plan`, {
      method: 'POST',
      body: JSON.stringify({ additional_instructions: instructions }),
    }),

  generateTasks: (eventId: string, instructions?: string) =>
    request<AIResponse<APITaskGeneratorResult>>(`/ai/events/${eventId}/generate-tasks`, {
      method: 'POST',
      body: JSON.stringify({ additional_instructions: instructions }),
    }),

  budgetAdvice: (eventId: string) =>
    request<AIResponse<APIBudgetAdviceResult>>(`/ai/events/${eventId}/budget-advice`, { method: 'POST' }),

  recommendVendors: (eventId: string, vendorIds?: string[]) =>
    request<AIResponse<APIVendorRecommendationResult>>(`/ai/events/${eventId}/recommend-vendors`, {
      method: 'POST',
      body: JSON.stringify({ vendor_ids: vendorIds }),
    }),

  chat: (message: string, eventId?: string, history?: { role: string; content: string }[]) =>
    request<AIResponse<APIChatResult>>('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ message, event_id: eventId, history: history ?? [] }),
    }),
};

export { APIError };
