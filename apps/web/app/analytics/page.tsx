'use client';

import { Activity, Bell, ClipboardList, Radio, ShieldAlert } from 'lucide-react';
import { DataTable, EmptyState, PageHeader, SeverityIndicator, StatusBadge } from '@/components/ui';
import { useAnalytics, useIncidents } from '@/hooks/use-data';

export default function AnalyticsPage() {
  const summary = useAnalytics(); const incidents = useIncidents();
  const data = summary.data;
  const metrics = [
    ['Observations', data?.observations ?? 0, <Radio key="observations" size={18}/>],
    ['Citizen reports', data?.reports ?? 0, <ClipboardList key="reports" size={18}/>],
    ['Incidents', data?.incidents ?? 0, <ShieldAlert key="incidents" size={18}/>],
    ['Alerts', data?.alerts ?? 0, <Bell key="alerts" size={18}/>],
  ] as const;
  const rows = (incidents.data ?? []).map((item) => [item.title, <SeverityIndicator key={`${item.id}-severity`} severity={item.severity}/>, <StatusBadge key={`${item.id}-status`} status={item.status}/>, new Date(item.created_at).toLocaleString()]);
  return <div className="page-wrap"><PageHeader eyebrow="Operational intelligence" title="Analytics" description="Live platform volumes and incident distribution from the shared environmental data plane." actions={<span className="secondary-button"><Activity size={15}/>{summary.isFetching ? 'Updating…' : 'Live metrics'}</span>}/>
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{metrics.map(([label, value, icon]) => <section key={label} className="surface-panel p-5"><div className="flex items-center justify-between text-emerald-400"><p className="text-xs text-slate-500">{label}</p>{icon}</div><p className="mt-3 font-mono text-3xl font-bold text-white">{value}</p></section>)}</div>
    <section className="mt-6"><h2 className="mb-3 font-semibold text-white">Incident performance</h2>{rows.length ? <DataTable columns={['Incident', 'Severity', 'Status', 'Created']} rows={rows}/> : <div className="surface-panel"><EmptyState icon={<Activity className="mx-auto text-emerald-400"/>} message={incidents.isLoading ? 'Loading incident analytics…' : 'No incidents are available for analysis.'}/></div>}</section>
  </div>;
}
