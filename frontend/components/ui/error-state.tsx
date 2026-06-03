'use client';

import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  inline?: boolean;
  className?: string;
}

export function ErrorState({
  title = 'Something went wrong',
  message,
  onRetry,
  inline = false,
  className,
}: ErrorStateProps) {
  const content = (
    <div className={cn('flex flex-col items-center gap-3 text-center p-8', className)}>
      <div className="p-3 rounded-full bg-red-50 dark:bg-red-900/20">
        <AlertTriangle className="h-6 w-6 text-red-500" aria-hidden="true" />
      </div>
      <div>
        <p className="font-semibold text-foreground">{title}</p>
        {message && (
          <p className="text-sm text-muted-foreground mt-1 max-w-xs">{message}</p>
        )}
      </div>
      {onRetry && (
        <Button
          variant="outline"
          size="sm"
          onClick={onRetry}
          className="gap-2 mt-1"
          aria-label="Retry request"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Try again
        </Button>
      )}
    </div>
  );

  if (inline) return content;

  return (
    <Card className="border-red-200 dark:border-red-800/50">{content}</Card>
  );
}
