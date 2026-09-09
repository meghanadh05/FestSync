'use client';

import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  sub?: string;
  trend?: { value: number; label: string };
  colorClass?: string;
  loading?: boolean;
  className?: string;
}

export function StatCard({
  icon,
  label,
  value,
  sub,
  trend,
  colorClass = 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400',
  loading = false,
  className,
}: StatCardProps) {
  if (loading) {
    return (
      <Card className={cn('p-5', className)}>
        <div className="flex items-center gap-3 mb-3">
          <Skeleton className="h-9 w-9 rounded-lg" />
          <Skeleton className="h-4 w-28" />
        </div>
        <Skeleton className="h-7 w-20 mb-1" />
        <Skeleton className="h-3 w-24" />
      </Card>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className={cn('p-5 hover:shadow-md transition-shadow', className)}>
        <div className="flex items-center gap-3 mb-3">
          <div
            className={cn('p-2 rounded-lg shrink-0', colorClass)}
            aria-hidden="true"
          >
            {icon}
          </div>
          <p className="text-sm text-muted-foreground truncate">{label}</p>
        </div>
        <p className="text-2xl font-bold tabular-nums">{value}</p>
        {sub && <p className="text-xs text-muted-foreground mt-0.5">{sub}</p>}
        {trend && (
          <p
            className={cn(
              'text-xs mt-1 font-medium',
              trend.value >= 0
                ? 'text-green-600 dark:text-green-400'
                : 'text-red-500 dark:text-red-400'
            )}
          >
            {trend.value >= 0 ? '↑' : '↓'} {Math.abs(trend.value)}% {trend.label}
          </p>
        )}
      </Card>
    </motion.div>
  );
}
