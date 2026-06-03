'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { budgetApi } from '@/lib/api';
import type { CreateBudgetItemPayload, UpdateBudgetItemPayload } from '@/lib/api-types';
import { toast } from 'sonner';

export const budgetKeys = {
  all: (eventId: string) => ['budget', eventId] as const,
  list: (eventId: string) => [...budgetKeys.all(eventId), 'list'] as const,
  summary: (eventId: string) => [...budgetKeys.all(eventId), 'summary'] as const,
};

export function useBudgetItems(eventId: string) {
  return useQuery({
    queryKey: budgetKeys.list(eventId),
    queryFn: () => budgetApi.list(eventId, { limit: 100 }),
    enabled: !!eventId,
  });
}

export function useBudgetSummary(eventId: string) {
  return useQuery({
    queryKey: budgetKeys.summary(eventId),
    queryFn: () => budgetApi.summary(eventId),
    enabled: !!eventId,
  });
}

export function useCreateBudgetItem(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateBudgetItemPayload) => budgetApi.create(eventId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: budgetKeys.all(eventId) });
      toast.success('Budget item added');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}

export function useUpdateBudgetItem(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ itemId, payload }: { itemId: string; payload: UpdateBudgetItemPayload }) =>
      budgetApi.update(itemId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: budgetKeys.all(eventId) });
      toast.success('Budget item updated');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}

export function useDeleteBudgetItem(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (itemId: string) => budgetApi.delete(itemId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: budgetKeys.all(eventId) });
      toast.success('Budget item removed');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}
