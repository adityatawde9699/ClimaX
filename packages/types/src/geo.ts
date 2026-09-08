/**
 * ClimaX Geospatial Types & Standards
 * Compliant with GeoJSON (RFC 7946) and WGS84 (EPSG:4326).
 */

export interface GeoPoint {
  type: 'Point';
  coordinates: [longitude: number, latitude: number];
}

export interface GeoPolygon {
  type: 'Polygon';
  coordinates: [longitude: number, latitude: number][][];
}

export interface Coordinates {
  latitude: number;
  longitude: number;
  altitude_m?: number;
  accuracy_radius_m?: number;
}

export interface BoundingBox {
  min_longitude: number;
  min_latitude: number;
  max_longitude: number;
  max_latitude: number;
}

export interface SpatialFeature<T = Record<string, unknown>> {
  type: 'Feature';
  geometry: GeoPoint | GeoPolygon;
  properties: T;
}

export interface SpatialFeatureCollection<T = Record<string, unknown>> {
  type: 'FeatureCollection';
  features: SpatialFeature<T>[];
}
