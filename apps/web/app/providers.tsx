'use client';

import { QueryClient, QueryClientProvider, useQueryClient } from '@tanstack/react-query';
import { useEffect, useState, type ReactNode } from 'react';
import { useRealtimeEvents } from '@/hooks/useRealtimeEvents';

function RealtimeSync() {
  const events = useRealtimeEvents();
  const client = useQueryClient();
  const [dismissedToast, setDismissedToast] = useState<string | null>(null);
  const latest = events[0];
  const severity = String(latest?.data?.severity ?? '');
  const toastId = latest?.event === 'alert.dispatched' && ['HIGH', 'VERY_HIGH', 'CRITICAL'].includes(severity) ? String(latest.data?.id ?? '') : null;
  const toast = toastId && toastId !== dismissedToast ? { id: toastId, title: `${severity.replaceAll('_', ' ')} environmental alert`, detail: 'A new public safety alert was dispatched. Open Alerts for details.' } : null;
  useEffect(() => {
    if (!latest) return;
    const domain = latest.event.split('.')[0];
    const keys: Record<string, string[]> = { incident: ['incidents'], intervention: ['interventions'], alert: ['alerts'], report: ['reports'], observation: ['observations'] };
    for (const key of keys[domain] ?? []) void client.invalidateQueries({ queryKey: [key] });
    void client.invalidateQueries({ queryKey: ['analytics-summary'] });
  }, [client, latest]);
  useEffect(() => {
    if (!toastId || toastId === dismissedToast) return;
    const timer = setTimeout(() => setDismissedToast(toastId), 8_000);
    return () => clearTimeout(timer);
  }, [dismissedToast, toastId]);
  return toast ? <aside role="alert" aria-live="assertive" className="fixed right-3 top-20 z-[70] w-[min(360px,calc(100vw-1.5rem))] rounded-xl border border-red-500/40 bg-[#101923] p-4 shadow-2xl"><div className="flex items-start justify-between gap-3"><div><p className="text-sm font-semibold text-red-300">{toast.title}</p><p className="mt-1 text-xs leading-5 text-slate-300">{toast.detail}</p></div><button aria-label="Dismiss notification" onClick={() => setDismissedToast(toast.id)} className="text-slate-500 hover:text-white">×</button></div></aside> : null;
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
