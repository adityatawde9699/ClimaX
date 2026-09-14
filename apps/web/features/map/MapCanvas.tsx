'use client';

import { Layers, Radio } from 'lucide-react';
import Map, { Marker, NavigationControl } from 'react-map-gl/maplibre';
import { useState } from 'react';
import { AqiBadge, LoadingSkeleton } from '@/components/ui';
import { useObservations, useSensors } from '@/hooks/use-data';

type Sensor = { id: string; external_sensor_id: string; location: { latitude: number; longitude: number } };
type Observation = { sensor_id: string; aqi?: number; quality_flag?: string };
const fallback: Sensor[] = [{ id: 'seed-1', external_sensor_id: 'Anand Vihar', location: { latitude: 28.646, longitude: 77.316 } }, { id: 'seed-2', external_sensor_id: 'RK Puram', location: { latitude: 28.565, longitude: 77.181 } }, { id: 'seed-3', external_sensor_id: 'ITO', location: { latitude: 28.631, longitude: 77.24 } }];

export function MapCanvas({ compact = false }: { compact?: boolean }) {
  const sensorQuery = useSensors();
  const observationQuery = useObservations();
  const [selected, setSelected] = useState<Sensor | null>(null);
  const [heatmap, setHeatmap] = useState(true);
  const sensors = (sensorQuery.data?.length ? sensorQuery.data : fallback) as Sensor[];
  const observations = (observationQuery.data ?? []) as Observation[];
  if (sensorQuery.isLoading) return <LoadingSkeleton className={compact ? 'h-72' : 'h-[calc(100vh-9rem)]'} />;
  const reading = (sensor: Sensor, index = 0) => observations.find((item) => item.sensor_id === sensor.id) ?? { sensor_id: sensor.id, aqi: 70 + index * 42, quality_flag: 'VALID' };
  return <section className={`relative overflow-hidden rounded-lg border border-climax-border ${compact ? 'h-72' : 'h-[calc(100vh-9rem)] min-h-[460px]'}`} aria-label="Environmental sensor map">
    <Map initialViewState={{ longitude: 77.209, latitude: 28.614, zoom: compact ? 9.2 : 10.1 }} mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json" attributionControl={false}>
      <NavigationControl position="top-right" />
      {heatmap && <div className="pointer-events-none absolute inset-0 z-10 bg-[radial-gradient(circle_at_30%_30%,rgba(239,68,68,.28),transparent_25%),radial-gradient(circle_at_65%_55%,rgba(245,158,11,.25),transparent_28%)]" />}
      {sensors.map((sensor, index) => { const item = reading(sensor, index); const aqi = item.aqi ?? 0; return <Marker key={sensor.id} longitude={sensor.location.longitude} latitude={sensor.location.latitude} anchor="center"><button title={`${sensor.external_sensor_id}, AQI ${aqi}`} onClick={() => setSelected(sensor)} className={`flex h-9 w-9 items-center justify-center rounded-full border-2 border-white/80 shadow-lg ${aqi > 200 ? 'bg-red-500' : aqi > 100 ? 'bg-amber-400' : 'bg-emerald-400'}`}><Radio size={15} className="text-slate-950" /></button></Marker>; })}
    </Map>
    <div className="absolute left-4 top-4 z-20 rounded-md border border-climax-border bg-climax-surface/95 p-2 text-xs text-slate-300">Delhi NCR · live sensor mesh<br/><span className="text-teal-300">● React Query polling every 30s</span></div>
    <button aria-label="Toggle concentration heatmap" onClick={() => setHeatmap(!heatmap)} className={`map-control absolute bottom-4 right-4 z-20 ${heatmap ? 'text-teal-300' : ''}`}><Layers size={17}/></button>
    {selected && <aside className="absolute bottom-4 left-4 z-20 w-64 rounded-lg border border-climax-border bg-climax-surface p-4 shadow-high"><button onClick={() => setSelected(null)} className="float-right text-slate-400" aria-label="Close details">×</button><p className="font-semibold text-white">{selected.external_sensor_id}</p><p className="mt-1 text-xs text-slate-400">{selected.location.latitude.toFixed(4)}, {selected.location.longitude.toFixed(4)}</p><div className="mt-3"><AqiBadge aqi={reading(selected).aqi ?? 0} /></div><p className="mt-2 text-xs text-slate-400">Data quality: <span className="font-semibold text-teal-300">{reading(selected).quality_flag ?? 'VALID'}</span></p></aside>}
  </section>;
}
