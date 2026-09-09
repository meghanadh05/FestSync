'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { tasksApi } from '@/lib/api';
import type { CreateTaskPayload, UpdateTaskPayload, TaskStatusAPI, APIKanbanBoard } from '@/lib/api-types';
import { toast } from 'sonner';
import { eventKeys } from './use-events';

export const taskKeys = {
  all: (eventId: string) => ['tasks', eventId] as const,
  kanban: (eventId: string, filters?: object) => [...taskKeys.all(eventId), 'kanban', filters] as const,
  list: (eventId: string, filters?: object) => [...taskKeys.all(eventId), 'list', filters] as const,
};

export function useKanbanTasks(
  eventId: string,
  filters?: { priority?: string; category?: string; search?: string }
) {
  return useQuery({
    queryKey: taskKeys.kanban(eventId, filters),
    queryFn: () => tasksApi.kanban(eventId, filters),
    enabled: !!eventId,
  });
}

export function useTasks(
  eventId: string,
  filters?: { status?: string; priority?: string; category?: string; search?: string }
) {
  return useQuery({
    queryKey: taskKeys.list(eventId, filters),
    queryFn: () => tasksApi.list(eventId, filters),
    enabled: !!eventId,
  });
}

export function useCreateTask(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateTaskPayload) => tasksApi.create(eventId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: taskKeys.all(eventId) });
      qc.invalidateQueries({ queryKey: eventKeys.dashboard(eventId) });
      toast.success('Task created!');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}

export function useUpdateTask(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ taskId, payload }: { taskId: string; payload: UpdateTaskPayload }) =>
      tasksApi.update(taskId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: taskKeys.all(eventId) });
    },
    onError: (err: Error) => toast.error(err.message),
  });
}

// Optimistic status update — updates kanban board instantly, rolls back on error
export function useUpdateTaskStatus(eventId: string) {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: ({ taskId, status }: { taskId: string; status: TaskStatusAPI }) =>
      tasksApi.updateStatus(taskId, status),

    onMutate: async ({ taskId, status }) => {
      // Cancel any outgoing refetches
      await qc.cancelQueries({ queryKey: taskKeys.all(eventId) });

      // Snapshot all kanban queries for this event
      const snapshots = qc.getQueriesData<APIKanbanBoard>({ queryKey: taskKeys.all(eventId) });

      // Optimistically update every kanban query
      qc.setQueriesData<APIKanbanBoard>(
        { queryKey: taskKeys.all(eventId) },
        (old) => {
          if (!old) return old;
          const cols = ['pending', 'in_progress', 'completed'] as const;
          const newBoard: APIKanbanBoard = { pending: [], in_progress: [], completed: [] };

          // Move the task to the new column
          for (const col of cols) {
            for (const task of old[col]) {
              if (task.id === taskId) {
                const dest = status.toLowerCase() as keyof APIKanbanBoard;
                newBoard[dest] = [...(newBoard[dest] ?? []), { ...task, status }];
              } else {
                newBoard[col] = [...newBoard[col], task];
              }
            }
          }
          return newBoard;
        }
      );

      return { snapshots };
    },

    onError: (_err, _vars, context) => {
      // Roll back on error
      if (context?.snapshots) {
        for (const [queryKey, data] of context.snapshots) {
          qc.setQueryData(queryKey, data);
        }
      }
      toast.error('Failed to update task status');
    },

    onSettled: () => {
      qc.invalidateQueries({ queryKey: taskKeys.all(eventId) });
      qc.invalidateQueries({ queryKey: eventKeys.dashboard(eventId) });
    },
  });
}

export function useDeleteTask(eventId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (taskId: string) => tasksApi.delete(taskId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: taskKeys.all(eventId) });
      qc.invalidateQueries({ queryKey: eventKeys.dashboard(eventId) });
      toast.success('Task deleted');
    },
    onError: (err: Error) => toast.error(err.message),
  });
}
