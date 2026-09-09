'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Calendar, ChevronRight, MapPin, Plus, Search, Users } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { useEvents } from '@/hooks/use-events';
import { daysUntil, formatCurrency } from '@/lib/utils';
import type { APIEvent } from '@/lib/api-types';

const STATUS_STYLES: Record<string, string> = {
  PLANNING: 'border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-900 dark:bg-blue-950/40 dark:text-blue-300',
  ACTIVE: 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300',
  COMPLETED: 'border-slate-200 bg-slate-50 text-slate-600 dark:border-neutral-800 dark:bg-neutral-900 dark:text-slate-300',
  CANCELLED: 'border-red-200 bg-red-50 text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300',
};

function EventRow({ event }: { event: APIEvent }) {
  const days = daysUntil(event.start_date);

  return (
    <Link
      href={`/events/${event.id}`}
      className="grid gap-3 border-b border-slate-100 px-4 py-4 transition-colors last:border-0 hover:bg-slate-50 dark:border-neutral-900 dark:hover:bg-neutral-900/60 md:grid-cols-[1fr_150px_140px_120px_32px] md:items-center"
    >
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <p className="truncate text-sm font-medium">{event.title}</p>
          <Badge variant="outline" className={STATUS_STYLES[event.status]}>{event.status}</Badge>
        </div>
        <div className="mt-1 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500">
          <span className="flex items-center gap-1">
            <Calendar className="h-3.5 w-3.5" />
            {new Date(event.start_date).toLocaleDateString()}
          </span>
          {event.location ? (
            <span className="flex items-center gap-1">
              <MapPin className="h-3.5 w-3.5" />
              {event.location}
            </span>
          ) : null}
        </div>
      </div>
      <div className="text-sm text-slate-600 dark:text-slate-300">{event.event_type.replace(/_/g, ' ')}</div>
      <div className="flex items-center gap-1 text-sm text-slate-600 dark:text-slate-300">
        <Users className="h-3.5 w-3.5 text-slate-400" />
        {event.estimated_guests ?? 0}
      </div>
      <div className="text-sm font-medium">
        {event.budget ? formatCurrency(event.budget, event.currency, event.currency === 'INR' ? 'en-IN' : 'en-US') : '-'}
        <p className="text-xs font-normal text-slate-500">{days >= 0 ? `${days} days left` : 'Past event'}</p>
      </div>
      <ChevronRight className="hidden h-4 w-4 text-slate-400 md:block" />
    </Link>
  );
}

export default function EventsPage() {
  const [search, setSearch] = useState('');
  const { data, isLoading, isError, error, refetch } = useEvents({ search: search || undefined, limit: 50 });

  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Events</h1>
          <p className="mt-1 text-sm text-slate-500">{data ? `${data.total} events in workspace` : 'Manage plans, budgets, tasks, and vendors.'}</p>
        </div>
        <Link href="/events/create">
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Create event
          </Button>
        </Link>
      </div>

      <Card className="rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
        <CardContent className="p-4">
          <div className="relative max-w-lg">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <Input
              placeholder="Search by title or description"
              className="pl-9"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {isError ? (
        <Card className="rounded-lg border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/30">
          <CardContent className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="font-medium text-red-700 dark:text-red-300">Events could not be loaded</p>
              <p className="mt-1 text-sm text-red-600/80 dark:text-red-300/80">{(error as Error).message}</p>
            </div>
            <Button variant="outline" onClick={() => refetch()}>Retry</Button>
          </CardContent>
        </Card>
      ) : null}

      <Card className="overflow-hidden rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
        {isLoading ? (
          <div className="space-y-3 p-4">
            {Array.from({ length: 6 }).map((_, index) => <Skeleton key={index} className="h-16 rounded-md" />)}
          </div>
        ) : data?.items.length === 0 ? (
          <div className="p-10 text-center">
            <p className="text-sm font-medium">No events found</p>
            <p className="mt-1 text-sm text-slate-500">Create a new event to start planning.</p>
            <Link href="/events/create">
              <Button className="mt-4 gap-2">
                <Plus className="h-4 w-4" />
                Create event
              </Button>
            </Link>
          </div>
        ) : (
          <div>
            <div className="hidden grid-cols-[1fr_150px_140px_120px_32px] border-b border-slate-100 bg-slate-50 px-4 py-2 text-xs font-medium uppercase tracking-wide text-slate-500 dark:border-neutral-900 dark:bg-neutral-900/70 md:grid">
              <span>Event</span>
              <span>Type</span>
              <span>Guests</span>
              <span>Budget</span>
              <span />
            </div>
            {data?.items.map((event) => <EventRow key={event.id} event={event} />)}
          </div>
        )}
      </Card>
    </div>
  );
}
