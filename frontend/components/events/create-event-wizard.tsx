'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useEventStore } from '@/store/event-store';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  ArrowRight,
  ArrowLeft,
  Sparkles,
  Calendar,
  MapPin,
  DollarSign,
  Users,
  Palette,
  CheckCircle2,
} from 'lucide-react';

const eventTypes = [
  { id: 'wedding', label: 'Wedding', icon: '💒', description: 'A romantic celebration' },
  { id: 'birthday', label: 'Birthday', icon: '🎂', description: 'Age celebration party' },
  { id: 'corporate', label: 'Corporate', icon: '💼', description: 'Business event' },
  { id: 'college_fest', label: 'College Fest', icon: '🎓', description: 'Student festival' },
  { id: 'conference', label: 'Conference', icon: '🎤', description: 'Professional conference' },
  { id: 'custom', label: 'Custom', icon: '🎉', description: 'Something else' },
];

const themes = [
  { id: 'elegant', label: 'Elegant', color: 'from-purple-600 to-pink-600' },
  { id: 'modern', label: 'Modern', color: 'from-blue-600 to-cyan-600' },
  { id: 'rustic', label: 'Rustic', color: 'from-amber-600 to-orange-600' },
  { id: 'minimalist', label: 'Minimalist', color: 'from-slate-600 to-gray-600' },
  { id: 'vibrant', label: 'Vibrant', color: 'from-green-600 to-emerald-600' },
  { id: 'luxury', label: 'Luxury', color: 'from-yellow-600 to-yellow-400' },
];

interface CreateEventWizardProps {
  onComplete?: () => void;
}

