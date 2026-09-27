'use client';

import { Layers3 } from 'lucide-react';
import { useEffect, useMemo, useRef, useState } from 'react';
import type * as Leaflet from 'leaflet';
import { AqiBadge, LoadingSkeleton } from '@/components/ui';
import { useHotspots, useIncidents, useInterventions, useObservations, usePredictions, useSensors } from '@/hooks/use-data';
import type { Sensor } from '@/types/api';

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
  const [mapReady, setMapReady] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<Leaflet.Map | null>(null);
  const leafletRef = useRef<typeof Leaflet | null>(null);
  const overlaysRef = useRef<Leaflet.LayerGroup | null>(null);
  const sensors = useMemo(() => sensorQuery.data ?? [], [sensorQuery.data]);
  const observations = useMemo(() => observationQuery.data ?? [], [observationQuery.data]);
  const risks = useMemo(() => riskQuery.data ?? [], [riskQuery.data]);
  const predictions = useMemo(() => predictionQuery.data ?? [], [predictionQuery.data]);
  const incidents = useMemo(() => incidentQuery.data ?? [], [incidentQuery.data]);
  const interventions = useMemo(() => interventionQuery.data ?? [], [interventionQuery.data]);
  const demoMode = process.env.NEXT_PUBLIC_DEMO_MODE === 'true';

  useEffect(() => {
    if (sensorQuery.isLoading || !containerRef.current) return;
    let cancelled = false;
    void import('leaflet').then((L) => {
      if (cancelled || !containerRef.current) return;
      const map = L.map(containerRef.current, { zoomControl: false }).setView(compact ? [25.1, 78.8] : [28.614, 77.209], compact ? 4 : 10);
      L.tileLayer(process.env.NEXT_PUBLIC_OSM_TILE_URL || 'https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors', maxZoom: 19,
      }).addTo(map);
      L.control.zoom({ position: 'topright' }).addTo(map);
      overlaysRef.current = L.layerGroup().addTo(map);
      leafletRef.current = L;
      mapRef.current = map;
      setMapReady(true);
    });
    return () => {
      cancelled = true;
      mapRef.current?.remove();
      mapRef.current = null;
      leafletRef.current = null;
      overlaysRef.current = null;
      setMapReady(false);
    };
  }, [compact, sensorQuery.isLoading]);

  useEffect(() => {
    const L = leafletRef.current;
    const overlays = overlaysRef.current;
    if (!mapReady || !L || !overlays) return;
    overlays.clearLayers();
    if (layers.risk) risks.forEach((risk) => {
      const critical = risk.severity === 'CRITICAL';
      L.circleMarker([risk.location.latitude, risk.location.longitude], {
        radius: critical ? 34 : 27, color: critical ? '#f87171' : '#fb923c',
        fillColor: critical ? '#ef4444' : '#f97316', fillOpacity: 0.26, weight: 1,
      }).bindTooltip(`Risk ${Math.round(risk.risk_score * (risk.risk_score <= 1 ? 100 : 1))}: ${risk.severity}`).addTo(overlays);
    });
    if (layers.predictions) predictions.forEach((prediction) => {
      L.circleMarker([prediction.latitude, prediction.longitude], {
        radius: 18, color: '#67e8f9', fillColor: '#22d3ee', fillOpacity: 0.3, weight: 1,
      }).bindTooltip(`${predictionHorizon}h predicted AQI ${Math.round(prediction.predicted_aqi)}`).addTo(overlays);
    });
    if (layers.interventions) interventions.forEach((intervention) => {
      const incident = incidents.find((item) => item.id === intervention.incident_id);
      if (!incident) return;
      const status = intervention.completed_at ? 'Completed' : intervention.executed_at ? 'Executing' : 'Dispatched';
      L.circleMarker([incident.location.latitude, incident.location.longitude], {
        radius: 13, color: '#c4b5fd', fillColor: '#7c3aed', fillOpacity: 0.9, weight: 2,
      }).bindTooltip(`${intervention.intervention_type.replaceAll('_', ' ')} · ${status}`).addTo(overlays);
    });
    if (layers.sensors) sensors.forEach((sensor) => {
      const aqi = observations.find((item) => item.sensor_id === sensor.id)?.aqi;
      const color = aqi == null ? '#64748b' : aqi > 200 ? '#ef4444' : aqi > 100 ? '#f97316' : '#34d399';
      const tooltip = document.createElement('span');
      tooltip.textContent = `${sensor.external_sensor_id}${aqi == null ? ', no current reading' : `, AQI ${aqi}`}`;
      L.circleMarker([sensor.location.latitude, sensor.location.longitude], {
        radius: 11, color: '#ffffff', fillColor: color, fillOpacity: 1, weight: 2,
      }).bindTooltip(tooltip).on('click', () => setSelected(sensor)).addTo(overlays);
    });
  }, [mapReady, layers, sensors, observations, risks, predictions, interventions, incidents, predictionHorizon]);

  if (sensorQuery.isLoading) return <LoadingSkeleton className={compact ? 'h-[410px]' : 'h-[calc(100vh-9rem)]'} />;
  const reading = (sensor: Sensor) => observations.find((item) => item.sensor_id === sensor.id);
  return <section className={`relative overflow-hidden rounded-lg border border-slate-800 ${compact ? 'h-[410px]' : 'h-[calc(100vh-9rem)] min-h-[460px]'}`} aria-label="Environmental sensor map">
    <div ref={containerRef} className="h-full w-full bg-[#071521]" />
    <div className="absolute right-12 top-3 z-[1000] flex flex-wrap justify-end gap-1 rounded-lg border border-slate-700/70 bg-[#061421]/95 p-1.5 shadow-lg"><span className="grid place-items-center px-1 text-slate-400"><Layers3 size={13}/></span>{(Object.keys(layers) as (keyof Layers)[]).map((layer) => <button key={layer} onClick={() => setLayers((current) => ({ ...current, [layer]: !current[layer] }))} className={`rounded px-2 py-1 text-[9px] font-semibold capitalize ${layers[layer] ? 'bg-emerald-500 text-slate-950' : 'bg-slate-800 text-slate-400'}`}>{layer}</button>)}</div>
    {layers.predictions && <div className="absolute right-3 top-14 z-[1000] flex gap-1 rounded-lg border border-slate-700/70 bg-[#061421]/95 p-1 shadow-lg" aria-label="Prediction horizon">{[6, 24, 72].map((hours) => <button key={hours} onClick={() => setPredictionHorizon(hours)} className={`rounded px-2 py-1 text-[9px] font-semibold ${predictionHorizon === hours ? 'bg-cyan-500 text-slate-950' : 'text-slate-300 hover:bg-slate-800'}`}>{hours}h</button>)}</div>}
    {compact ? <><div className="absolute left-3 top-3 z-[1000] rounded-lg border border-slate-700/70 bg-[#061421]/95 px-3 py-2 text-[10px] text-slate-300 shadow-lg">{sensors.length} {demoMode ? 'demo' : 'live'} sensor{sensors.length === 1 ? '' : 's'}</div><div className="absolute bottom-3 left-3 z-[1000] rounded-lg border border-slate-700/70 bg-[#061421]/95 p-3 text-[9px] text-slate-400 shadow-lg"><p className="mb-2 font-semibold text-slate-200">AQI Scale (PM2.5)</p>{[['bg-emerald-500','Good (0–50)'],['bg-amber-400','Moderate (51–100)'],['bg-orange-500','Unhealthy (101–150)'],['bg-red-500','Very unhealthy (151–200)'],['bg-violet-500','Hazardous (200+)']].map(([color,label]) => <p key={label} className="mt-1 flex items-center gap-2"><i className={`h-1.5 w-1.5 rounded-full ${color}`}/>{label}</p>)}</div></> : <div className="absolute left-4 top-4 z-[1000] rounded-md border border-climax-border bg-climax-surface/95 p-2 text-xs text-slate-300">{sensors.length} {demoMode ? 'demo' : 'live'} sensor{sensors.length === 1 ? '' : 's'}<br/><span className="text-teal-300">● {demoMode ? 'Sample readings' : 'Updates every 30 seconds'}</span></div>}
    {!sensors.length && <div className="pointer-events-none absolute inset-0 z-[1000] grid place-items-center"><p className="rounded-lg border border-slate-700 bg-[#061421]/95 px-4 py-3 text-sm text-slate-300">No sensor data is available.</p></div>}
    {selected && <aside className="absolute bottom-4 left-4 z-[1000] w-64 rounded-lg border border-climax-border bg-climax-surface p-4 shadow-high"><button onClick={() => setSelected(null)} className="float-right text-slate-400" aria-label="Close details">×</button><p className="font-semibold text-white">{selected.external_sensor_id}</p><p className="mt-1 text-xs text-slate-400">{selected.location.latitude.toFixed(4)}, {selected.location.longitude.toFixed(4)}</p>{reading(selected)?.aqi == null ? <p className="mt-3 text-xs text-slate-500">No current observation</p> : <><div className="mt-3"><AqiBadge aqi={reading(selected)?.aqi ?? 0}/></div><p className="mt-2 text-xs text-slate-400">Data quality: <span className="font-semibold text-teal-300">{reading(selected)?.quality_flag ?? 'UNSPECIFIED'}</span></p></>}</aside>}
  </section>;
}
