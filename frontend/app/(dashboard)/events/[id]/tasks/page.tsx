'use client';

import { use, useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Sparkles, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { useKanbanTasks, useCreateTask, useUpdateTaskStatus } from '@/hooks/use-tasks';
import { useGenerateTasks } from '@/hooks/use-ai';
import type { APITask, TaskStatusAPI } from '@/lib/api-types';
import { toast } from 'sonner';
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const PRIORITY_COLORS: Record<string, string> = {
  URGENT: 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300',
  HIGH: 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300',
  MEDIUM: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300',
  LOW: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
};

type ColKey = 'pending' | 'in_progress' | 'completed';

const COLUMNS: { key: ColKey; label: string; color: string }[] = [
  { key: 'pending', label: 'Pending', color: 'border-slate-300 dark:border-slate-700' },
  { key: 'in_progress', label: 'In Progress', color: 'border-blue-400 dark:border-blue-600' },
  { key: 'completed', label: 'Completed', color: 'border-green-400 dark:border-green-600' },
];

function TaskCard({ task }: {
  task: APITask;
}) {
  const [dragging, setDragging] = useState(false);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: dragging ? 0.5 : 1, scale: 1 }}
      draggable
      onDragStart={(e) => {
        setDragging(true);
        (e as unknown as DragEvent).dataTransfer?.setData('taskId', task.id);
        (e as unknown as DragEvent).dataTransfer?.setData('taskStatus', task.status);
      }}
      onDragEnd={() => setDragging(false)}
      className="cursor-grab active:cursor-grabbing"
    >
      <Card className="p-3.5 space-y-2 hover:shadow-md transition-shadow">
        <p className="text-sm font-medium leading-snug">{task.title}</p>
        {task.description && (
          <p className="text-xs text-slate-400 line-clamp-2">{task.description}</p>
        )}
        <div className="flex items-center justify-between gap-2 flex-wrap">
          <Badge className={`text-xs ${PRIORITY_COLORS[task.priority]}`}>{task.priority}</Badge>
          {task.category && (
            <span className="text-xs text-slate-400 bg-slate-50 dark:bg-slate-800 px-2 py-0.5 rounded">
              {task.category}
            </span>
          )}
          {task.due_date && (
            <span className="text-xs text-slate-400 ml-auto">
              {new Date(task.due_date).toLocaleDateString()}
            </span>
          )}
        </div>
        {task.subtasks.length > 0 && (
          <p className="text-xs text-slate-400">
            {task.subtasks.filter(s => s.status === 'COMPLETED').length}/{task.subtasks.length} subtasks
          </p>
        )}
      </Card>
    </motion.div>
  );
}

function KanbanColumn({ col, tasks, onDrop }: {
  col: typeof COLUMNS[number];
  tasks: APITask[];
  onDrop: (colKey: string, taskId: string) => void;
}) {
  const [over, setOver] = useState(false);

  const statusMap: Record<string, TaskStatusAPI> = {
    pending: 'PENDING', in_progress: 'IN_PROGRESS', completed: 'COMPLETED',
  };

  return (
    <div
      className={`flex flex-col gap-3 min-h-[200px] p-3 rounded-xl border-2 transition-colors
        ${over ? 'bg-slate-50 dark:bg-slate-800/60' : 'bg-slate-50/50 dark:bg-slate-900/30'}
        ${col.color}`}
      onDragOver={(e) => { e.preventDefault(); setOver(true); }}
      onDragLeave={() => setOver(false)}
      onDrop={(e) => {
        e.preventDefault();
        setOver(false);
        const taskId = e.dataTransfer.getData('taskId');
        const fromStatus = e.dataTransfer.getData('taskStatus');
        if (taskId && fromStatus !== statusMap[col.key]) {
          onDrop(col.key, taskId);
        }
      }}
    >
      <div className="flex items-center justify-between px-1 pb-1">
        <h3 className="font-semibold text-sm">{col.label}</h3>
        <Badge variant="outline" className="text-xs">{tasks.length}</Badge>
      </div>
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
      {tasks.length === 0 && (
        <div className="flex-1 flex items-center justify-center py-8">
          <p className="text-xs text-slate-400">Drop tasks here</p>
        </div>
      )}
    </div>
  );
}

