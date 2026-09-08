# External Data Sources Catalog

ClimaX harmonizes multi-source data across physical, meteorological, and community streams:

---

## 1. Ground Sensor Telemetry

| Data Source | Parameters | Refresh Cadence | Ingestion Method | License / Access |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAQ Network** | PM2.5, PM10, NO2, SO2, O3, CO | 10 - 60 mins | REST API Ingestion Worker | Open Data (CC BY 4.0) |
| **CPCB India (CAAQMS)** | PM2.5, PM10, NOx, NH3, Benzene | 15 mins | Scraped API / Government Feed | Public Government Use |
| **EPA AirNow (US)** | PM2.5, Ozone, AQI | 60 mins | AirNow Gateway API | Public Domain |
| **Community IoT Mesh** | PM2.5, PM10, Temp, Humidity | 1 - 5 mins | MQTT Broker / Cloud Pub/Sub | Proprietary / Community |

---

## 2. Satellite & Earth Observation (Google Earth Engine)

| Satellite / Instrument | Derived Product | Spatial Resolution | Temporal Frequency | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Sentinel-5P TROPOMI** | Tropospheric NO2, Carbon Monoxide | 3.5 km x 5.5 km | Daily overpass (~13:30 local) | Urban industrial emission plumes |
| **MODIS (Terra & Aqua)** | Aerosol Optical Depth (AOD) | 1 km / 3 km | 2 passes daily | Regional background particulate haze |
| **VIIRS (Suomi NPP)** | Thermal Anomalies (Active Fires) | 375 m | Daily & Nightly passes | Stubble & agricultural burning detection |
| **Landsat 8 / 9 (OLI)** | Land Surface Temp, Urban Albedo | 30 m | 8 - 16 days | Urban heat islands & dust emissivity |

---

## 3. Meteorology & Atmospheric Physics

| Source | Parameters | Forecast Horizon | Use Case |
| :--- | :--- | :--- | :--- |
| **NOAA GFS** | Wind speed, wind direction, temp, surface pressure | 0 - 384 hours | Macro atmospheric advection modeling |
| **ECMWF ERA5 / IFS** | Boundary layer height, thermal inversions | 0 - 72 hours | Inversion trapping & stagnation prediction |
| **OpenWeatherMap API** | Localized hyper-local surface wind and humidity | Hourly | Immediate street-canyon dispersion input |

---

## 4. Cadastral & Demographic Context

| Dataset | Provider | Usage in ClimaX |
| :--- | :--- | :--- |
| **Sensitive Receptors** | OpenStreetMap / Municipal GIS | Buffer intersections for schools, daycares, hospitals, elderly homes |
| **Industrial Zoning** | State Pollution Control Boards | Back-trajectory emitter candidate matching |
| **Population Density** | WorldPop / CIESIN Gridded Population | Population Vulnerability Index weighting for Risk Engine |
