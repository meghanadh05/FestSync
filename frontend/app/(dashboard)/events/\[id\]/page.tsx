'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { mockEvents, mockTasks, mockBudgetItems, mockSavedVendors } from '@/lib/mock-data';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import {
  Calendar,
  MapPin,
  Users,
  DollarSign,
  CheckCircle2,
  Clock,
  Zap,
  Share2,
  Edit,
  MoreVertical,
} from 'lucide-react';
import {
  formatCurrency,
  getEventIcon,
  daysUntil,
  calculateBudgetUsage,
  formatDate,
} from '@/lib/utils';
import Link from 'next/link';

interface EventDetailPageProps {
  params: { id: string };
}

export default function EventDetailPage({ params }: EventDetailPageProps) {
  const event = mockEvents.find((e) => e.id === params.id) || mockEvents[0];
  const eventTasks = mockTasks.filter((t) => t.event_id === event.id);
  const eventBudget = mockBudgetItems.filter((b) => b.event_id === event.id);
  const eventVendors = mockSavedVendors.filter((v) => v.event_id === event.id);

  const completedTasks = eventTasks.filter((t) => t.status === 'completed').length;
  const totalSpent = eventBudget.reduce((sum, item) => sum + item.amount, 0);
  const taskProgress = (completedTasks / eventTasks.length) * 100 || 0;
  const budgetProgress = calculateBudgetUsage(totalSpent, event.budget || 0);
  const daysLeft = daysUntil(event.start_date);

  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-start justify-between gap-4"
      >
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-4xl">{getEventIcon(event.event_type)}</span>
            <div>
              <h1 className="text-3xl font-bold">{event.title}</h1>
              <p className="text-slate-600 dark:text-slate-400 capitalize">
                {event.event_type} • {formatDate(event.start_date, 'long')}
              </p>
            </div>
          </div>
          <Badge className="bg-gradient-to-r from-indigo-600 to-purple-600">
            {event.status}
          </Badge>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="icon" className="gap-2">
            <Share2 className="h-4 w-4" />
          </Button>
          <Button variant="outline" className="gap-2">
            <Edit className="h-4 w-4" />
            Edit
          </Button>
        </div>
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ staggerChildren: 0.1 }}
      >
        <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Calendar className="h-4 w-4 text-indigo-600" />
                Days Remaining
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-indigo-600">{Math.max(0, daysLeft)}</div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                {daysLeft > 0 ? `Starting ${formatDate(event.start_date, 'short')}` : 'Event is happening!'}
              </p>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-green-600" />
                Tasks Completed
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">
                {completedTasks}/{eventTasks.length}
              </div>
              <Progress value={taskProgress} className="mt-3 h-2" />
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-2">
                {Math.round(taskProgress)}% complete
              </p>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <DollarSign className="h-4 w-4 text-amber-600" />
                Budget Used
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-amber-600">
                {budgetProgress}%
              </div>
              <Progress value={budgetProgress} className="mt-3 h-2" />
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-2">
                {formatCurrency(totalSpent)} / {formatCurrency(event.budget || 0)}
              </p>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Users className="h-4 w-4 text-purple-600" />
                Vendors Booked
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                {eventVendors.filter((v) => v.status === 'booked').length}
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                of {eventVendors.length} shortlisted
              </p>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>

      {/* Event Details & Tabs */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Event Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                  Location
                </p>
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-slate-500" />
                  <p className="font-medium">{event.location}</p>
                </div>
              </div>
              <div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                  Estimated Guests
                </p>
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-slate-500" />
                  <p className="font-medium">{event.estimated_guests} people</p>
                </div>
              </div>
              <div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                  Date Range
                </p>
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-slate-500" />
                  <p className="font-medium">
                    {formatDate(event.start_date, 'short')} - {formatDate(event.end_date, 'short')}
                  </p>
                </div>
              </div>
              <div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
                  Total Budget
                </p>
                <div className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4 text-slate-500" />
                  <p className="font-medium">{formatCurrency(event.budget || 0)}</p>
                </div>
              </div>
            </div>

            {event.description && (
              <div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-2">
                  Description
                </p>
                <p className="text-slate-700 dark:text-slate-300">{event.description}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Tabs */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Event Dashboard</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="tasks">Tasks</TabsTrigger>
                <TabsTrigger value="budget">Budget</TabsTrigger>
                <TabsTrigger value="vendors">Vendors</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="mt-6 space-y-4">
                <div className="p-4 rounded-lg bg-indigo-50 dark:bg-indigo-950 border border-indigo-200 dark:border-indigo-800">
                  <div className="flex items-start gap-3">
                    <Zap className="h-5 w-5 text-indigo-600 dark:text-indigo-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-sm text-indigo-900 dark:text-indigo-100">
                        AI Insights
                      </p>
                      <p className="text-sm text-indigo-800 dark:text-indigo-200 mt-1">
                        Based on your event progress, we recommend focusing on vendor confirmations next. You're 25% through your planning timeline and 34% through your budget.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700">
                    <h4 className="font-semibold text-sm mb-3">Quick Actions</h4>
                    <div className="space-y-2">
                      <Link href={`/events/${event.id}/tasks`}>
                        <Button variant="ghost" className="w-full justify-start text-sm h-9">
                          ✅ Manage Tasks
                        </Button>
                      </Link>
                      <Link href={`/events/${event.id}/budget`}>
                        <Button variant="ghost" className="w-full justify-start text-sm h-9">
                          💰 Track Budget
                        </Button>
                      </Link>
                      <Link href={`/events/${event.id}/vendors`}>
                        <Button variant="ghost" className="w-full justify-start text-sm h-9">
                          👥 Manage Vendors
                        </Button>
                      </Link>
                    </div>
                  </div>

                  <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700">
                    <h4 className="font-semibold text-sm mb-3">Event Summary</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-600 dark:text-slate-400">Total Tasks</span>
                        <span className="font-medium">{eventTasks.length}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600 dark:text-slate-400">Completed</span>
                        <span className="font-medium text-green-600">{completedTasks}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600 dark:text-slate-400">Vendors</span>
                        <span className="font-medium">{eventVendors.length}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="tasks" className="mt-6">
                <Link href={`/events/${event.id}/tasks`}>
                  <Button className="mb-4 w-full">View Full Task Board</Button>
                </Link>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Manage all your event tasks with our Kanban board
                </p>
              </TabsContent>

              <TabsContent value="budget" className="mt-6">
                <Link href={`/events/${event.id}/budget`}>
                  <Button className="mb-4 w-full">View Full Budget Tracker</Button>
                </Link>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Track expenses and optimize your spending
                </p>
              </TabsContent>

              <TabsContent value="vendors" className="mt-6">
                <Link href={`/events/${event.id}/vendors`}>
                  <Button className="mb-4 w-full">View Saved Vendors</Button>
                </Link>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Manage and compare your shortlisted vendors
                </p>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
