'use client';

import { Flame, MapPin, Radio, ShieldAlert } from 'lucide-react';
import { MapCanvas } from '@/features/map/MapCanvas';
import { useHotspots } from '@/hooks/use-data';
import { EmptyState, PageHeader, SeverityIndicator } from '@/components/ui';

export default function HotspotsPage() {
  const query = useHotspots();
  const hotspots = query.data ?? [];
  return <div className="page-wrap max-w-none">
    <PageHeader eyebrow="Risk intelligence" title="Active hotspots" description="Prioritized environmental risk assessments ranked by current risk score." actions={<span className="secondary-button"><Radio size={15}/>{query.isFetching ? 'Refreshing…' : 'Live feed'}</span>}/>
    <div className="grid gap-5 xl:grid-cols-[minmax(0,1.7fr)_380px]">
      <MapCanvas/>
      <section className="surface-panel min-h-[460px] p-4"><div className="flex items-center justify-between border-b border-slate-800 pb-3"><h2 className="font-semibold text-white">Priority locations</h2><span className="font-mono text-sm text-orange-400">{hotspots.length}</span></div>
        <div className="mt-3 space-y-3">{hotspots.length ? hotspots.map((item, index) => <article key={item.id} className="rounded-xl border border-slate-800 bg-[#04111d] p-4"><div className="flex items-start justify-between gap-3"><div><p className="text-[10px] uppercase tracking-wider text-slate-600">Priority {String(index + 1).padStart(2, '0')}</p><p className="mt-1 flex items-center gap-1.5 text-xs text-slate-300"><MapPin size={12}/>{item.location.latitude.toFixed(3)}, {item.location.longitude.toFixed(3)}</p></div><SeverityIndicator severity={item.severity}/></div><div className="mt-4 flex items-end justify-between"><span className="text-xs text-slate-500">Risk score</span><strong className="font-mono text-2xl text-orange-300">{item.risk_score.toFixed(0)}</strong></div></article>) : <EmptyState icon={<Flame className="mx-auto text-orange-400"/>} message={query.isLoading ? 'Loading hotspot assessments…' : 'No active risk hotspots have been calculated.'}/>}</div>
      </section>
    </div>
    {query.error && <p className="mt-4 rounded-lg border border-red-500/20 bg-red-500/5 p-3 text-sm text-red-300"><ShieldAlert size={15} className="mr-2 inline"/>{query.error.message}</p>}
  </div>;
}
