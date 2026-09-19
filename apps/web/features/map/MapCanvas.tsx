'use client';

import { Flame, Layers3, Truck } from 'lucide-react';
import Map, { Marker, NavigationControl } from 'react-map-gl/maplibre';
import { useState } from 'react';
import { AqiBadge, LoadingSkeleton } from '@/components/ui';
import { useHotspots, useIncidents, useInterventions, useObservations, usePredictions, useSensors } from '@/hooks/use-data';
import type { Observation, RiskAssessment, Sensor } from '@/types/api';

type Layers = { sensors: boolean; risk: boolean; predictions: boolean; interventions: boolean };

export function MapCanvas({ compact = false }: { compact?: boolean }) {
  const [predictionHorizon, setPredictionHorizon] = useState(24);
  const sensorQuery = useSensors();
  const observationQuery = useObservations();
  const riskQuery = useHotspots();
  const predictionQuery = usePredictions(predictionHorizon);
  const interventionQuery = useInterventions();
  const incidentQuery = useIncidents();
  const [selected, setSelected] = useState<Sensor | null>(null);
  const [layers, setLayers] = useState<Layers>({ sensors: true, risk: true, predictions: true, interventions: true });
  const sensors = sensorQuery.data ?? [];
  const observations = observationQuery.data ?? [];
  const risks = riskQuery.data ?? [];
  const predictions = predictionQuery.data ?? [];
  const incidents = incidentQuery.data ?? [];
  const interventions = interventionQuery.data ?? [];
  if (sensorQuery.isLoading) return <LoadingSkeleton className={compact ? 'h-[410px]' : 'h-[calc(100vh-9rem)]'} />;
  const reading = (sensor: Sensor) => observations.find((item) => item.sensor_id === sensor.id);
  return <section className={`relative overflow-hidden rounded-lg border border-slate-800 ${compact ? 'h-[410px]' : 'h-[calc(100vh-9rem)] min-h-[460px]'}`} aria-label="Environmental sensor map">
    <Map initialViewState={{ longitude: compact ? 78.8 : 77.209, latitude: compact ? 25.1 : 28.614, zoom: compact ? 4.25 : 10.1 }} mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json" attributionControl={false}>
      <NavigationControl position="top-right" />
      {layers.risk && risks.map((risk: RiskAssessment) => <Marker key={`risk-${risk.id}`} longitude={risk.location.longitude} latitude={risk.location.latitude} anchor="center"><div title={`Risk ${Math.round(risk.risk_score * (risk.risk_score <= 1 ? 100 : 1))}: ${risk.severity}`} className={`pointer-events-none rounded-full border shadow-[0_0_35px_currentColor] ${risk.severity === 'CRITICAL' ? 'border-red-400/70 bg-red-500/30 text-red-500' : 'border-orange-400/60 bg-orange-500/25 text-orange-500'}`} style={{ width: `${36 + Math.min(64, risk.risk_score * (risk.risk_score <= 1 ? 70 : .7))}px`, height: `${36 + Math.min(64, risk.risk_score * (risk.risk_score <= 1 ? 70 : .7))}px` }}/></Marker>)}
      {layers.predictions && predictions.map((prediction) => <Marker key={`prediction-${prediction.id}`} longitude={prediction.longitude} latitude={prediction.latitude} anchor="center"><div title={`${predictionHorizon}h predicted AQI ${Math.round(prediction.predicted_aqi)}`} className="pointer-events-none grid h-16 w-16 place-items-center rounded-full border border-cyan-300/60 bg-cyan-400/15 text-[9px] font-bold text-cyan-100 shadow-[0_0_30px_rgba(34,211,238,.45)]">{Math.round(prediction.predicted_aqi)}</div></Marker>)}
      {layers.interventions && interventions.map((intervention) => { const incident = incidents.find((item) => item.id === intervention.incident_id); if (!incident) return null; const status = intervention.completed_at ? 'Completed' : intervention.executed_at ? 'Executing' : 'Dispatched'; return <Marker key={`intervention-${intervention.id}`} longitude={incident.location.longitude} latitude={incident.location.latitude} anchor="bottom"><div title={`${intervention.intervention_type.replaceAll('_', ' ')} · ${status}`} className="grid h-8 w-8 place-items-center rounded-lg border border-violet-300/70 bg-violet-600 text-white shadow-[0_0_18px_rgba(139,92,246,.55)]"><Truck size={14}/></div></Marker>; })}
      {layers.sensors && sensors.map((sensor) => { const item = reading(sensor); const aqi = item?.aqi; return <Marker key={sensor.id} longitude={sensor.location.longitude} latitude={sensor.location.latitude} anchor="center"><button title={`${sensor.external_sensor_id}${aqi == null ? ', no current reading' : `, AQI ${aqi}`}`} onClick={() => setSelected(sensor)} className={`flex h-8 w-8 items-center justify-center rounded-full border-2 border-white/80 shadow-[0_0_18px_currentColor] transition hover:scale-110 ${aqi == null ? 'bg-slate-500 text-slate-500' : aqi > 200 ? 'bg-red-500 text-red-500' : aqi > 100 ? 'bg-orange-500 text-orange-500' : 'bg-emerald-400 text-emerald-400'}`}><Flame size={13} className="text-slate-950" /></button></Marker>; })}
    </Map>
    <div className="absolute right-12 top-3 z-20 flex flex-wrap justify-end gap-1 rounded-lg border border-slate-700/70 bg-[#061421]/95 p-1.5 shadow-lg"><span className="grid place-items-center px-1 text-slate-400"><Layers3 size={13}/></span>{(Object.keys(layers) as (keyof Layers)[]).map((layer) => <button key={layer} onClick={() => setLayers((current) => ({ ...current, [layer]: !current[layer] }))} className={`rounded px-2 py-1 text-[9px] font-semibold capitalize ${layers[layer] ? 'bg-emerald-500 text-slate-950' : 'bg-slate-800 text-slate-400'}`}>{layer}</button>)}</div>
    {layers.predictions && <div className="absolute right-3 top-14 z-20 flex gap-1 rounded-lg border border-slate-700/70 bg-[#061421]/95 p-1 shadow-lg" aria-label="Prediction horizon">{[6, 24, 72].map((hours) => <button key={hours} onClick={() => setPredictionHorizon(hours)} className={`rounded px-2 py-1 text-[9px] font-semibold ${predictionHorizon === hours ? 'bg-cyan-500 text-slate-950' : 'text-slate-300 hover:bg-slate-800'}`}>{hours}h</button>)}</div>}
    {compact ? <>
      <div className="absolute left-3 top-3 z-20 rounded-lg border border-slate-700/70 bg-[#061421]/95 px-3 py-2 text-[10px] text-slate-300 shadow-lg">{sensors.length} live sensor{sensors.length === 1 ? '' : 's'}</div>
      <div className="absolute bottom-3 left-3 z-20 rounded-lg border border-slate-700/70 bg-[#061421]/95 p-3 text-[9px] text-slate-400 shadow-lg"><p className="mb-2 font-semibold text-slate-200">AQI Scale (PM2.5)</p>{[['bg-emerald-500','Good (0–50)'],['bg-amber-400','Moderate (51–100)'],['bg-orange-500','Unhealthy (101–150)'],['bg-red-500','Very unhealthy (151–200)'],['bg-violet-500','Hazardous (200+)']].map(([color,label]) => <p key={label} className="mt-1 flex items-center gap-2"><i className={`h-1.5 w-1.5 rounded-full ${color}`}/>{label}</p>)}</div>
    </> : <div className="absolute left-4 top-4 z-20 rounded-md border border-climax-border bg-climax-surface/95 p-2 text-xs text-slate-300">{sensors.length} live sensor{sensors.length === 1 ? '' : 's'}<br/><span className="text-teal-300">● Updates every 30 seconds</span></div>}
    {!sensors.length && !sensorQuery.isLoading && <div className="pointer-events-none absolute inset-0 z-10 grid place-items-center"><p className="rounded-lg border border-slate-700 bg-[#061421]/95 px-4 py-3 text-sm text-slate-300">No sensor data is available.</p></div>}
    {selected && <aside className="absolute bottom-4 left-4 z-20 w-64 rounded-lg border border-climax-border bg-climax-surface p-4 shadow-high"><button onClick={() => setSelected(null)} className="float-right text-slate-400" aria-label="Close details">×</button><p className="font-semibold text-white">{selected.external_sensor_id}</p><p className="mt-1 text-xs text-slate-400">{selected.location.latitude.toFixed(4)}, {selected.location.longitude.toFixed(4)}</p>{reading(selected)?.aqi == null ? <p className="mt-3 text-xs text-slate-500">No current observation</p> : <><div className="mt-3"><AqiBadge aqi={reading(selected)?.aqi ?? 0}/></div><p className="mt-2 text-xs text-slate-400">Data quality: <span className="font-semibold text-teal-300">{reading(selected)?.quality_flag ?? 'UNSPECIFIED'}</span></p></>}</aside>}
  </section>;
}
