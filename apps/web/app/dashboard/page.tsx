'use client';

import Link from 'next/link';
import {
  Activity,
  ArrowUpDown,
  ArrowUp,
  BellRing,
  Building2,
  CloudSun,
  Factory,
  Flame,
  HeartPulse,
  Radio,
  Send,
  ShieldAlert,
  Users,
  Wind,
} from 'lucide-react';
import { useState, type ReactNode } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { MapCanvas } from '@/features/map/MapCanvas';
import { EmptyState, SeverityIndicator, StatusBadge } from '@/components/ui';
import { useAlerts, useAnalytics, useHotspots, useIncidents, useObservations, usePredictions, useReports, useWeather } from '@/hooks/use-data';
import { apiClient } from '@/lib/api-client';
import type { Alert, CitizenReport, Incident, Observation } from '@/types/api';

type Tone = 'green' | 'orange' | 'red' | 'blue' | 'violet';

const toneStyles: Record<Tone, string> = {
  green: 'border-emerald-500/35 bg-emerald-500/[.07] text-emerald-400',
  orange: 'border-orange-500/30 bg-orange-500/[.07] text-orange-400',
  red: 'border-red-500/30 bg-red-500/[.07] text-red-400',
  blue: 'border-sky-500/30 bg-sky-500/[.07] text-sky-400',
  violet: 'border-violet-500/30 bg-violet-500/[.07] text-violet-400',
};

function StatCard({ label, value, note, tone, icon }: { label: string; value: string; note: string; tone: Tone; icon: ReactNode }) {
  return (
    <section className={`relative min-w-0 overflow-hidden rounded-xl border px-4 py-4 shadow-[inset_0_1px_rgba(255,255,255,.03)] ${toneStyles[tone]}`}>
      <div className="absolute -right-5 -top-7 h-24 w-24 rounded-full bg-current opacity-[.04] blur-xl" />
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[.08em] text-slate-300">{label}</p>
          <div className="mt-2 flex items-end gap-2">
            <strong className="font-mono text-3xl leading-none">{value}</strong>
            <span className="mb-0.5 flex items-center gap-1 text-[11px] text-slate-300">{note.includes('today') && <ArrowUp size={11} />}{note}</span>
          </div>
        </div>
        <span className="rounded-lg bg-current/10 p-2.5">{icon}</span>
      </div>
    </section>
  );
}

function ForecastTable() {
  const [horizon, setHorizon] = useState(24);
  const query = usePredictions(horizon);
  return (
    <section className="dashboard-panel min-w-0 p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <h2 className="panel-title">AQI Forecast</h2>
        <div className="flex rounded-lg bg-[#07131f] p-1 text-[10px] text-slate-400">
          {[6, 24, 72].map((item) => <button key={item} onClick={() => setHorizon(item)} className={`rounded-md px-2.5 py-1.5 transition ${horizon === item ? 'bg-emerald-500 text-white' : 'hover:text-white'}`}>{item}h</button>)}
        </div>
      </div>
      <div className="overflow-x-auto">
        {query.data?.length ? <table className="w-full min-w-[360px] text-center text-xs"><thead className="text-[10px] text-slate-500"><tr><th className="pb-2 text-left font-medium">Location</th><th className="font-medium">Horizon</th><th className="font-medium">AQI</th><th className="font-medium">PM2.5</th></tr></thead><tbody>{query.data.map((item) => <tr key={item.id} className="border-t border-slate-800/70"><td className="py-2.5 text-left font-medium text-slate-200">{item.latitude.toFixed(3)}, {item.longitude.toFixed(3)}</td><td>{item.horizon_hours}h</td><td className="font-mono text-orange-300">{Math.round(item.predicted_aqi)}</td><td className="font-mono text-slate-300">{item.predicted_pm25.toFixed(1)}</td></tr>)}</tbody></table> : <EmptyState icon={<CloudSun className="mx-auto text-cyan-400"/>} message={query.isLoading ? 'Loading forecasts…' : query.error?.message || 'No forecast data is available.'}/>}
      </div>
    </section>
  );
}