export function CreateEventWizard({ onComplete }: CreateEventWizardProps) {
  const wizardState = useEventStore((state) => state.wizardState);
  const updateWizardState = useEventStore((state) => state.updateWizardState);
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const steps = [
    { number: 1, title: 'Event Type', icon: Sparkles },
    { number: 2, title: 'Details', icon: Calendar },
    { number: 3, title: 'Date & Location', icon: MapPin },
    { number: 4, title: 'Budget & Guests', icon: DollarSign },
    { number: 5, title: 'Theme', icon: Palette },
    { number: 6, title: 'Review', icon: CheckCircle2 },
  ];

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return !!wizardState.eventType;
      case 2:
        return !!wizardState.title && !!wizardState.description;
      case 3:
        return !!wizardState.startDate && !!wizardState.location;
      case 4:
        return wizardState.budget > 0 && wizardState.estimatedGuests > 0;
      default:
        return true;
    }
  };

  const handleNext = () => {
    if (canProceed() && currentStep < 6) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      onComplete?.();
    }, 1500);
  };

  const progress = (currentStep / 6) * 100;

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Create Your Event</h2>
          <span className="text-sm text-slate-600 dark:text-slate-400">
            Step {currentStep} of 6
          </span>
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      {/* Step Indicators */}
      <div className="flex justify-between mb-8 overflow-x-auto pb-2">
        {steps.map((step, idx) => {
          const StepIcon = step.icon;
          const isActive = step.number === currentStep;
          const isCompleted = step.number < currentStep;

          return (
            <div
              key={step.number}
              className="flex flex-col items-center min-w-max md:min-w-0"
            >
              <motion.div
                className={`h-12 w-12 rounded-full flex items-center justify-center mb-2 transition-all ${
                  isActive
                    ? 'bg-indigo-600 text-white ring-2 ring-indigo-600 ring-offset-2 dark:ring-offset-slate-950'
                    : isCompleted
                    ? 'bg-green-600 text-white'
                    : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'
                }`}
                layout
              >
                {isCompleted ? (
                  <CheckCircle2 className="h-6 w-6" />
                ) : (
                  <StepIcon className="h-5 w-5" />
                )}
              </motion.div>
              <p className="text-xs font-medium text-center hidden sm:block">
                {step.title}
              </p>
            </div>
          );
        })}
      </div>

      {/* Content Area */}
      <Card className="p-8 min-h-96">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {/* Step 1: Event Type */}
            {currentStep === 1 && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">What type of event are you planning?</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  This helps us provide personalized suggestions
                </p>
                <div className="grid grid-cols-2 gap-3 mt-6">
                  {eventTypes.map((type) => (
                    <motion.button
                      key={type.id}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() =>
                        updateWizardState({
                          eventType: type.id,
                        })
                      }
                      className={`p-4 rounded-lg border-2 transition-all text-left ${
                        wizardState.eventType === type.id
                          ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-950'
                          : 'border-slate-200 dark:border-slate-700 hover:border-indigo-300 dark:hover:border-indigo-700'
                      }`}
                    >
                      <span className="text-3xl block mb-2">{type.icon}</span>
                      <p className="font-semibold text-sm">{type.label}</p>
                      <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                        {type.description}
                      </p>
                    </motion.button>
                  ))}
                </div>
              </div>
            )}

            {/* Step 2: Details */}
            {currentStep === 2 && (
              <div className="space-y-5">
                <h3 className="text-lg font-semibold">Tell us about your event</h3>

                <div>
                  <Label htmlFor="title" className="mb-2 block">
                    Event Title *
                  </Label>
                  <Input
                    id="title"
                    placeholder="e.g., Sarah & John's Wedding"
                    value={wizardState.title}
                    onChange={(e) =>
                      updateWizardState({ title: e.target.value })
                    }
                  />
                </div>

                <div>
                  <Label htmlFor="description" className="mb-2 block">
                    Description
                  </Label>
                  <Textarea
                    id="description"
                    placeholder="Tell us more about your event, your vision, any special requirements..."
                    rows={4}
                    value={wizardState.description}
                    onChange={(e) =>
                      updateWizardState({ description: e.target.value })
                    }
                  />
                </div>
              </div>
            )}

            {/* Step 3: Date & Location */}
            {currentStep === 3 && (
              <div className="space-y-5">
                <h3 className="text-lg font-semibold">When & where?</h3>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="startDate" className="mb-2 block">
                      Start Date *
                    </Label>
                    <Input
                      id="startDate"
                      type="date"
                      value={wizardState.startDate}
                      onChange={(e) =>
                        updateWizardState({ startDate: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <Label htmlFor="endDate" className="mb-2 block">
                      End Date
                    </Label>
                    <Input
                      id="endDate"
                      type="date"
                      value={wizardState.endDate}
                      onChange={(e) =>
                        updateWizardState({ endDate: e.target.value })
                      }
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="location" className="mb-2 block">
                    Location *
                  </Label>
                  <Input
                    id="location"
                    placeholder="City, Country or Venue name"
                    value={wizardState.location}
                    onChange={(e) =>
                      updateWizardState({ location: e.target.value })
                    }
                  />
                </div>
              </div>
            )}

            {/* Step 4: Budget & Guests */}
            {currentStep === 4 && (
              <div className="space-y-5">
                <h3 className="text-lg font-semibold">Budget & Guest Count</h3>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="budget" className="mb-2 block">
                      Total Budget (USD) *
                    </Label>
                    <div className="relative">
                      <span className="absolute left-3 top-3 text-slate-500">$</span>
                      <Input
                        id="budget"
                        type="number"
                        placeholder="50000"
                        className="pl-7"
                        value={wizardState.budget || ''}
                        onChange={(e) =>
                          updateWizardState({
                            budget: parseFloat(e.target.value) || 0,
                          })
                        }
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="guests" className="mb-2 block">
                      Estimated Guests *
                    </Label>
                    <Input
                      id="guests"
                      type="number"
                      placeholder="150"
                      value={wizardState.estimatedGuests || ''}
                      onChange={(e) =>
                        updateWizardState({
                          estimatedGuests: parseInt(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                </div>

                {wizardState.budget > 0 && wizardState.estimatedGuests > 0 && (
                  <div className="p-4 rounded-lg bg-slate-100 dark:bg-slate-800">
                    <p className="text-sm text-slate-700 dark:text-slate-300">
                      💡 Estimated budget per guest:{' '}
                      <span className="font-semibold">
                        ${(wizardState.budget / wizardState.estimatedGuests).toFixed(0)}
                      </span>
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Step 5: Theme */}
            {currentStep === 5 && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Choose a theme</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  This will guide our AI recommendations
                </p>
                <div className="grid grid-cols-2 gap-3 mt-6">
                  {themes.map((theme) => (
                    <motion.button
                      key={theme.id}
                      whileHover={{ scale: 1.02 }}
                      onClick={() => updateWizardState({ title: theme.id })}
                      className={`p-4 rounded-lg border-2 overflow-hidden transition-all ${
                        wizardState.title === theme.id
                          ? 'border-indigo-600'
                          : 'border-slate-200 dark:border-slate-700'
                      }`}
                    >
                      <div
                        className={`h-16 rounded-lg mb-2 bg-gradient-to-br ${theme.color}`}
                      />
                      <p className="font-semibold text-sm">{theme.label}</p>
                    </motion.button>
                  ))}
                </div>
              </div>
            )}

            {/* Step 6: Review */}
            {currentStep === 6 && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold">Ready to create your event?</h3>

                <div className="space-y-4">
                  <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                      Event Title
                    </p>
                    <p className="font-semibold">{wizardState.title}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                      <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                        Type
                      </p>
                      <p className="font-semibold capitalize">
                        {wizardState.eventType}
                      </p>
                    </div>
                    <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                      <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                        Date
                      </p>
                      <p className="font-semibold">{wizardState.startDate}</p>
                    </div>
                    <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                      <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                        Budget
                      </p>
                      <p className="font-semibold">
                        ${wizardState.budget.toLocaleString()}
                      </p>
                    </div>
                    <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                      <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                        Guests
                      </p>
                      <p className="font-semibold">
                        {wizardState.estimatedGuests} people
                      </p>
                    </div>
                  </div>

                  <div className="p-4 rounded-lg bg-indigo-50 dark:bg-indigo-950 border border-indigo-200 dark:border-indigo-800">
                    <p className="text-sm text-indigo-900 dark:text-indigo-100">
                      ✨ We'll generate a comprehensive event plan, create initial tasks, and recommend vendors once you create your event!
                    </p>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </Card>

      {/* Navigation Buttons */}
      <div className="flex gap-4 mt-8">
        <Button
          variant="outline"
          onClick={handlePrev}
          disabled={currentStep === 1}
          className="gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Previous
        </Button>

        <div className="flex-1" />

        {currentStep < 6 ? (
          <Button
            onClick={handleNext}
            disabled={!canProceed()}
            className="gap-2"
          >
            Next
            <ArrowRight className="h-4 w-4" />
          </Button>
        ) : (
          <Button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
          >
            {isSubmitting ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{
                    duration: 1,
                    repeat: Infinity,
                  }}
                  className="h-4 w-4 border-2 border-white border-t-transparent rounded-full"
                />
                Creating...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                Create Event
              </>
            )}
          </Button>
        )}
      </div>
    </div>
  );
}
