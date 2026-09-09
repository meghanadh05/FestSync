'use client';

import { useRouter } from 'next/navigation';
import { CreateEventWizard } from '@/components/events/create-event-wizard';

export default function CreateEventPage() {
  const router = useRouter();

  const handleComplete = () => {
    router.push('/events');
  };

  return (
    <div className="py-4">
      <CreateEventWizard onComplete={handleComplete} />
    </div>
  );
}
