# AI Architecture Specification

## 1. The ClimaX AI Pipeline

In high-stakes environmental decision making, AI must be verifiable, evidence-grounded, and integrated into human municipal command. The ClimaX AI pipeline enforces a strict 9-stage sequence:

```
  ┌────────────────────────────────────────────────────────┐
  │ 1. INPUT DATA                                          │
  │    (Citizen Photos, Videos, IoT Sensor Streams, Winds) │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. DATA VALIDATION                                     │
  │    (Exif Check, GPS Bounds, Timestamp, Outlier Purge)  │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. FEATURE EXTRACTION                                  │
  │    (Sentinel-5P NO2 Rasters, Elevation, Wind Trajectory│
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 4. AI / ML PROCESSING                                  │
  │    (Gemini 1.5 Multimodal, Vertex AI Plume Predictor)  │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 5. STRUCTURED AI RESULT                                │
  │    (Pydantic Schema: Category, Plume BBox, Severity)   │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 6. CONFIDENCE ASSESSMENT                               │
  │    (Score 0.0 - 1.0 mapped to LOW, MEDIUM, HIGH, CRIT) │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 7. EVIDENCE FORMULATION                                │
  │    (Visual Ringelmann score, sensor delta, wind vector)│
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 8. HUMAN VERIFICATION                                  │
  │    (Municipal field inspection & certificate of fact)  │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 9. ACTION EXECUTION                                    │
  │    (Intervention dispatch, Legal Notice, Citizen Alert)│
  └────────────────────────────────────────────────────────┘
```

---

## 2. Dedicated AI Subsystem Modules

### A. Gemini 1.5 Multimodal (Citizen Media Intelligence)
- **Role**: Visual scene analysis of citizen uploaded photos and video clips.
- **Capabilities**:
  - Distinguishes between biomass burning (white/grey diffuse smoke), industrial emissions (dense black carbonaceous plumes), construction dust (ground-level brown particulate), and false positives (steam clouds, water vapor, overcast fog).
  - Generates normalized bounding box coordinates for visual plumes.
  - Formulates structured evidence citations.

### B. Gemini 1.5 Pro / Flash (Environmental Reasoning & AI Copilot)
- **Role**: High-context synthesis of multi-modal environmental feeds.
- **Capabilities**:
  - Fuses real-time sensor timeseries with wind vectors and cadastral zoning maps to identify likely emitter candidates.
  - Powers the Municipal AI Copilot, answering complex queries such as:
    *"Identify the top 3 contributors to the Anand Vihar AQI spike between 02:00 and 06:00 today, citing supporting sensor readings and wind directions."*

### C. Vertex AI (Predictive Plume Modeling & Forecasting)
- **Role**: Managed ML training, model registry, and serverless endpoint hosting.
- **Capabilities**:
  - Hosts spatio-temporal LSTM / Transformer sequence models predicting localized AQI at 6h, 24h, and 72h horizons.
  - Implements physics-informed neural network (PINN) Gaussian plume dispersion modeling.
  - Exposes low-latency inference endpoints integrated with Cloud Run.

### D. Google Earth Engine (Satellite Feature Extraction)
- **Role**: Planetary-scale Earth observation data processing.
- **Capabilities**:
  - Extracts daily tropospheric NO2 column density from Sentinel-5P TROPOMI.
  - Extracts thermal anomalies (active fire hotspots) from MODIS / VIIRS to detect agricultural stubble burning.
  - Computes spatial zonal statistics across administrative municipal wards.
