'use client';

import Link from 'next/link';
import { Calendar, ChevronRight, DollarSign, FolderKanban, Plus, Users } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useEvents } from '@/hooks/use-events';
import { daysUntil, formatCurrency } from '@/lib/utils';

const STATUS_STYLES: Record<string, string> = {
  PLANNING: 'border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-900 dark:bg-blue-950/40 dark:text-blue-300',
  ACTIVE: 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300',
  COMPLETED: 'border-slate-200 bg-slate-50 text-slate-600 dark:border-neutral-800 dark:bg-neutral-900 dark:text-slate-300',
  CANCELLED: 'border-red-200 bg-red-50 text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300',
};

function Metric({ label, value, icon: Icon }: { label: string; value: string | number; icon: typeof Calendar }) {
  return (
    <Card className="rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
      <CardContent className="flex items-center justify-between p-4">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</p>
          <p className="mt-1 text-2xl font-semibold">{value}</p>
        </div>
        <div className="flex h-10 w-10 items-center justify-center rounded-md bg-slate-100 text-slate-700 dark:bg-neutral-900 dark:text-slate-200">
          <Icon className="h-5 w-5" />
        </div>
      </CardContent>
    </Card>
  );
}

export default function DashboardPage() {
  const { data, isLoading, isError, error, refetch } = useEvents({ limit: 50 });
  const events = data?.items ?? [];
  const activeEvents = events.filter((event) => ['ACTIVE', 'PLANNING'].includes(event.status));
  const upcoming = activeEvents
    .filter((event) => daysUntil(event.start_date) >= 0)
    .sort((a, b) => daysUntil(a.start_date) - daysUntil(b.start_date))
    .slice(0, 6);
  const totalBudget = events.reduce((sum, event) => sum + Number(event.budget ?? 0), 0);
  const guestCount = events.reduce((sum, event) => sum + Number(event.estimated_guests ?? 0), 0);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
          <p className="mt-1 text-sm text-slate-500">Live planning summary from your FestSync API.</p>
        </div>
        <Link href="/events/create">
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            New event
          </Button>
        </Link>
      </div>

      {isError ? (
        <Card className="rounded-lg border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/30">
          <CardContent className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="font-medium text-red-700 dark:text-red-300">Could not load dashboard data</p>
              <p className="mt-1 text-sm text-red-600/80 dark:text-red-300/80">{(error as Error).message}</p>
            </div>
            <Button variant="outline" onClick={() => refetch()}>Retry</Button>
          </CardContent>
        </Card>
      ) : null}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {isLoading ? (
          Array.from({ length: 4 }).map((_, index) => <Skeleton key={index} className="h-28 rounded-lg" />)
        ) : (
          <>
            <Metric label="Total events" value={data?.total ?? 0} icon={Calendar} />
            <Metric label="Active plans" value={activeEvents.length} icon={FolderKanban} />
            <Metric label="Planned budget" value={formatCurrency(totalBudget, 'INR', 'en-IN')} icon={DollarSign} />
            <Metric label="Expected guests" value={guestCount} icon={Users} />
          </>
        )}
      </div>

      <div className="grid gap-5 lg:grid-cols-[1fr_360px]">
        <Card className="rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <CardHeader className="flex flex-row items-center justify-between gap-3 pb-3">
            <CardTitle className="text-base">Upcoming Events</CardTitle>
            <Link href="/events">
              <Button variant="ghost" size="sm" className="gap-1">
                View all
                <ChevronRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-3">
                {Array.from({ length: 5 }).map((_, index) => <Skeleton key={index} className="h-16 rounded-md" />)}
              </div>
            ) : upcoming.length === 0 ? (
              <div className="rounded-lg border border-dashed border-slate-300 p-8 text-center dark:border-neutral-800">
                <p className="text-sm font-medium">No upcoming events</p>
                <p className="mt-1 text-sm text-slate-500">Create an event or seed demo data to populate this view.</p>
              </div>
            ) : (
              <div className="divide-y divide-slate-100 dark:divide-neutral-900">
                {upcoming.map((event) => (
                  <Link
                    key={event.id}
                    href={`/events/${event.id}`}
                    className="flex items-center justify-between gap-4 py-3 transition-colors hover:bg-slate-50 dark:hover:bg-neutral-900/60"
                  >
                    <div className="min-w-0 px-1">
                      <p className="truncate text-sm font-medium">{event.title}</p>
                      <p className="mt-1 truncate text-xs text-slate-500">
                        {new Date(event.start_date).toLocaleDateString()} {event.location ? `· ${event.location}` : ''}
                      </p>
                    </div>
                    <div className="flex shrink-0 items-center gap-3">
                      <Badge variant="outline" className={STATUS_STYLES[event.status]}>{event.status}</Badge>
                      <span className="w-16 text-right text-sm font-semibold">{daysUntil(event.start_date)}d</span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <CardHeader>
            <CardTitle className="text-base">Operations</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Link href="/events/create">
              <Button variant="outline" className="w-full justify-between">
                Create event
                <ChevronRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/events">
              <Button variant="outline" className="w-full justify-between">
                Manage events
                <ChevronRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/vendors">
              <Button variant="outline" className="w-full justify-between">
                Browse vendors
                <ChevronRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
