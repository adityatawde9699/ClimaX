# Geospatial Architecture Specification

## 1. Coordinate Reference Systems (CRS) Standards

To avoid coordinate distortions, ClimaX enforces strict CRS conventions across the stack:

| Layer | Standard CRS | Justification |
| :--- | :--- | :--- |
| **Database Storage (PostGIS)** | `EPSG:4326` (WGS84 Lat/Lon) | Universal standard for GPS and GeoJSON geometry storage. |
| **Spatial Distance Calculations** | `Geography(Point, 4326)` / Haversine | Ellipsoidal geodesic calculations ensuring meter accuracy across latitudes. |
| **Web Vector Tile Display** | `EPSG:3857` (Spherical Web Mercator) | Standard projection for Google Maps, Mapbox, and OpenStreetMap rendering engines. |
| **Satellite Earth Engine Rasters** | Native sensor CRS reprojected to `EPSG:4326` | Aligns Sentinel-5P and MODIS pixels directly with ground sensor coordinates. |

---

## 2. Spatial Query Patterns

### A. Proximity Query (Radius Search)
Retrieves all sensors, citizen reports, or historical incidents within a specified kilometer radius of a point:
```sql
SELECT id, model_name, ST_Distance(geom, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography) AS distance_meters
FROM sensors
WHERE ST_DWithin(geom::geography, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, :radius_meters)
ORDER BY distance_meters ASC;
```

### B. Sensitive Receptor Buffer Intersection
Calculates whether an unmitigated industrial emission plume intersects sensitive infrastructure (e.g. schools, healthcare centers, dense housing):
```sql
SELECT r.id, r.name, r.receptor_type
FROM sensitive_receptors r
WHERE ST_Intersects(r.geom, ST_Buffer(ST_SetSRID(ST_MakePoint(:plume_lon, :plume_lat), 4326)::geography, :plume_radius_m)::geometry);
```

---

## 3. Visualization Pipeline & Vector Tiles

1. **High-Density Sensor Aggregation**: Employs spatial hexbinning (Uber H3 or PostGIS `ST_HexagonGrid`) when map zoom is <= 12 to prevent browser DOM thrashing from rendering tens of thousands of individual points.
2. **Plume Dispersion Isopleths**: Converts Vertex AI Gaussian plume calculations into GeoJSON multi-polygons with opacity contours corresponding to concentration brackets (50, 100, 200 µg/m³).
