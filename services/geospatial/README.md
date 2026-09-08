# Geospatial Domain Service (`services/geospatial`)

Responsible for Google Earth Engine satellite raster processing, PostGIS spatial queries, and Mapbox/Google Maps tile pipelines.

## Responsibilities:
- **Satellite Ingestion (Sentinel-5P / Landsat / MODIS)**: Interfaces with Google Earth Engine Python API to retrieve tropospheric NO2, aerosol optical depth (AOD), and thermal anomaly active fires.
- **Spatial Indexing & Buffers**: Computes spatial buffers around vulnerable receptors (schools, hospitals) and generates spatial Voronoi / Hexbin aggregations for map visualization.
- **Coordinate Reference Systems**: Standardizes spatial data across WGS84 (EPSG:4326) and Web Mercator (EPSG:3857).

## Planned Implementation Phase:
- Phase 2 (Database & Spatial Setup) & Phase 3 (Data Ingestion).
