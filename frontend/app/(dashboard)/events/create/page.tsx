'use client';

import { useRouter } from 'next/navigation';
import { CreateEventWizard } from '@/components/events/create-event-wizard';

export default function CreateEventPage() {
  const router = useRouter();

  const handleComplete = () => {
    // In a real app, this would create the event via API
    // For now, redirect to events list
    router.push('/events');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900 py-12 px-4">
      <CreateEventWizard onComplete={handleComplete} />
    </div>
  );
}
