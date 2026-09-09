'use client';

import { use, useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Calendar, MapPin, Users, DollarSign, CheckCircle2, ShoppingBag, Clock, Sparkles } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useEventDashboard } from '@/hooks/use-events';
import { formatCurrency } from '@/lib/utils';
import { AIAssistantDrawer } from '@/components/ai/ai-assistant-drawer';

function StatCard({ icon, label, value, sub, colorClass }: {
  icon: React.ReactNode; label: string; value: string | number; sub?: string; colorClass?: string;
}) {
  return (
    <Card className="p-5">
      <div className="flex items-center gap-3 mb-3">
        <div className={`p-2 rounded-lg ${colorClass ?? 'bg-indigo-50 dark:bg-indigo-900/30'}`}>{icon}</div>
        <p className="text-sm text-slate-500">{label}</p>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      {sub && <p className="text-xs text-slate-400 mt-0.5">{sub}</p>}
    </Card>
  );
}

export default function EventDashboardPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { data, isLoading, isError, error } = useEventDashboard(id);
  const [aiOpen, setAiOpen] = useState(false);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-32 rounded-xl" />)}
        </div>
        <Skeleton className="h-16 rounded-xl" />
      </div>
    );
  }

  if (isError || !data) {
    return (
      <Card className="p-12 text-center border-red-200 dark:border-red-800">
        <p className="text-red-600 font-semibold">Failed to load event</p>
        <p className="text-slate-500 text-sm mt-1">{(error as Error)?.message}</p>
      </Card>
    );
  }

  const { event } = data;
  const healthColor =
    data.budget_percentage_used > 100 ? 'text-red-500'
    : data.budget_percentage_used > 80 ? 'text-amber-500'
    : 'text-green-500';

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-3xl font-bold">{event.title}</h1>
          <div className="flex flex-wrap items-center gap-3 mt-2 text-sm text-slate-500">
            <span className="flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5" />
              {new Date(event.start_date).toLocaleDateString()}
            </span>
            {event.location && (
              <span className="flex items-center gap-1.5">
                <MapPin className="h-3.5 w-3.5" />{event.location}
              </span>
            )}
            {event.estimated_guests && (
              <span className="flex items-center gap-1.5">
                <Users className="h-3.5 w-3.5" />{event.estimated_guests} guests
              </span>
            )}
          </div>
        </div>
        <Button onClick={() => setAiOpen(true)} className="gap-2 bg-indigo-600 hover:bg-indigo-700">
          <Sparkles className="h-4 w-4" /> AI Assistant
        </Button>
      </motion.div>

      {/* KPI cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={<Clock className="h-4 w-4 text-indigo-600" />}
          label="Days remaining" value={data.days_remaining >= 0 ? data.days_remaining : 'Past'}
          colorClass="bg-indigo-50 dark:bg-indigo-900/30" />
        <StatCard icon={<CheckCircle2 className="h-4 w-4 text-green-600" />}
          label="Tasks done" value={`${data.tasks_completed} / ${data.tasks_total}`}
          sub={`${data.tasks_completion_percentage}% complete`}
          colorClass="bg-green-50 dark:bg-green-900/30" />
        <StatCard icon={<DollarSign className="h-4 w-4 text-amber-600" />}
          label="Budget spent" value={formatCurrency(data.budget_spent, event.currency)}
          sub={`of ${formatCurrency(data.budget_total, event.currency)}`}
          colorClass="bg-amber-50 dark:bg-amber-900/30" />
        <StatCard icon={<ShoppingBag className="h-4 w-4 text-purple-600" />}
          label="Vendors saved" value={data.vendors_saved}
          colorClass="bg-purple-50 dark:bg-purple-900/30" />
      </div>

      {/* Progress bar */}
      <Card className="p-5">
        <div className="flex items-center justify-between mb-2">
          <p className="font-medium">Overall progress</p>
          <span className={`font-bold text-sm ${healthColor}`}>
            {data.budget_percentage_used}% budget used
          </span>
        </div>
        <Progress value={data.progress_percentage} className="h-2.5" />
        <p className="text-sm text-slate-500 mt-2">{data.progress_percentage}% complete</p>
      </Card>

      {/* Navigation tabs */}
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="tasks" asChild>
            <Link href={`/events/${id}/tasks`}>Tasks</Link>
          </TabsTrigger>
          <TabsTrigger value="budget" asChild>
            <Link href={`/events/${id}/budget`}>Budget</Link>
          </TabsTrigger>
          <TabsTrigger value="vendors" asChild>
            <Link href={`/events/${id}/vendors`}>Vendors</Link>
          </TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="mt-4">
          {event.description && (
            <Card className="p-5">
              <p className="text-sm font-medium mb-2 text-slate-500">About this event</p>
              <p className="text-slate-700 dark:text-slate-300">{event.description}</p>
            </Card>
          )}
        </TabsContent>
      </Tabs>

      <AIAssistantDrawer open={aiOpen} onOpenChange={setAiOpen} eventId={id} />
    </div>
  );
}
