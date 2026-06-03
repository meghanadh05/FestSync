'use client';

import { create } from 'zustand';
import type { Event } from '@/types/index';

interface EventWizardState {
  title: string;
  eventType: string;
  startDate: string;
  endDate: string;
  location: string;
  estimatedGuests: number;
  budget: number;
  description: string;
  currentStep: number;
}

interface EventState {
  selectedEventId: string | null;
  wizardState: EventWizardState;
  setSelectedEvent: (eventId: string) => void;
  clearSelectedEvent: () => void;
  updateWizardState: (state: Partial<EventWizardState>) => void;
  resetWizard: () => void;
  setWizardStep: (step: number) => void;
}

const initialWizardState: EventWizardState = {
  title: '',
  eventType: '',
  startDate: '',
  endDate: '',
  location: '',
  estimatedGuests: 0,
  budget: 0,
  description: '',
  currentStep: 1,
};

export const useEventStore = create<EventState>((set) => ({
  selectedEventId: null,
  wizardState: initialWizardState,
  setSelectedEvent: (eventId) => set({ selectedEventId: eventId }),
  clearSelectedEvent: () => set({ selectedEventId: null }),
  updateWizardState: (state) =>
    set((prevState) => ({
      wizardState: { ...prevState.wizardState, ...state },
    })),
  resetWizard: () => set({ wizardState: initialWizardState }),
  setWizardStep: (step) =>
    set((prevState) => ({
      wizardState: { ...prevState.wizardState, currentStep: step },
    })),
}));
