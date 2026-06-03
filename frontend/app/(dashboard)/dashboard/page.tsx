'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  Calendar, DollarSign, CheckCircle2, Plus,
  ArrowRight, Sparkles, Users, TrendingUp,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { StatCard } from '@/components/ui/stat-card';
import { EmptyState } from '@/components/ui/empty-state';
import { ErrorState } from '@/components/ui/error-state';
import { useEvents } from '@/hooks/use-events';
import { formatCurrency, daysUntil } from '@/lib/utils';

const STAGGER = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.08 } } };
const ITEM = { hidden: { opacity: 0, y: 12 }, visible: { opacity: 1, y: 0, transition: { duration: 0.35 } } };

const STATUS_COLORS: Record<string, string> = {
  PLANNING: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
  ACTIVE: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300',
  COMPLETED: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
  CANCELLED: 'bg-red-100 text-red-600 dark:bg-red-900/40 dark:text-red-300',
};

export default function DashboardPage() {
  const { data: eventsData, isLoading, isError, refetch } = useEvents({ limit: 50 } as never);

  const events = eventsData?.items ?? [];
  const totalEvents = eventsData?.total ?? 0;
  const upcomingEvents = events
    .filter(e => daysUntil(e.start_date) >= 0)
    .sort((a, b) => daysUntil(a.start_date) - daysUntil(b.start_date))
    .slice(0, 4);
  const totalBudget = events.reduce((s, e) => s + (e.budget ?? 0), 0);
  const activeEvents = events.filter(e => e.status === 'ACTIVE' || e.status === 'PLANNING').length;

  return (
    <div className="space-y-7">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
      >
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground mt-1 text-sm">
            Your event planning command centre
          </p>
        </div>
        <Link href="/events/create">
          <Button className="gap-2 w-full sm:w-auto" size="sm">
            <Plus className="h-4 w-4" aria-hidden="true" />
            New Event
          </Button>
        </Link>
      </motion.div>

      {/* KPI strip */}
      <motion.div
        variants={STAGGER}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-2 lg:grid-cols-4 gap-4"
      >
        <motion.div variants={ITEM}>
          <StatCard
            icon={<Calendar className="h-4 w-4" />}
            label="Total Events"
            value={isLoading ? '—' : totalEvents}
            sub={isLoading ? undefined : `${activeEvents} active`}
            colorClass="bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400"
            loading={isLoading}
          />
        </motion.div>
        <motion.div variants={ITEM}>
          <StatCard
            icon={<TrendingUp className="h-4 w-4" />}
            label="Active Plans"
            value={isLoading ? '—' : activeEvents}
            sub="in planning"
            colorClass="bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400"
            loading={isLoading}
          />
        </motion.div>
        <motion.div variants={ITEM}>
          <StatCard
            icon={<DollarSign className="h-4 w-4" />}
            label="Total Budget"
            value={isLoading ? '—' : formatCurrency(totalBudget, 'INR')}
            sub="across all events"
            colorClass="bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400"
            loading={isLoading}
          />
        </motion.div>
        <motion.div variants={ITEM}>
          <StatCard
            icon={<Users className="h-4 w-4" />}
            label="Events Completed"
            value={isLoading ? '—' : events.filter(e => e.status === 'COMPLETED').length}
            sub="all time"
            colorClass="bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400"
            loading={isLoading}
          />
        </motion.div>
      </motion.div>

      {/* Main grid */}
      {isError ? (
        <ErrorState
          title="Couldn't load your events"
          message="Check your connection or try again."
          onRetry={() => refetch()}
        />
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Upcoming events */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
            className="lg:col-span-2"
          >
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-3">
                <div>
                  <CardTitle className="text-base">Upcoming Events</CardTitle>
                  <CardDescription>Events happening soon</CardDescription>
                </div>
                <Link href="/events">
                  <Button variant="ghost" size="sm" className="gap-1 text-xs h-7">
                    View all <ArrowRight className="h-3 w-3" />
                  </Button>
                </Link>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="space-y-3">
                    {Array.from({ length: 3 }).map((_, i) => (
                      <Skeleton key={i} className="h-16 rounded-lg" />
                    ))}
                  </div>
                ) : upcomingEvents.length === 0 ? (
                  <EmptyState
                    icon="📅"
                    title="No upcoming events"
                    description="Create your first event to get started."
                    size="sm"
                    action={{ label: 'Create Event', href: '/events/create' }}
                  />
                ) : (
                  <div className="space-y-2.5">
                    {upcomingEvents.map((event) => {
                      const days = daysUntil(event.start_date);
                      return (
                        <Link key={event.id} href={`/events/${event.id}`}>
                          <motion.div
                            whileHover={{ x: 3 }}
                            className="flex items-center gap-4 p-3.5 rounded-xl border border-border hover:border-indigo-300 dark:hover:border-indigo-700 hover:bg-muted/40 transition-all cursor-pointer group"
                          >
                            <div className="flex-1 min-w-0">
                              <p className="font-medium text-sm truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400">
                                {event.title}
                              </p>
                              <div className="flex items-center gap-2 mt-1">
                                <Calendar className="h-3 w-3 text-muted-foreground shrink-0" />
                                <span className="text-xs text-muted-foreground">
                                  {new Date(event.start_date).toLocaleDateString('en-IN', {
                                    day: 'numeric', month: 'short', year: 'numeric',
                                  })}
                                </span>
                                {event.location && (
                                  <>
                                    <span className="text-muted-foreground">·</span>
                                    <span className="text-xs text-muted-foreground truncate">{event.location}</span>
                                  </>
                                )}
                              </div>
                            </div>
                            <div className="flex items-center gap-2.5 shrink-0">
                              <Badge className={`text-xs ${STATUS_COLORS[event.status]}`}>
                                {event.status}
                              </Badge>
                              {days >= 0 && (
                                <div className="text-right hidden sm:block">
                                  <p className="text-sm font-bold text-indigo-600 dark:text-indigo-400">{days}d</p>
                                  <p className="text-[10px] text-muted-foreground">left</p>
                                </div>
                              )}
                            </div>
                          </motion.div>
                        </Link>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Quick actions */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
          >
            <Card className="h-full">
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Quick Actions</CardTitle>
                <CardDescription>Jump to common tasks</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2.5">
                {[
                  { icon: '📋', label: 'Create New Event', href: '/events/create', color: 'hover:bg-indigo-50 dark:hover:bg-indigo-900/20' },
                  { icon: '🏪', label: 'Browse Vendors', href: '/vendors', color: 'hover:bg-purple-50 dark:hover:bg-purple-900/20' },
                  { icon: '📊', label: 'View All Events', href: '/events', color: 'hover:bg-green-50 dark:hover:bg-green-900/20' },
                  { icon: '✨', label: 'AI Assistant', href: '#', color: 'hover:bg-amber-50 dark:hover:bg-amber-900/20' },
                ].map((item) => (
                  <Link key={item.href} href={item.href}>
                    <motion.div
                      whileHover={{ x: 3 }}
                      className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-colors ${item.color}`}
                    >
                      <span className="text-xl" aria-hidden="true">{item.icon}</span>
                      <span className="text-sm font-medium">{item.label}</span>
                      <ArrowRight className="h-3.5 w-3.5 text-muted-foreground ml-auto" />
                    </motion.div>
                  </Link>
                ))}

                <div className="mt-4 pt-4 border-t border-border">
                  <div className="flex items-center gap-2 p-3 rounded-xl bg-indigo-50 dark:bg-indigo-900/20">
                    <div className="p-1.5 rounded-lg bg-indigo-600">
                      <Sparkles className="h-3.5 w-3.5 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-semibold text-indigo-700 dark:text-indigo-300">AI-powered planning</p>
                      <p className="text-[11px] text-indigo-600/70 dark:text-indigo-400/70">Open any event to use AI</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      )}
    </div>
  );
}
