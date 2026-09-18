'use client';

import { Globe2, Radio, Wind } from 'lucide-react';
import { MapCanvas } from '@/features/map/MapCanvas';
import { EmptyState, PageHeader } from '@/components/ui';
import { useAlerts, useHotspots, useWeather } from '@/hooks/use-data';

export default function CrossBorderPage() {
  const hotspots = useHotspots(); const alerts = useAlerts(); const weather = useWeather();
  return <div className="page-wrap max-w-none"><PageHeader eyebrow="Federated intelligence" title="Cross-border environmental view" description="Shared regional risk signals and atmospheric transport context from configured federation nodes." actions={<span className="secondary-button"><Globe2 size={15}/>Federation registry</span>}/>
    <div className="mb-5 grid gap-3 sm:grid-cols-3"><section className="surface-panel p-4"><p className="text-xs text-slate-500">Shared hotspots</p><p className="mt-2 font-mono text-2xl font-bold text-orange-400">{hotspots.data?.length ?? 0}</p></section><section className="surface-panel p-4"><p className="text-xs text-slate-500">Cross-border alerts</p><p className="mt-2 font-mono text-2xl font-bold text-red-400">{alerts.data?.length ?? 0}</p></section><section className="surface-panel p-4"><p className="text-xs text-slate-500">Delhi wind</p><p className="mt-2 flex items-center gap-2 font-mono text-2xl font-bold text-sky-400"><Wind size={19}/>{weather.data?.wind_speed_kmh != null ? Math.round(weather.data.wind_speed_kmh) : '—'} <small className="text-xs text-slate-500">km/h</small></p></section></div>
    <div className="grid gap-5 xl:grid-cols-[minmax(0,1.8fr)_340px]"><MapCanvas/><section className="surface-panel p-4"><h2 className="font-semibold text-white">Federation status</h2><div className="mt-4"><EmptyState icon={<Radio className="mx-auto text-sky-400"/>} message="No federation node registry is configured. Connected nodes will appear here when the production registry is available."/></div></section></div>
  </div>;
}
