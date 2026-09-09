'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

import { workspacesApi } from '@/lib/api';
import type { CreateWorkspacePayload } from '@/lib/api-types';

export const workspaceKeys = {
  all: ['workspaces'] as const,
  detail: (id: string) => [...workspaceKeys.all, id] as const,
};

export function useWorkspaces() {
  return useQuery({
    queryKey: workspaceKeys.all,
    queryFn: () => workspacesApi.list(),
  });
}

export function useCreateWorkspace() {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateWorkspacePayload) => workspacesApi.create(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: workspaceKeys.all });
      toast.success('Workspace created');
    },
    onError: (error: Error) => toast.error(error.message),
  });
}
