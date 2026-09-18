'use client';

import { Clock3, CloudSun } from 'lucide-react';
import { useState } from 'react';
import { AqiBadge, EmptyState, PageHeader, TierBadge } from '@/components/ui';
import { usePredictions } from '@/hooks/use-data';
import type { Prediction } from '@/types/api';

function PredictionCard({ item, active }: { item: Prediction; active: boolean }) {
  return <section className={`surface-panel relative overflow-hidden p-5 transition ${active ? 'border-cyan-500/50 ring-1 ring-cyan-500/20' : 'hover:border-slate-700'}`}><div className="absolute right-0 top-0 h-24 w-24 rounded-full bg-cyan-500/5 blur-2xl"/><div className="flex items-center justify-between"><TierBadge tier="PREDICTED"/><Clock3 size={16} className="text-slate-600"/></div><p className="mt-5 text-xs uppercase tracking-wider text-slate-500">{item.horizon_hours}-hour horizon</p><p className="mt-1 font-mono text-4xl font-bold text-white">{Math.round(item.predicted_aqi)}<span className="ml-1 text-sm font-normal text-slate-500">AQI</span></p><div className="mt-3"><AqiBadge aqi={Math.round(item.predicted_aqi)}/></div><div className="mt-5 border-t border-slate-800 pt-4 text-xs text-slate-400"><p className="flex justify-between"><span>Predicted PM2.5</span><strong className="text-slate-200">{item.predicted_pm25.toFixed(1)} µg/m³</strong></p><p className="mt-2 flex justify-between"><span>Confidence range</span><strong className="text-slate-200">{item.confidence_interval_low.toFixed(0)}–{item.confidence_interval_high.toFixed(0)}</strong></p></div></section>;
}

export default function PredictionsPage() {
  const [horizon, setHorizon] = useState(24);
  const query = usePredictions(horizon);
  const predictions = query.data ?? [];
  return <div className="page-wrap"><PageHeader eyebrow="Predictive intelligence" title="Air-quality forecast" description="AI-assisted concentration forecasts with confidence bounds for operational planning." actions={<span className="secondary-button"><CloudSun size={15}/>{query.isFetching ? 'Refreshing' : 'Prediction service'}</span>}/><div className="mb-5 flex w-fit gap-1 rounded-lg border border-slate-800 bg-[#071521] p-1">{[6,24,72].map((value) => <button onClick={() => setHorizon(value)} className={`rounded-md px-5 py-2 text-xs font-semibold transition ${horizon === value ? 'bg-emerald-500 text-slate-950' : 'text-slate-400 hover:text-white'}`} key={value}>{value} hours</button>)}</div>{predictions.length ? <div className="grid gap-4 md:grid-cols-3">{predictions.map((item) => <PredictionCard key={item.id} item={item} active={item.horizon_hours === horizon}/>)}</div> : <section className="surface-panel"><EmptyState icon={<CloudSun className="mx-auto text-cyan-400"/>} message={query.isLoading ? 'Loading forecast data…' : query.error?.message || 'No production forecast is available for this location and horizon.'}/></section>}</div>;
}
