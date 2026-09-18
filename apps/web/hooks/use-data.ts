'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import type { Alert, AnalyticsSummary, CitizenReport, Incident, Intervention, Observation, Prediction, RiskAssessment, Sensor, User, Weather } from '@/types/api';

const useApiQuery = <T,>(key: readonly unknown[], endpoint: string, enabled = true) => useQuery({ queryKey: key, queryFn: async () => (await apiClient.request<T>(endpoint)).data, enabled, refetchInterval: 30_000 });

export const useIncidents = () => useApiQuery<Incident[]>(['incidents'], '/incidents/');
export const useIncident = (id: string) => useApiQuery<Incident>(['incident', id], `/incidents/${id}`, Boolean(id));
export const useSensors = () => useApiQuery<Sensor[]>(['sensors'], '/sensors/?limit=100');
export const useObservations = () => useApiQuery<Observation[]>(['observations'], '/environment/latest?limit=100');
export const useAlerts = (enabled = true) => useApiQuery<Alert[]>(['alerts'], '/alerts/?active=true', enabled);
export const useReports = () => useApiQuery<CitizenReport[]>(['reports'], '/reports/');
export const useInterventions = () => useApiQuery<Intervention[]>(['interventions'], '/interventions/');
export const usePredictions = (horizon: number, lat = 28.6, lng = 77.2) => useApiQuery<Prediction[]>(['predictions', horizon, lat, lng], `/predictions?lat=${lat}&lng=${lng}&horizon_hours=${horizon}`);
export const useHotspots = () => useApiQuery<RiskAssessment[]>(['risk-hotspots'], '/risk/hotspots');
export const useRisk = (lat = 28.6, lng = 77.2) => useApiQuery<RiskAssessment>(['risk', lat, lng], `/risk?lat=${lat}&lng=${lng}`);
export const useWeather = (lat = 28.6, lng = 77.2) => useApiQuery<Weather>(['weather', lat, lng], `/weather?lat=${lat}&lng=${lng}`);
export const useAnalytics = () => useApiQuery<AnalyticsSummary>(['analytics-summary'], '/analytics/summary');
export const useCurrentUser = (enabled = true) => useApiQuery<User>(['current-user'], '/users/me', enabled);

export function useMap() {
  const sensors = useSensors();
  const observations = useObservations();
  const incidents = useIncidents();
  return { data: { sensors: sensors.data ?? [], observations: observations.data ?? [], incidents: incidents.data ?? [] }, loading: sensors.isLoading || observations.isLoading || incidents.isLoading };
}
