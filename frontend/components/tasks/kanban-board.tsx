'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Calendar, Filter, Plus, MoreVertical, X } from 'lucide-react';
import {
  getPriorityBgColor,
  formatDate,
} from '@/lib/utils';
import type { Task, TaskPriority, TaskStatus } from '@/types/index';

interface KanbanBoardProps {
  tasks: Task[];
  onTaskCreate?: (task: Partial<Task>) => void;
  onTaskUpdate?: (taskId: string, updates: Partial<Task>) => void;
  onTaskDelete?: (taskId: string) => void;
  categoryFilter?: string;
  priorityFilter?: string;
}

const taskStatuses = ['pending', 'in_progress', 'completed', 'cancelled'];
const categories = ['venue', 'catering', 'decoration', 'entertainment', 'photography', 'invitations'];
const priorities = ['low', 'medium', 'high', 'urgent'];

export function KanbanBoard({
  tasks,
  onTaskCreate,
  onTaskUpdate,
  onTaskDelete,
  categoryFilter,
  priorityFilter,
}: KanbanBoardProps) {
  const [draggedTask, setDraggedTask] = useState<Task | null>(null);
  const [showNewTaskDialog, setShowNewTaskDialog] = useState(false);
  const [selectedStatus, setSelectedStatus] = useState<string>('pending');
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'medium' });
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState<string | null>(categoryFilter || null);
  const [activePriority, setActivePriority] = useState<string | null>(priorityFilter || null);

  const filteredTasks = tasks.filter((task) => {
    let matches = true;
    if (searchTerm) {
      matches = task.title.toLowerCase().includes(searchTerm.toLowerCase());
    }
    if (activeCategory) {
      matches = matches && task.category === activeCategory;
    }
    if (activePriority) {
      matches = matches && task.priority === activePriority;
    }
    return matches;
  });

  const getTasksByStatus = (status: string) =>
    filteredTasks.filter((task) => task.status === status);

  const handleDragStart = (task: Task) => {
    setDraggedTask(task);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (status: string) => {
    if (draggedTask && draggedTask.status !== status) {
      onTaskUpdate?.(draggedTask.id, { status: status as TaskStatus });
      setDraggedTask(null);
    }
  };

  const handleCreateTask = () => {
    if (newTask.title.trim()) {
      onTaskCreate?.({
        title: newTask.title,
        description: newTask.description,
        priority: newTask.priority as TaskPriority,
        status: selectedStatus as TaskStatus,
      });
      setNewTask({ title: '', description: '', priority: 'medium' });
      setShowNewTaskDialog(false);
    }
  };

  const columns = [
    { status: 'pending', title: 'Pending', color: 'from-slate-500 to-slate-600', icon: '📋' },
    { status: 'in_progress', title: 'In Progress', color: 'from-amber-500 to-orange-600', icon: '🔄' },
    { status: 'completed', title: 'Completed', color: 'from-green-500 to-emerald-600', icon: '✅' },
  ];

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Input
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-4"
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 hover:bg-slate-100 dark:hover:bg-slate-800 rounded"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>

        <div className="flex gap-2 flex-wrap">
          {/* Category Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="gap-2">
                <Filter className="h-4 w-4" />
                Category {activeCategory && <X className="h-3 w-3" />}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => setActiveCategory(null)}>
                All Categories
              </DropdownMenuItem>
              {categories.map((cat) => (
                <DropdownMenuItem
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={activeCategory === cat ? 'bg-slate-100 dark:bg-slate-800' : ''}
                >
                  {cat}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Priority Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="gap-2">
                <Filter className="h-4 w-4" />
                Priority {activePriority && <X className="h-3 w-3" />}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => setActivePriority(null)}>
                All Priorities
              </DropdownMenuItem>
              {priorities.map((pri) => (
                <DropdownMenuItem
                  key={pri}
                  onClick={() => setActivePriority(pri)}
                  className={activePriority === pri ? 'bg-slate-100 dark:bg-slate-800' : ''}
                >
                  {pri}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Add Task Button */}
          <Button onClick={() => setShowNewTaskDialog(true)} className="gap-2">
            <Plus className="h-4 w-4" />
            Add Task
          </Button>
        </div>
      </div>

      {/* Kanban Columns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {columns.map((column) => {
          const columnTasks = getTasksByStatus(column.status);

          return (
            <motion.div key={column.status} layout className="flex flex-col">
              {/* Column Header */}
              <div className="flex items-center gap-3 mb-4">
                <div className={`h-3 w-3 rounded-full bg-gradient-to-r ${column.color}`} />
                <h3 className="font-semibold text-sm">
                  {column.title} ({columnTasks.length})
                </h3>
              </div>

              {/* Column Content */}
              <motion.div
                onDragOver={handleDragOver}
                onDrop={() => handleDrop(column.status)}
                className="flex-1 rounded-lg border-2 border-dashed border-slate-200 dark:border-slate-700 p-4 min-h-96 space-y-3 bg-slate-50/50 dark:bg-slate-900/50 transition-colors hover:border-slate-300 dark:hover:border-slate-600"
              >
                {columnTasks.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-center">
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      No tasks here yet
                    </p>
                  </div>
                ) : (
                  columnTasks.map((task) => (
                    <motion.div
                      key={task.id}
                      layout
                      draggable
                      onDragStart={() => handleDragStart(task)}
                      className="cursor-grab active:cursor-grabbing"
                    >
                      <Card className="p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between gap-2 mb-2">
                          <h4 className="font-medium text-sm flex-1 line-clamp-2">
                            {task.title}
                          </h4>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" size="icon" className="h-6 w-6 -mr-2">
                                <MoreVertical className="h-3 w-3" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem
                                onClick={() =>
                                  onTaskDelete?.(task.id)
                                }
                                className="text-red-600"
                              >
                                Delete
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </div>

                        {/* Priority Badge */}
                        <div className="flex gap-2 mb-3 flex-wrap">
                          <Badge className={getPriorityBgColor(task.priority)}>
                            {task.priority}
                          </Badge>
                          {task.category && (
                            <Badge variant="outline" className="text-xs">
                              {task.category}
                            </Badge>
                          )}
                        </div>

                        {/* Due Date */}
                        {task.due_date && (
                          <div className="flex items-center gap-1 text-xs text-slate-600 dark:text-slate-400">
                            <Calendar className="h-3 w-3" />
                            {formatDate(task.due_date, 'short')}
                          </div>
                        )}
                      </Card>
                    </motion.div>
                  ))
                )}
              </motion.div>
            </motion.div>
          );
        })}
      </div>

      {/* Add Task Dialog */}
      <Dialog open={showNewTaskDialog} onOpenChange={setShowNewTaskDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Task</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            <div>
              <Label htmlFor="title" className="mb-2 block">
                Task Title *
              </Label>
              <Input
                id="title"
                placeholder="e.g., Book photographer"
                value={newTask.title}
                onChange={(e) =>
                  setNewTask({ ...newTask, title: e.target.value })
                }
              />
            </div>

            <div>
              <Label htmlFor="description" className="mb-2 block">
                Description
              </Label>
              <Textarea
                id="description"
                placeholder="Add more details..."
                rows={3}
                value={newTask.description}
                onChange={(e) =>
                  setNewTask({ ...newTask, description: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="status" className="mb-2 block">
                  Status
                </Label>
                <select
                  id="status"
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value)}
                  className="w-full px-3 py-2 rounded-md border border-input bg-background text-sm"
                >
                  {taskStatuses.map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <Label htmlFor="priority" className="mb-2 block">
                  Priority
                </Label>
                <select
                  id="priority"
                  value={newTask.priority}
                  onChange={(e) =>
                    setNewTask({ ...newTask, priority: e.target.value })
                  }
                  className="w-full px-3 py-2 rounded-md border border-input bg-background text-sm"
                >
                  {priorities.map((pri) => (
                    <option key={pri} value={pri}>
                      {pri}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowNewTaskDialog(false)}
            >
              Cancel
            </Button>
            <Button onClick={handleCreateTask} disabled={!newTask.title.trim()}>
              Create Task
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
