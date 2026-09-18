'use client';

import { Database, Download, Radio, Search } from 'lucide-react';
import { useMemo, useState, type ReactNode } from 'react';
import { DataTable, EmptyState, PageHeader, StatusBadge } from '@/components/ui';
import { useObservations, useReports, useSensors } from '@/hooks/use-data';

type Dataset = 'sensors' | 'observations' | 'reports';

export default function DataExplorerPage() {
  const [dataset, setDataset] = useState<Dataset>('sensors'); const [filter, setFilter] = useState('');
  const sensors = useSensors(); const observations = useObservations(); const reports = useReports();
  const table = useMemo<{ columns: string[]; rows: ReactNode[][] }>(() => {
    const needle = filter.toLowerCase();
    if (dataset === 'observations') return { columns: ['Sensor', 'Timestamp', 'AQI', 'PM2.5', 'Quality'], rows: (observations.data ?? []).filter((item) => JSON.stringify(item).toLowerCase().includes(needle)).map((item) => [item.sensor_id, new Date(item.timestamp).toLocaleString(), item.aqi ?? '—', item.pm25 ?? '—', <StatusBadge key={item.id} status={item.quality_flag ?? 'VALID'}/>]) };
    if (dataset === 'reports') return { columns: ['Category', 'Description', 'Location', 'Status'], rows: (reports.data ?? []).filter((item) => JSON.stringify(item).toLowerCase().includes(needle)).map((item) => [item.category.replaceAll('_', ' '), item.description, `${item.location.latitude.toFixed(3)}, ${item.location.longitude.toFixed(3)}`, <StatusBadge key={item.id} status={item.status}/>]) };
    return { columns: ['Sensor', 'Type', 'Model', 'Location', 'Status'], rows: (sensors.data ?? []).filter((item) => JSON.stringify(item).toLowerCase().includes(needle)).map((item) => [item.external_sensor_id, item.sensor_type.replaceAll('_', ' '), item.model_name, `${item.location.latitude.toFixed(3)}, ${item.location.longitude.toFixed(3)}`, <StatusBadge key={item.id} status={item.is_active ? 'ACTIVE' : 'INACTIVE'}/>]) };
  }, [dataset, filter, observations.data, reports.data, sensors.data]);
  const loading = sensors.isLoading || observations.isLoading || reports.isLoading;
  return <div className="page-wrap max-w-none"><PageHeader eyebrow="Environmental data plane" title="Data explorer" description="Search and inspect normalized sensors, observations, and citizen evidence." actions={<button type="button" onClick={() => { const blob = new Blob([JSON.stringify(table.rows.map((row) => row.map(String)), null, 2)], { type: 'application/json' }); const link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = `climax-${dataset}.json`; link.click(); URL.revokeObjectURL(link.href); }} className="secondary-button"><Download size={15}/>Export view</button>}/>
    <div className="mb-5 flex flex-col gap-3 rounded-xl border border-slate-800 bg-[#071521] p-3 sm:flex-row sm:items-center sm:justify-between"><div className="flex gap-1">{(['sensors','observations','reports'] as Dataset[]).map((item) => <button key={item} onClick={() => setDataset(item)} className={`rounded-lg px-4 py-2 text-xs font-semibold capitalize ${dataset === item ? 'bg-emerald-500 text-slate-950' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>{item}</button>)}</div><label className="relative"><Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"/><input value={filter} onChange={(event) => setFilter(event.target.value)} className="input min-w-[260px] pl-9" placeholder={`Filter ${dataset}…`}/></label></div>
    {table.rows.length ? <DataTable columns={table.columns} rows={table.rows}/> : <div className="surface-panel"><EmptyState icon={<Database className="mx-auto text-sky-400"/>} message={loading ? 'Loading environmental datasets…' : `No matching ${dataset} found.`} cta={<span className="text-xs"><Radio size={13} className="mr-1 inline"/>Live API dataset</span>}/></div>}
  </div>;
}
