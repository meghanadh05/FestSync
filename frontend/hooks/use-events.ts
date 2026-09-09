'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { eventsApi } from '@/lib/api';
import type { CreateEventPayload, UpdateEventPayload } from '@/lib/api-types';
import { toast } from 'sonner';

export const eventKeys = {
  all: ['events'] as const,
  list: (params?: object) => [...eventKeys.all, 'list', params] as const,
  detail: (id: string) => [...eventKeys.all, 'detail', id] as const,
  dashboard: (id: string) => [...eventKeys.all, 'dashboard', id] as const,
};

export function useEvents(params?: { search?: string; status?: string; skip?: number; limit?: number }) {
  return useQuery({
    queryKey: eventKeys.list(params),
    queryFn: () => eventsApi.list({ limit: 50, ...params }),
  });
}

export function useEvent(id: string) {
  return useQuery({
    queryKey: eventKeys.detail(id),
    queryFn: () => eventsApi.get(id),
    enabled: !!id,
  });
}

export function useEventDashboard(id: string) {
  return useQuery({
    queryKey: eventKeys.dashboard(id),
    queryFn: () => eventsApi.dashboard(id),
    enabled: !!id,
  });
}

export function useCreateEvent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateEventPayload) => eventsApi.create(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: eventKeys.all });
      toast.success('Event created!');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}

export function useUpdateEvent(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: UpdateEventPayload) => eventsApi.update(id, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: eventKeys.detail(id) });
      qc.invalidateQueries({ queryKey: eventKeys.dashboard(id) });
      toast.success('Event updated!');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}

export function useDeleteEvent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => eventsApi.delete(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: eventKeys.all });
      toast.success('Event deleted');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}
