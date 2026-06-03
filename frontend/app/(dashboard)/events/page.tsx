'use client';

import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { mockEvents } from '@/lib/mock-data';
import {
  formatCurrency,
  getEventIcon,
  getStatusBgColor,
  daysUntil,
} from '@/lib/utils';
import { Calendar, MapPin, Users, DollarSign, Search, Plus } from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useState } from 'react';

export default function EventsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const filteredEvents = mockEvents.filter((e) =>
    e.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-4xl font-bold">Events</h1>
          <p className="text-slate-600 dark:text-slate-400 mt-2">
            Manage all your events in one place
          </p>
        </div>
        <Link href="/events/create">
          <Button size="lg" className="gap-2">
            <Plus className="h-4 w-4" />
            Create Event
          </Button>
        </Link>
      </motion.div>

      {/* Search */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
      >
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
          <Input
            type="text"
            placeholder="Search events..."
            className="pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </motion.div>

      {/* Events Grid */}
      {filteredEvents.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-20"
        >
          <Calendar className="h-16 w-16 text-slate-300 dark:text-slate-700 mb-4" />
          <h3 className="text-lg font-semibold mb-2">No events found</h3>
          <p className="text-slate-600 dark:text-slate-400 mb-6">
            Create your first event to get started
          </p>
          <Link href="/events/create">
            <Button className="gap-2">
              <Plus className="h-4 w-4" />
              Create Event
            </Button>
          </Link>
        </motion.div>
      ) : (
        <motion.div
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ staggerChildren: 0.1 }}
        >
          {filteredEvents.map((event, i) => (
            <motion.div
              key={event.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Link href={`/events/${event.id}`}>
                <motion.div whileHover={{ y: -4 }} className="cursor-pointer">
                  <Card className="overflow-hidden h-full hover:border-indigo-500 dark:hover:border-indigo-500 transition-colors">
                    {event.thumbnail_url && (
                      <div className="h-40 bg-slate-200 dark:bg-slate-800 overflow-hidden">
                        <img
                          src={event.thumbnail_url}
                          alt={event.title}
                          className="w-full h-full object-cover hover:scale-105 transition-transform"
                        />
                      </div>
                    )}
                    <div className="p-6">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h3 className="font-semibold text-lg">{event.title}</h3>
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            {getEventIcon(event.event_type)} {event.event_type}
                          </p>
                        </div>
                      </div>

                      <Badge className={`${getStatusBgColor(event.status)} mb-4`}>
                        {event.status}
                      </Badge>

                      <div className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          {event.start_date}{' '}
                          <span className="text-xs">
                            ({daysUntil(event.start_date)} days)
                          </span>
                        </div>
                        {event.location && (
                          <div className="flex items-center gap-2">
                            <MapPin className="h-4 w-4" />
                            {event.location}
                          </div>
                        )}
                        {event.estimated_guests && (
                          <div className="flex items-center gap-2">
                            <Users className="h-4 w-4" />
                            {event.estimated_guests} guests
                          </div>
                        )}
                        {event.budget && (
                          <div className="flex items-center gap-2">
                            <DollarSign className="h-4 w-4" />
                            {formatCurrency(event.budget)}
                          </div>
                        )}
                      </div>
                    </div>
                  </Card>
                </motion.div>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
