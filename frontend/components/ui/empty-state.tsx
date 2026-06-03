'use client';

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface EmptyStateProps {
  icon?: string;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick?: () => void;
    href?: string;
  };
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function EmptyState({
  icon = '✨',
  title,
  description,
  action,
  className,
  size = 'md',
}: EmptyStateProps) {
  const sizes = {
    sm: { wrapper: 'py-8', icon: 'text-3xl', title: 'text-base', desc: 'text-xs' },
    md: { wrapper: 'py-16', icon: 'text-5xl', title: 'text-lg', desc: 'text-sm' },
    lg: { wrapper: 'py-24', icon: 'text-6xl', title: 'text-xl', desc: 'text-base' },
  };

  const s = sizes[size];

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn(
        'flex flex-col items-center justify-center text-center',
        s.wrapper,
        className
      )}
    >
      <motion.div
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', stiffness: 200, damping: 15, delay: 0.1 }}
        className={cn('mb-4 select-none', s.icon)}
        aria-hidden="true"
      >
        {icon}
      </motion.div>
      <p className={cn('font-semibold text-foreground', s.title)}>{title}</p>
      {description && (
        <p className={cn('text-muted-foreground mt-1.5 max-w-xs leading-relaxed', s.desc)}>
          {description}
        </p>
      )}
      {action && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mt-5"
        >
          {action.href ? (
            <a href={action.href}>
              <Button size="sm">{action.label}</Button>
            </a>
          ) : (
            <Button size="sm" onClick={action.onClick}>
              {action.label}
            </Button>
          )}
        </motion.div>
      )}
    </motion.div>
  );
}
