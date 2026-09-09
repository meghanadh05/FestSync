'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { vendorsApi } from '@/lib/api';
import { toast } from 'sonner';

export const vendorKeys = {
  search: (params: object) => ['vendors', 'search', params] as const,
  detail: (id: string) => ['vendors', 'detail', id] as const,
  saved: (eventId: string) => ['vendors', 'saved', eventId] as const,
};

export function useVendorSearch(params: {
  category?: string; location?: string; event_type?: string;
  min_price?: number; max_price?: number; min_rating?: number;
  verified_only?: boolean; event_budget?: number;
  skip?: number; limit?: number;
}) {
  return useQuery({
    queryKey: vendorKeys.search(params),
    queryFn: () => vendorsApi.search(params),
    staleTime: 1000 * 60 * 2,   // vendor list refreshes less often
  });
}

export function useVendor(id: string) {
  return useQuery({
    queryKey: vendorKeys.detail(id),
    queryFn: () => vendorsApi.get(id),
    enabled: !!id,
  });
}

export function useSavedVendors(eventId: string) {
  return useQuery({
    queryKey: vendorKeys.saved(eventId),
    queryFn: () => vendorsApi.getSaved(eventId),
    enabled: !!eventId,
  });
}

export function useSaveVendor(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ vendorId, notes }: { vendorId: string; notes?: string }) =>
      vendorsApi.saveToEvent(eventId, vendorId, notes),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: vendorKeys.saved(eventId) });
      toast.success('Vendor saved!');
    },
    onError: (err: Error) => {
      if (err.message.includes('already saved')) {
        toast.info('Vendor already saved to this event');
      } else {
        toast.error(err.message);
      }
    },
  });
}

export function useUnsaveVendor(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vendorId: string) => vendorsApi.unsave(eventId, vendorId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: vendorKeys.saved(eventId) });
      toast.success('Vendor removed');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}
