'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowRight, Building2, CalendarDays, Loader2, UserRound } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { eventsApi } from '@/lib/api';
import type { EventTypeAPI } from '@/lib/api-types';
import { useCreateWorkspace } from '@/hooks/use-workspaces';

const EVENT_TYPES: EventTypeAPI[] = [
  'CONFERENCE',
  'CORPORATE_EVENT',
  'COLLEGE_FEST',
  'WEDDING',
  'BIRTHDAY',
  'CONCERT',
  'OTHER',
];

export default function OnboardingPage() {
  const router = useRouter();
  const createWorkspace = useCreateWorkspace();
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    name: '',
    profession: '',
    phone: '',
    workspaceName: '',
    organization: '',
    country: 'India',
    currency: 'INR',
    timezone: 'Asia/Kolkata',
    eventName: '',
    eventType: 'CONFERENCE' as EventTypeAPI,
    startDate: '',
    endDate: '',
    location: '',
    guests: '',
    budget: '',
    description: '',
    planningStyle: 'Structured',
    priority: 'Budget control',
  });

  const update = (key: keyof typeof form, value: string) => setForm((current) => ({ ...current, [key]: value }));

  const canContinue =
    step === 1 ? form.name.trim().length > 1
    : step === 2 ? form.workspaceName.trim().length > 1
    : step === 3 ? form.eventName.trim().length > 1 && form.startDate && form.endDate
    : true;

  const submit = async () => {
    await createWorkspace.mutateAsync({
      name: form.workspaceName,
      organization: form.organization || undefined,
      country: form.country,
      currency: form.currency,
      timezone: form.timezone,
    });

    if (form.eventName && form.startDate && form.endDate) {
      await eventsApi.create({
        title: form.eventName,
        event_type: form.eventType,
        start_date: form.startDate,
        end_date: form.endDate,
        location: form.location || undefined,
        estimated_guests: form.guests ? Number(form.guests) : undefined,
        budget: form.budget ? Number(form.budget) : undefined,
        currency: form.currency,
        description: form.description || undefined,
      });
    }

    router.push('/dashboard');
  };

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 text-slate-950 dark:bg-neutral-950 dark:text-slate-50">
      <div className="mx-auto max-w-3xl space-y-6">
        <div>
          <p className="text-sm font-medium text-slate-500">FestSync onboarding</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Set up your planning workspace</h1>
          <p className="mt-2 text-sm text-slate-500">Create the operational base for your first event. AI can help after the core details are in place.</p>
        </div>

        <div className="grid grid-cols-4 gap-2">
          {[1, 2, 3, 4].map((item) => (
            <div key={item} className={`h-1.5 rounded-full ${item <= step ? 'bg-slate-950 dark:bg-white' : 'bg-slate-200 dark:bg-neutral-800'}`} />
          ))}
        </div>

        <Card className="rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              {step === 1 ? <UserRound className="h-5 w-5" /> : step === 2 ? <Building2 className="h-5 w-5" /> : <CalendarDays className="h-5 w-5" />}
              {step === 1 ? 'Your Profile' : step === 2 ? 'Workspace' : step === 3 ? 'First Event' : 'Planning Preferences'}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            {step === 1 ? (
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Name</Label>
                  <Input value={form.name} onChange={(event) => update('name', event.target.value)} placeholder="Your name" />
                </div>
                <div className="space-y-2">
                  <Label>Role or profession</Label>
                  <Input value={form.profession} onChange={(event) => update('profession', event.target.value)} placeholder="Planner, founder, coordinator" />
                </div>
                <div className="space-y-2 sm:col-span-2">
                  <Label>Phone</Label>
                  <Input value={form.phone} onChange={(event) => update('phone', event.target.value)} placeholder="Optional" />
                </div>
              </div>
            ) : null}

            {step === 2 ? (
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Workspace name</Label>
                  <Input value={form.workspaceName} onChange={(event) => update('workspaceName', event.target.value)} placeholder="Meghanadh Events" />
                </div>
                <div className="space-y-2">
                  <Label>Organization</Label>
                  <Input value={form.organization} onChange={(event) => update('organization', event.target.value)} placeholder="Optional" />
                </div>
                <div className="space-y-2">
                  <Label>Country</Label>
                  <Input value={form.country} onChange={(event) => update('country', event.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Currency</Label>
                  <Input value={form.currency} onChange={(event) => update('currency', event.target.value.toUpperCase())} />
                </div>
                <div className="space-y-2 sm:col-span-2">
                  <Label>Timezone</Label>
                  <Input value={form.timezone} onChange={(event) => update('timezone', event.target.value)} />
                </div>
              </div>
            ) : null}

            {step === 3 ? (
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2 sm:col-span-2">
                  <Label>Event name</Label>
                  <Input value={form.eventName} onChange={(event) => update('eventName', event.target.value)} placeholder="Tech Summit 2027" />
                </div>
                <div className="space-y-2">
                  <Label>Event type</Label>
                  <select className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm" value={form.eventType} onChange={(event) => update('eventType', event.target.value)}>
                    {EVENT_TYPES.map((type) => <option key={type} value={type}>{type.replace(/_/g, ' ')}</option>)}
                  </select>
                </div>
                <div className="space-y-2">
                  <Label>Venue or city</Label>
                  <Input value={form.location} onChange={(event) => update('location', event.target.value)} placeholder="Mumbai" />
                </div>
                <div className="space-y-2">
                  <Label>Start date</Label>
                  <Input type="date" value={form.startDate} onChange={(event) => update('startDate', event.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>End date</Label>
                  <Input type="date" value={form.endDate} onChange={(event) => update('endDate', event.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Expected guests</Label>
                  <Input type="number" value={form.guests} onChange={(event) => update('guests', event.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Initial budget</Label>
                  <Input type="number" value={form.budget} onChange={(event) => update('budget', event.target.value)} />
                </div>
                <div className="space-y-2 sm:col-span-2">
                  <Label>Description</Label>
                  <Textarea value={form.description} onChange={(event) => update('description', event.target.value)} placeholder="Goals, audience, constraints, and notes" />
                </div>
              </div>
            ) : null}

            {step === 4 ? (
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Planning style</Label>
                  <Input value={form.planningStyle} onChange={(event) => update('planningStyle', event.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Top priority</Label>
                  <Input value={form.priority} onChange={(event) => update('priority', event.target.value)} />
                </div>
              </div>
            ) : null}

            <div className="flex justify-between border-t border-slate-100 pt-5 dark:border-neutral-900">
              <Button variant="outline" onClick={() => setStep((current) => Math.max(1, current - 1))} disabled={step === 1}>
                Back
              </Button>
              {step < 4 ? (
                <Button onClick={() => setStep((current) => current + 1)} disabled={!canContinue} className="gap-2">
                  Continue
                  <ArrowRight className="h-4 w-4" />
                </Button>
              ) : (
                <Button onClick={submit} disabled={createWorkspace.isPending} className="gap-2">
                  {createWorkspace.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                  Start planning
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