function TrendChart({ readings }: { readings: Observation[] }) {
  const values = readings.filter((item) => item.aqi != null).slice(-12);
  return (
    <section className="dashboard-panel min-w-0 p-4">
      <h2 className="panel-title">AQI Trend <span className="font-normal text-slate-500">(Delhi)</span></h2>
      {values.length ? <><div className="mt-3 flex h-[190px] items-end gap-2 border-b border-slate-800 px-2">{values.map((item) => <i key={item.id} title={`AQI ${item.aqi}`} className="min-h-1 flex-1 rounded-t bg-emerald-500/70" style={{ height: `${Math.max(2, Math.min(100, ((item.aqi ?? 0) / 500) * 100))}%` }}/>)}</div><div className="mt-2 flex justify-between text-[10px] text-slate-500"><span>{new Date(values[0].timestamp).toLocaleTimeString()}</span><span>{new Date(values[values.length - 1].timestamp).toLocaleTimeString()}</span></div></> : <div className="mt-3"><EmptyState icon={<Radio className="mx-auto text-emerald-400"/>} message="No AQI observations are available."/></div>}
    </section>
  );
}

function RecentReports({ items }: { items: CitizenReport[] }) {
  const visible = items.slice(0, 4);
  return (
    <section className="dashboard-panel p-4">
      <div className="flex items-center justify-between"><h2 className="panel-title">Recent Reports</h2><Link href="/reports" className="text-[11px] text-sky-400 hover:text-sky-300">View all</Link></div>
      <div className="mt-3 divide-y divide-slate-800/80">{visible.length ? visible.map((item) => <div key={item.id} className="flex items-center gap-3 py-2.5"><div className="grid h-10 w-12 shrink-0 place-items-center rounded-md bg-slate-800"><Factory size={17} className="text-slate-200"/></div><div className="min-w-0 flex-1"><p className="truncate text-xs font-medium text-slate-200">{item.category.replaceAll('_', ' ')}</p><p className="truncate text-[10px] text-slate-500">{item.address_text || `${item.location.latitude.toFixed(2)}, ${item.location.longitude.toFixed(2)}`} · {new Date(item.created_at).toLocaleString()}</p></div><span className="text-[10px] text-slate-400">{item.status}</span></div>) : <EmptyState icon={<Users className="mx-auto text-violet-400"/>} message="No citizen reports are available."/>}</div>
    </section>
  );
}

function CriticalAlert({ alert }: { alert?: Alert }) {
  if (!alert) return <section className="dashboard-panel p-4"><div className="flex items-center justify-between"><h2 className="panel-title">Latest Critical Alert</h2><Link href="/alerts" className="text-[11px] text-sky-400">View all</Link></div><div className="mt-3"><EmptyState icon={<ShieldAlert className="mx-auto text-emerald-400"/>} message="No active alerts."/></div></section>;
  return (
    <section className="dashboard-panel flex min-h-0 flex-col p-4">
      <div className="flex items-center justify-between"><h2 className="panel-title">Latest Critical Alert</h2><Link href="/alerts" className="text-[11px] text-sky-400">View all</Link></div>
      <div className="mt-3 flex flex-1 flex-col rounded-xl border border-red-500/30 bg-red-500/[.045] p-4">
        <div className="flex items-center justify-between border-b border-red-500/20 pb-3"><strong className="text-sm text-red-400">ALERT #{alert.id.slice(0, 6).toUpperCase()}</strong><span className="rounded border border-red-500/30 bg-red-500/10 px-2 py-1 text-[9px] font-bold text-red-300">{alert.severity}</span></div>
        <dl className="mt-3 grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-[11px]"><dt className="text-slate-500">Title</dt><dd className="text-right font-medium text-slate-200">{alert.title}</dd><dt className="text-slate-500">Channel</dt><dd className="text-right font-medium text-slate-200">{alert.channel.replaceAll('_', ' ')}</dd><dt className="text-slate-500">Detected</dt><dd className="text-right text-slate-300">{new Date(alert.created_at).toLocaleString()}</dd><dt className="text-slate-500">Status</dt><dd className="text-right font-bold text-white">{alert.is_dispatched ? 'Dispatched' : 'Pending'}</dd></dl>
        <Link href="/alerts" className="mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-red-600 px-3 py-2.5 text-xs font-semibold text-white transition hover:bg-red-500"><Send size={13}/>Open alert details</Link>
      </div>
    </section>
  );
}

