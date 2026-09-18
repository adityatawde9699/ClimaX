'use client';

import { QueryClient, QueryClientProvider, useQueryClient } from '@tanstack/react-query';
import { useEffect, useState, type ReactNode } from 'react';
import { useRealtimeEvents } from '@/hooks/useRealtimeEvents';

function RealtimeSync() {
  const events = useRealtimeEvents();
  const client = useQueryClient();
  useEffect(() => {
    const latest = events[0];
    if (!latest) return;
    const domain = latest.event.split('.')[0];
    const keys: Record<string, string[]> = { incident: ['incidents'], alert: ['alerts'], report: ['reports'], observation: ['observations'] };
    for (const key of keys[domain] ?? []) void client.invalidateQueries({ queryKey: [key] });
    void client.invalidateQueries({ queryKey: ['analytics-summary'] });
  }, [client, events]);
  return null;
}

export function Providers({ children }: { children: ReactNode }) {
  const [client] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        retry: (failureCount, error) => (
          failureCount < 1 && !error.message.includes('Database service is unavailable')
        ),
        refetchInterval: (query) => query.state.status === 'error' ? false : 30_000,
        refetchOnWindowFocus: false,
      },
    },
  }));
  return <QueryClientProvider client={client}><RealtimeSync/>{children}</QueryClientProvider>;
}
