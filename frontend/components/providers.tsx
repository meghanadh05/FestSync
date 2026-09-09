'use client';

import React, { useEffect, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from 'sonner';
import { useUIStore } from '@/store/ui-store';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      gcTime: 1000 * 60 * 10,
      retry: (failureCount, error: unknown) => {
        // Don't retry on 401/403/404
        if (error instanceof Error && 'status' in error) {
          const status = (error as { status: number }).status;
          if ([401, 403, 404].includes(status)) return false;
        }
        return failureCount < 2;
      },
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  const theme = useUIStore((state) => state.theme);

  useEffect(() => {
    setMounted(true);
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {mounted && (
        <Toaster
          position="bottom-right"
          richColors
          closeButton
          theme={theme as 'light' | 'dark' | 'system'}
        />
      )}
      {mounted && process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}
