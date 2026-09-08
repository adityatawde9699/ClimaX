/**
 * ClimaX Core Domain Entities Contract
 * Represents the unified type definitions across Frontend, Backend, and Data layers.
 */

import { AIExplanationMetadata, InformationTier, PollutionCategory, VerificationStatus } from './ai';
import { Coordinates, GeoPoint } from './geo';

export type UserRole = 'CITIZEN' | 'AUTHORITY' | 'RESEARCHER' | 'ADMIN';

export type IncidentStatus = 'OPEN' | 'INVESTIGATING' | 'DISPATCHED' | 'MITIGATED' | 'RESOLVED' | 'DISMISSED';

export type IncidentSeverity = 'LOW' | 'MODERATE' | 'HIGH' | 'VERY_HIGH' | 'CRITICAL';

export type AlertChannel = 'IN_APP' | 'SMS' | 'PUSH' | 'EMAIL' | 'MUNICIPAL_BROADCAST';

export type SensorType = 'GOVERNMENT_STATION' | 'IOT_LOW_COST' | 'COMMUNITY' | 'SATELLITE_PIXEL';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  organization_id?: string;
  phone_number?: string;
  preferred_language: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Organization {
  id: string;
  name: string;
  jurisdiction_code: string;
  department: string;
  contact_email: string;
  boundary_geojson?: string;
  created_at: string;
}

export interface DataSource {
  id: string;
  name: string;
  source_type: 'SENSOR_NETWORK' | 'GOVERNMENT_API' | 'SATELLITE' | 'CITIZEN' | 'WEATHER';
  provider: string;
  refresh_interval_seconds: number;
  is_active: boolean;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface Sensor {
  id: string;
  data_source_id: string;
  external_sensor_id: string;
  sensor_type: SensorType;
  model_name: string;
  location: Coordinates;
  geometry: GeoPoint;
  elevation_m?: number;
  is_calibrated: boolean;
  is_active: boolean;
  last_ping_at?: string;
  created_at: string;
}

export interface EnvironmentalObservation {
  id: string;
  sensor_id: string;
  timestamp: string;
  tier: InformationTier; // 'OBSERVED'
  pm25?: number;
  pm10?: number;
  no2?: number;
  so2?: number;
  co?: number;
  o3?: number;
  aqi?: number;
  temperature_c?: number;
  humidity_percent?: number;
  wind_speed_kmh?: number;
  wind_direction_deg?: number;
  raw_payload_uri?: string;
  created_at: string;
}

export interface CitizenReport {
  id: string;
  user_id?: string; // Optional for anonymous citizen reporting
  tier: InformationTier; // 'OBSERVED'
  location: Coordinates;
  geometry: GeoPoint;
  address_text?: string;
  category: PollutionCategory;
  description: string;
  media_urls: string[];
  status: 'SUBMITTED' | 'TRIAGED' | 'VERIFIED' | 'RESOLVED';
  incident_id?: string;
  created_at: string;
  updated_at: string;
}

export interface AIAnalysis {
  id: string;
  report_id?: string;
  observation_id?: string;
  tier: InformationTier; // 'INFERRED'
  classification: PollutionCategory;
  explanation: AIExplanationMetadata;
  suggested_severity: IncidentSeverity;
  plume_bounding_box?: [number, number, number, number];
  raw_model_response?: Record<string, unknown>;
  created_at: string;
}

export interface PollutionEvent {
  id: string;
  event_type: string;
  tier: InformationTier; // 'INFERRED' or 'OBSERVED'
  start_time: string;
  end_time?: string;
  geometry: GeoPoint;
  peak_pm25?: number;
  affected_radius_meters: number;
  severity: IncidentSeverity;
  created_at: string;
}

export interface Prediction {
  id: string;
  sensor_id?: string;
  target_location: Coordinates;
  forecast_timestamp: string;
  horizon_hours: number; // 6, 24, 72
  tier: InformationTier; // 'PREDICTED'
  predicted_pm25: number;
  predicted_aqi: number;
  confidence_interval_low: number;
  confidence_interval_high: number;
  explanation: AIExplanationMetadata;
  created_at: string;
}

export interface RiskAssessment {
  id: string;
  location: Coordinates;
  risk_score: number; // 0.0 to 100.0
  severity: IncidentSeverity;
  population_vulnerability_index: number;
  sensitive_receptors_count: number; // Schools, hospitals within 1km
  dominant_pollutant: string;
  calculated_at: string;
}

export interface Alert {
  id: string;
  title: string;
  message: string;
  severity: IncidentSeverity;
  channel: AlertChannel;
  target_geometry?: GeoPoint;
  affected_radius_m?: number;
  is_dispatched: boolean;
  dispatched_at?: string;
  expires_at?: string;
  created_at: string;
}

export interface Incident {
  id: string;
  organization_id: string;
  title: string;
  status: IncidentStatus;
  severity: IncidentSeverity;
  category: PollutionCategory;
  geometry: GeoPoint;
  location: Coordinates;
  assigned_officer_id?: string;
  risk_score?: number;
  ai_analysis_id?: string;
  root_cause_summary?: string;
  created_at: string;
  resolved_at?: string;
}

export interface Verification {
  id: string;
  incident_id: string;
  verified_by_user_id: string;
  tier: InformationTier; // 'VERIFIED'
  status: VerificationStatus;
  official_notes: string;
  field_photos: string[];
  verified_at: string;
}

export interface Intervention {
  id: string;
  incident_id: string;
  intervention_type: 'SMOG_GUN' | 'ROAD_WATERING' | 'FACTORY_HALT' | 'TRAFFIC_DIVERSION' | 'CLEANUP';
  dispatched_at: string;
  executed_at?: string;
  completed_at?: string;
  executing_agency: string;
  action_summary: string;
}

export interface InterventionMeasurement {
  id: string;
  intervention_id: string;
  pre_intervention_pm25: number;
  post_intervention_pm25: number;
  delta_pm25_percent: number;
  evaluation_window_hours: number;
  is_statistically_significant: boolean;
  measured_at: string;
}

export interface AuditLog {
  id: string;
  user_id?: string;
  action: string;
  entity_name: string;
  entity_id: string;
  ip_address?: string;
  changes?: Record<string, unknown>;
  timestamp: string;
}
