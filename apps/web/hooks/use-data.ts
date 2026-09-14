'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export type MapData = { sensors: unknown[]; observations: unknown[]; incidents: unknown[] };

const query = <T,>(key: string, endpoint: string) => useQuery({ queryKey: [key], queryFn: async () => (await apiClient.request<T>(endpoint)).data ?? ([] as T), refetchInterval: 30_000 });
export const useIncidents = () => query<unknown[]>('incidents', '/incidents?limit=100');
export const useSensors = () => query<unknown[]>('sensors', '/sensors?limit=100');
export const useObservations = () => query<unknown[]>('observations', '/environment/latest?limit=100');
export const useAlerts = () => query<unknown[]>('alerts', '/alerts?active=true');
export function useMap() {
  const sensors = useSensors();
  const observations = useObservations();
  const incidents = useIncidents();
  return { data: { sensors: sensors.data ?? [], observations: observations.data ?? [], incidents: incidents.data ?? [] } satisfies MapData, loading: sensors.isLoading || observations.isLoading || incidents.isLoading };
}
