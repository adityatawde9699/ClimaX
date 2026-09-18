'use client';

import { Bell, BellRing, CheckCircle2, MapPin, ShieldCheck } from 'lucide-react';
import { useAlerts } from '@/hooks/use-data';
import { EmptyState, PageHeader, SeverityIndicator } from '@/components/ui';

type Alert = { id: string; title: string; message: string; severity: string; is_dispatched: boolean };

export default function AlertsPage() {
  const query = useAlerts();
  const alerts = (query.data ?? []) as Alert[];
  return <div className="page-wrap">
    <PageHeader eyebrow="Public safety" title="Alert history" description="Monitor active air-quality warnings, health advisories, and municipal response notices." actions={<button className="secondary-button"><Bell size={15}/>Notification preferences</button>}/>
    <div className="mb-6 grid gap-3 sm:grid-cols-3"><section className="surface-panel p-4"><p className="text-xs text-slate-500">Active alerts</p><p className="mt-2 font-mono text-2xl font-bold text-red-400">{alerts.length}</p></section><section className="surface-panel p-4"><p className="text-xs text-slate-500">Dispatched alerts</p><p className="mt-2 font-mono text-2xl font-bold text-sky-400">{(query.data ?? []).filter((alert) => alert.is_dispatched).length}</p></section><section className="surface-panel p-4"><p className="text-xs text-slate-500">Alert service</p><p className={`mt-2 flex items-center gap-2 text-sm font-semibold ${query.isError ? 'text-red-400' : 'text-emerald-400'}`}><ShieldCheck size={18}/>{query.isError ? 'Unavailable' : 'Connected'}</p></section></div>
    <div className="space-y-3">{alerts.length ? alerts.map((alert) => <article key={alert.id} className="surface-panel p-5 transition hover:border-slate-700"><div className="flex flex-wrap items-start justify-between gap-3"><div><SeverityIndicator severity={alert.severity}/><h2 className="mt-3 font-semibold text-white">{alert.title}</h2><p className="mt-1 text-sm leading-6 text-slate-400">{alert.message}</p></div><span className="flex items-center gap-1.5 text-xs text-slate-500"><MapPin size={13}/>Regional</span></div></article>) : <div className="surface-panel"><EmptyState icon={<span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-emerald-500/10 text-emerald-400"><CheckCircle2/></span>} message={query.isLoading ? 'Checking the alert network…' : 'No active alerts for your area.'} cta={<button className="secondary-button"><BellRing size={15}/>Manage alert radius</button>}/></div>}</div>
  </div>;
}
