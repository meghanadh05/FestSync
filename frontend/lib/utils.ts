import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(
  amount: number,
  currency: string = 'USD',
  locale: string = 'en-US'
): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatDate(date: string | Date, format: 'short' | 'long' = 'short'): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  if (format === 'short') {
    return dateObj.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  }

  return dateObj.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });
}

export function getEventIcon(eventType: string): string {
  const icons: Record<string, string> = {
    wedding: '💒',
    birthday: '🎂',
    corporate: '💼',
    college_fest: '🎓',
    conference: '🎤',
    custom: '🎉',
  };
  return icons[eventType] || '🎉';
}

export function getVendorTypeIcon(vendorType: string): string {
  const icons: Record<string, string> = {
    catering: '🍽️',
    venue: '🏢',
    photography: '📷',
    decoration: '🎨',
    music: '🎵',
    event_planner: '📋',
    transportation: '🚗',
    accommodation: '🏨',
    invitations: '💌',
    cake: '🎂',
    florist: '🌸',
    entertainment: '🎭',
  };
  return icons[vendorType] || '✨';
}

export function getPriorityColor(priority: string): string {
  const colors: Record<string, string> = {
    low: 'text-blue-500',
    medium: 'text-amber-500',
    high: 'text-orange-500',
    urgent: 'text-red-500',
  };
  return colors[priority] || 'text-gray-500';
}

export function getPriorityBgColor(priority: string): string {
  const colors: Record<string, string> = {
    low: 'bg-blue-500/10 text-blue-600 dark:text-blue-400',
    medium: 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
    high: 'bg-orange-500/10 text-orange-600 dark:text-orange-400',
    urgent: 'bg-red-500/10 text-red-600 dark:text-red-400',
  };
  return colors[priority] || 'bg-gray-500/10 text-gray-600 dark:text-gray-400';
}

export function getStatusBgColor(status: string): string {
  const colors: Record<string, string> = {
    planning: 'bg-blue-500/10 text-blue-600 dark:text-blue-400',
    pending: 'bg-gray-500/10 text-gray-600 dark:text-gray-400',
    in_progress: 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
    ongoing: 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
    completed: 'bg-green-500/10 text-green-600 dark:text-green-400',
    confirmed: 'bg-green-500/10 text-green-600 dark:text-green-400',
    cancelled: 'bg-red-500/10 text-red-600 dark:text-red-400',
  };
  return colors[status] || 'bg-gray-500/10 text-gray-600 dark:text-gray-400';
}

export function formatStatusLabel(status: string): string {
  return status
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export function daysUntil(date: string | Date): number {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  dateObj.setHours(0, 0, 0, 0);
  const diff = dateObj.getTime() - today.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

export function isOverdue(date: string | Date): boolean {
  return daysUntil(date) < 0;
}

export function isToday(date: string | Date): boolean {
  return daysUntil(date) === 0;
}

export function isSoon(date: string | Date): boolean {
  const days = daysUntil(date);
  return days > 0 && days <= 7;
}

export function calculateBudgetUsage(spent: number, budget: number): number {
  if (budget === 0) return 0;
  return Math.round((spent / budget) * 100);
}
