'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { aiApi } from '@/lib/api';
import { taskKeys } from './use-tasks';
import { eventKeys } from './use-events';
import { toast } from 'sonner';

export function useGeneratePlan(eventId: string) {
  return useMutation({
    mutationFn: (instructions?: string) => aiApi.generatePlan(eventId, instructions),
    onError: (err: Error) => toast.error(`AI plan failed: ${err.message}`),
  });
}

export function useGenerateTasks(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (instructions?: string) => aiApi.generateTasks(eventId, instructions),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: taskKeys.all(eventId) });
      qc.invalidateQueries({ queryKey: eventKeys.dashboard(eventId) });
    },
    onError: (err: Error) => toast.error(`AI task generation failed: ${err.message}`),
  });
}

export function useBudgetAdvice(eventId: string) {
  return useMutation({
    mutationFn: () => aiApi.budgetAdvice(eventId),
    onError: (err: Error) => toast.error(`Budget advice failed: ${err.message}`),
  });
}

export function useRecommendVendors(eventId: string) {
  return useMutation({
    mutationFn: (vendorIds?: string[]) => aiApi.recommendVendors(eventId, vendorIds),
    onError: (err: Error) => toast.error(`Vendor recommendations failed: ${err.message}`),
  });
}

export function useAIChat() {
  return useMutation({
    mutationFn: ({
      message,
      eventId,
      history,
    }: {
      message: string;
      eventId?: string;
      history?: { role: string; content: string }[];
    }) => aiApi.chat(message, eventId, history),
    onError: (err: Error) => toast.error(`Chat failed: ${err.message}`),
  });
}
