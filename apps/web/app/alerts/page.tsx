'use client';
import { useAlerts } from '@/hooks/use-data';
import { EmptyState, SeverityIndicator } from '@/components/ui';
type Alert = { id: string; title: string; message: string; severity: string };
export default function AlertsPage() { const query = useAlerts(); const alerts = (query.data ?? []) as Alert[]; return <div className="p-4 md:p-8"><h1 className="text-2xl font-bold">Alert history</h1><div className="mt-6 space-y-3">{alerts.length ? alerts.map((alert) => <article key={alert.id} className="rounded-lg border border-climax-border bg-climax-surface p-4"><SeverityIndicator severity={alert.severity}/><h2 className="mt-2 font-semibold">{alert.title}</h2><p className="text-sm text-slate-400">{alert.message}</p></article>) : <EmptyState icon="🔔" message="No active alerts for your area."/>}</div></div>; }