function AqiOperationsStrip({ readings }: { readings: Observation[] }) {
  const live = readings.filter((item) => item.aqi != null).slice(0, 5);
  const average = live.length ? Math.round(live.reduce((sum, item) => sum + (item.aqi ?? 0), 0) / live.length) : null;
  const guidance = average == null ? 'Waiting for verified sensor observations.' : average <= 50 ? 'Outdoor activity is suitable for most people.' : average <= 100 ? 'Sensitive groups should monitor prolonged outdoor activity.' : average <= 200 ? 'Sensitive groups should reduce prolonged outdoor exertion.' : 'Limit outdoor exposure and follow active health advisories.';
  return <section className="mt-3 grid gap-3 lg:grid-cols-[1.45fr_.8fr]"><div className="dashboard-panel overflow-hidden p-4"><div className="mb-3 flex items-center justify-between"><h2 className="panel-title flex items-center gap-2"><Activity size={15} className="text-emerald-400"/>Real-time AQI ticker</h2><span className="text-[9px] uppercase tracking-wider text-slate-500">Verified observations</span></div>{live.length ? <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-5">{live.map((item) => <article key={item.id} className="rounded-lg border border-slate-800 bg-[#04111d] px-3 py-2"><p className="truncate text-[9px] text-slate-500">{item.sensor_id}</p><p className="mt-1 font-mono text-xl font-bold text-white">{Math.round(item.aqi ?? 0)}</p><p className="text-[9px] text-emerald-400">AQI · {item.quality_flag ?? 'UNSPECIFIED'}</p></article>)}</div> : <p className="text-xs text-slate-500">No live AQI observations are available.</p>}</div><div className="dashboard-panel p-4"><h2 className="panel-title flex items-center gap-2"><HeartPulse size={15} className="text-rose-400"/>Health guidance</h2><p className="mt-3 text-sm leading-6 text-slate-300">{guidance}</p>{average != null && <p className="mt-2 text-[10px] text-slate-500">Based on current mean AQI {average}; follow local authority instructions.</p>}</div></section>;
}

function IncidentQueue({ items }: { items: Incident[] }) {
  const client = useQueryClient();
  const [sort, setSort] = useState<'severity' | 'status' | 'created_at'>('severity');
  const [interventionType, setInterventionType] = useState('FIELD_INSPECTION');
  const severityRank: Record<string, number> = { CRITICAL: 5, VERY_HIGH: 4, HIGH: 3, MODERATE: 2, LOW: 1 };
  const sorted = [...items].filter((item) => !['RESOLVED', 'DISMISSED'].includes(item.status)).sort((left, right) => sort === 'severity' ? (severityRank[right.severity] ?? 0) - (severityRank[left.severity] ?? 0) : sort === 'created_at' ? Date.parse(right.updated_at) - Date.parse(left.updated_at) : left.status.localeCompare(right.status));
  const dispatch = useMutation({ mutationFn: async (incident: Incident) => apiClient.request(`/incidents/${incident.id}/dispatch`, { method: 'POST', body: JSON.stringify({ intervention_type: interventionType, executing_agency: 'Municipal response team', action_summary: `Dispatched from command center for ${incident.title}` }) }), onSuccess: async () => { await client.invalidateQueries({ queryKey: ['incidents'] }); await client.invalidateQueries({ queryKey: ['interventions'] }); } });
  return <section className="dashboard-panel mt-3 p-4"><div className="flex flex-wrap items-center justify-between gap-3"><div><h2 className="panel-title">Municipal incident queue</h2><p className="mt-1 text-[10px] text-slate-500">Prioritize and dispatch active incidents using persisted workflows.</p></div><div className="flex flex-wrap gap-2"><label className="flex items-center gap-1 text-[10px] text-slate-500"><ArrowUpDown size={12}/><select value={sort} onChange={(event) => setSort(event.target.value as typeof sort)} className="rounded border border-slate-700 bg-[#030d17] px-2 py-1.5 text-slate-200"><option value="severity">Severity</option><option value="status">Status</option><option value="created_at">Last updated</option></select></label><select aria-label="Intervention type" value={interventionType} onChange={(event) => setInterventionType(event.target.value)} className="rounded border border-slate-700 bg-[#030d17] px-2 py-1.5 text-[10px] text-slate-200"><option value="FIELD_INSPECTION">Field inspection</option><option value="EMISSIONS_CONTROL">Emissions control</option><option value="ROAD_WATERING">Road watering</option><option value="PUBLIC_ADVISORY">Public advisory</option></select></div></div><div className="mt-3 overflow-x-auto">{sorted.length ? <table className="w-full min-w-[720px] text-left text-xs"><thead className="text-[10px] uppercase text-slate-500"><tr><th className="pb-2">Incident</th><th>Severity</th><th>Status</th><th>Created</th><th className="text-right">Action</th></tr></thead><tbody>{sorted.map((item) => <tr key={item.id} className="border-t border-slate-800"><td className="py-3 pr-3"><Link href={`/incidents/${item.id}`} className="font-medium text-slate-200 hover:text-emerald-300">{item.title}</Link></td><td><SeverityIndicator severity={item.severity}/></td><td><StatusBadge status={item.status}/></td><td className="text-slate-500">{new Date(item.created_at).toLocaleString()}</td><td className="text-right"><button disabled={dispatch.isPending || !['OPEN', 'INVESTIGATING'].includes(item.status)} onClick={() => dispatch.mutate(item)} className="rounded bg-emerald-500 px-3 py-1.5 text-[10px] font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-40">Dispatch</button></td></tr>)}</tbody></table> : <p className="py-5 text-center text-xs text-slate-500">No active incidents require dispatch.</p>}</div>{dispatch.error && <p className="mt-3 text-xs text-red-300">{dispatch.error.message}</p>}</section>;
}

export default function DashboardPage() {
  const analytics = useAnalytics();
  const observations = useObservations();
  const incidents = useIncidents();
  const alerts = useAlerts();
  const reportQuery = useReports();
  const hotspots = useHotspots();
  const weather = useWeather();
  const readings = observations.data ?? [];
  const overallAqi = readings.length ? Math.round(readings.reduce((total, item) => total + (item.aqi ?? 0), 0) / readings.length) : 0;
  const highRisk = (incidents.data ?? []).filter((item) => ['HIGH', 'VERY_HIGH', 'CRITICAL'].includes(item.severity)).length;
  return (
    <div className="command-dashboard min-h-[calc(100vh-64px)] p-3 sm:p-4 xl:p-5">
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <StatCard label="Overall AQI (All Regions)" value={overallAqi ? String(overallAqi) : '—'} note={overallAqi > 100 ? 'Unhealthy' : overallAqi ? 'Moderate' : 'Awaiting data'} tone="green" icon={<CloudSun size={25}/>} />
        <StatCard label="Active Hotspots" value={String(hotspots.data?.length ?? 0)} note="Live risk feed" tone="orange" icon={<Flame size={25}/>} />
        <StatCard label="High Risk Events" value={String(highRisk)} note={`${incidents.data?.length ?? 0} total`} tone="red" icon={<ShieldAlert size={25}/>} />
        <StatCard label="Wind Speed" value={weather.data?.wind_speed_kmh != null ? String(Math.round(weather.data.wind_speed_kmh)) : '—'} note="km/h live" tone="blue" icon={<Wind size={25}/>} />
        <StatCard label="Citizen Reports" value={String(analytics.data?.reports ?? reportQuery.data?.length ?? 0)} note="View all" tone="violet" icon={<Users size={25}/>} />
      </div>

      <div className="mt-3 grid gap-3 xl:grid-cols-[minmax(0,2.15fr)_minmax(285px,.78fr)]">
        <section className="dashboard-panel overflow-hidden p-3">
          <div className="mb-3 flex items-center justify-between"><h2 className="panel-title">Live Pollution &amp; Risk Map</h2><span className="flex items-center gap-1.5 text-[10px] text-emerald-400"><i className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400"/>LIVE</span></div>
          <MapCanvas compact />
        </section>
        <CriticalAlert alert={alerts.data?.[0]} />
      </div>

      <div className="mt-3 grid gap-3 lg:grid-cols-2 xl:grid-cols-[1fr_1.1fr_.92fr]">
        <ForecastTable />
        <TrendChart readings={readings} />
        <RecentReports items={reportQuery.data ?? []} />
      </div>

      <AqiOperationsStrip readings={readings}/>
      <IncidentQueue items={incidents.data ?? []}/>

      <footer className="mt-3 flex flex-col gap-3 rounded-xl border border-slate-800/80 bg-[#07131f] px-4 py-3 text-[10px] text-slate-500 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2"><span className="font-semibold text-slate-300">Data Sources</span><span className="flex gap-1.5"><CloudSun size={12}/>Satellite (GEE)</span><span className="flex gap-1.5"><Wind size={12}/>IMD Weather</span><span className="flex gap-1.5"><Radio size={12}/>IoT Sensors</span><span className="flex gap-1.5"><Users size={12}/>Citizen Reports</span></div>
        <div className="flex items-center gap-5"><span><i className={`mr-1.5 inline-block h-2 w-2 rounded-full ${[analytics, observations, incidents, alerts, reportQuery, hotspots, weather].some((query) => query.isError) ? 'bg-red-500' : 'bg-emerald-500'}`}/>{[analytics, observations, incidents, alerts, reportQuery, hotspots, weather].some((query) => query.isError) ? 'One or more data sources unavailable' : 'Connected to live services'}</span></div>
      </footer>
    </div>
  );
}
