/**
 * ClimaX Standard API Envelopes & Query Contracts
 */

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: ApiErrorPayload;
  meta?: ApiMetadata;
}

export interface ApiErrorPayload {
  code: string;
  message: string;
  details?: Record<string, unknown>[];
}

export interface ApiMetadata {
  page?: number;
  per_page?: number;
  total_items?: number;
  total_pages?: number;
  request_id?: string;
  timestamp: string;
}

export interface PaginationParams {
  page?: number;
  limit?: number;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

export interface SpatialQueryParams extends PaginationParams {
  latitude?: number;
  longitude?: number;
  radius_km?: number;
  bbox?: [minLng: number, minLat: number, maxLng: number, maxLat: number];
}
