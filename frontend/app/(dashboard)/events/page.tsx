'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Calendar, MapPin, Users, DollarSign, Search, Plus } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { useEvents } from '@/hooks/use-events';
import { formatCurrency, daysUntil } from '@/lib/utils';
import type { APIEvent } from '@/lib/api-types';

const STATUS_COLORS: Record<string, string> = {
  PLANNING: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
  ACTIVE: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300',
  COMPLETED: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
  CANCELLED: 'bg-red-100 text-red-600 dark:bg-red-900/40 dark:text-red-300',
};

const EVENT_ICONS: Record<string, string> = {
  WEDDING: '💒', BIRTHDAY: '🎂', CORPORATE_EVENT: '💼', COLLEGE_FEST: '🎓',
  CONFERENCE: '🎤', RECEPTION: '🥂', ENGAGEMENT: '💍', CONCERT: '🎵', OTHER: '🎉',
};

function EventCardSkeleton() {
  return (
    <Card className="p-6 space-y-4">
      <Skeleton className="h-5 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
      <div className="grid grid-cols-2 gap-3">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-full" />
      </div>
    </Card>
  );
}

function EventCard({ event }: { event: APIEvent }) {
  const days = daysUntil(event.start_date);
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
      <Link href={`/events/${event.id}`}>
        <Card className="group cursor-pointer p-6 transition-all hover:shadow-lg hover:border-indigo-300 dark:hover:border-indigo-700">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xl">{EVENT_ICONS[event.event_type] ?? '🎉'}</span>
                <h3 className="font-semibold text-lg truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400">
                  {event.title}
                </h3>
              </div>
              <Badge className={`text-xs ${STATUS_COLORS[event.status]}`}>
                {event.status}
              </Badge>
            </div>
            {days !== null && days >= 0 && (
              <div className="text-right shrink-0">
                <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{days}</p>
                <p className="text-xs text-slate-500">days left</p>
              </div>
            )}
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm text-slate-600 dark:text-slate-400">
            <div className="flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5 shrink-0" />
              <span className="truncate">{new Date(event.start_date).toLocaleDateString()}</span>
            </div>
            {event.location && (
              <div className="flex items-center gap-1.5">
                <MapPin className="h-3.5 w-3.5 shrink-0" />
                <span className="truncate">{event.location}</span>
              </div>
            )}
            {event.estimated_guests && (
              <div className="flex items-center gap-1.5">
                <Users className="h-3.5 w-3.5 shrink-0" />
                <span>{event.estimated_guests} guests</span>
              </div>
            )}
            {event.budget && (
              <div className="flex items-center gap-1.5">
                <DollarSign className="h-3.5 w-3.5 shrink-0" />
                <span>{formatCurrency(event.budget, event.currency)}</span>
              </div>
            )}
          </div>
        </Card>
      </Link>
    </motion.div>
  );
}

export default function EventsPage() {
  const [search, setSearch] = useState('');
  const { data, isLoading, isError, error } = useEvents({ search: search || undefined });

  return (
    <div className="space-y-8">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold">Events</h1>
          <p className="mt-2 text-slate-600 dark:text-slate-400">
            {data ? `${data.total} event${data.total !== 1 ? 's' : ''}` : 'Manage all your events'}
          </p>
        </div>
        <Link href="/events/create">
          <Button size="lg" className="gap-2"><Plus className="h-4 w-4" />Create Event</Button>
        </Link>
      </motion.div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
        <Input placeholder="Search events…" className="pl-10" value={search}
          onChange={(e) => setSearch(e.target.value)} />
      </div>

      {isError && (
        <Card className="p-8 text-center border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 font-medium">Failed to load events</p>
          <p className="text-sm text-slate-500 mt-1">{(error as Error).message}</p>
        </Card>
      )}

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {isLoading
          ? Array.from({ length: 6 }).map((_, i) => <EventCardSkeleton key={i} />)
          : data?.items.length === 0
          ? (
            <div className="col-span-full py-20 text-center">
              <p className="text-5xl mb-4">🎉</p>
              <p className="text-xl font-semibold">No events yet</p>
              <p className="text-slate-500 mt-2">Create your first event to get started</p>
              <Link href="/events/create"><Button className="mt-6 gap-2"><Plus className="h-4 w-4" /> Create Event</Button></Link>
            </div>
          )
          : data?.items.map((event) => <EventCard key={event.id} event={event} />)
        }
      </div>
    </div>
  );
}