export default function TasksPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: eventId } = use(params);
  const { data: kanban, isLoading } = useKanbanTasks(eventId);
  const createTask = useCreateTask(eventId);
  const updateStatus = useUpdateTaskStatus(eventId);
  const generateTasks = useGenerateTasks(eventId);

  const [showNewTask, setShowNewTask] = useState(false);
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'MEDIUM' });

  const statusMap: Record<string, TaskStatusAPI> = {
    pending: 'PENDING', in_progress: 'IN_PROGRESS', completed: 'COMPLETED',
  };

  const handleDrop = (colKey: string, taskId: string) => {
    updateStatus.mutate({ taskId, status: statusMap[colKey] });
  };

  const handleGenerateTasks = async () => {
    const res = await generateTasks.mutateAsync(undefined);
    if (res?.result?.tasks) {
      for (const t of res.result.tasks) {
        await createTask.mutateAsync({
          title: t.title,
          description: t.description ?? undefined,
          priority: t.priority,
          category: t.category ?? undefined,
          due_date: t.due_date ?? undefined,
        });
      }
      toast.success(`${res.result.tasks.length} tasks generated!`);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h1 className="text-3xl font-bold">Tasks</h1>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2"
            disabled={generateTasks.isPending} onClick={handleGenerateTasks}>
            {generateTasks.isPending
              ? <><Loader2 className="h-4 w-4 animate-spin" /> Generating…</>
              : <><Sparkles className="h-4 w-4" /> AI Generate</>}
          </Button>
          <Button className="gap-2" onClick={() => setShowNewTask(true)}>
            <Plus className="h-4 w-4" /> Add Task
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="space-y-3">
              <Skeleton className="h-6 w-24" />
              {Array.from({ length: 3 }).map((_, j) => <Skeleton key={j} className="h-24 rounded-xl" />)}
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {COLUMNS.map((col) => (
            <KanbanColumn
              key={col.key}
              col={col}
              tasks={(kanban as unknown as Record<ColKey, APITask[]>)?.[col.key] ?? []}
              onDrop={handleDrop}
            />
          ))}
        </div>
      )}

      {/* New task dialog */}
      <Dialog open={showNewTask} onOpenChange={setShowNewTask}>
        <DialogContent>
          <DialogHeader><DialogTitle>Add Task</DialogTitle></DialogHeader>
          <div className="space-y-4 py-2">
            <div className="space-y-1.5">
              <Label>Title</Label>
              <Input placeholder="Task title" value={newTask.title}
                onChange={(e) => setNewTask(p => ({ ...p, title: e.target.value }))} />
            </div>
            <div className="space-y-1.5">
              <Label>Description</Label>
              <Textarea placeholder="Optional description" value={newTask.description}
                onChange={(e) => setNewTask(p => ({ ...p, description: e.target.value }))} />
            </div>
            <div className="space-y-1.5">
              <Label>Priority</Label>
              <Select value={newTask.priority} onValueChange={(v) => setNewTask(p => ({ ...p, priority: v }))}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {['LOW', 'MEDIUM', 'HIGH', 'URGENT'].map(p => (
                    <SelectItem key={p} value={p}>{p}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowNewTask(false)}>Cancel</Button>
            <Button
              disabled={!newTask.title.trim() || createTask.isPending}
              onClick={async () => {
                await createTask.mutateAsync({
                  title: newTask.title,
                  description: newTask.description || undefined,
                  priority: newTask.priority as import('@/lib/api-types').TaskPriorityAPI,
                });
                setNewTask({ title: '', description: '', priority: 'MEDIUM' });
                setShowNewTask(false);
              }}
            >
              {createTask.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Create'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
