'use client';

import { Card } from '@/components/ui/card';
import { KanbanBoard } from '@/components/tasks/kanban-board';
import { mockTasks } from '@/lib/mock-data';

interface TasksPageProps {
  params: { id: string };
}

export default function TasksPage({ params }: TasksPageProps) {
  const eventTasks = mockTasks.filter((t) => t.event_id === params.id);

  const handleTaskCreate = (task: any) => {
    console.log('Create task:', task);
    // Will be connected to API later
  };

  const handleTaskUpdate = (taskId: string, updates: any) => {
    console.log('Update task:', taskId, updates);
    // Will be connected to API later
  };

  const handleTaskDelete = (taskId: string) => {
    console.log('Delete task:', taskId);
    // Will be connected to API later
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">Task Board</h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Manage your event tasks with our smart Kanban board. Drag and drop to change status.
        </p>
      </div>

      <Card className="p-6">
        <KanbanBoard
          tasks={eventTasks}
          onTaskCreate={handleTaskCreate}
          onTaskUpdate={handleTaskUpdate}
          onTaskDelete={handleTaskDelete}
        />
      </Card>
    </div>
  );
}
