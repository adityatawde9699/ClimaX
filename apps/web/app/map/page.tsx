import { Layers3, LocateFixed } from 'lucide-react';
import { PageHeader } from '@/components/ui';
import { MapCanvas } from '@/features/map/MapCanvas';

export default function MapPage() {
  return <div className="page-wrap max-w-none"><PageHeader eyebrow="Live intelligence" title="Environmental risk map" description="Explore real-time sensor observations, AQI concentration layers, and active pollution events across the region." actions={<><button className="secondary-button"><Layers3 size={15}/>Layers</button><button className="primary-button"><LocateFixed size={15}/>Use my location</button></>}/><MapCanvas /></div>;
}
