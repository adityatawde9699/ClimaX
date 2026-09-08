# Frontend Architecture Specification

## 1. Architectural Strategy

The ClimaX frontend is structured as a unified Next.js 14+ application with explicit feature-based boundaries. It supports four distinct persona journeys from a single cohesive repository without fragmenting into disparate single-page apps.

### Key Architectural Tenets:
1. **Feature-First Organization**: Code is organized around business features (`features/command-center`, `features/citizen-reports`, `features/pollution-map`) rather than flat technical categories.
2. **Design System Token Discipline**: All visual styling strictly references `@climax/ui` tokens (`climax.bg`, `climax.surface`, `aqi.*`). Ad-hoc hex values and arbitrary Tailwind classes are prohibited.
3. **No Unnecessary Client Logic**: Dynamic geospatial rendering occurs via WebGL/Canvas, while metadata and dashboard routing leverage Next.js Server Components for initial load speed.

---

## 2. Directory Layout & Route Groups

```text
apps/web/
├── app/
│   ├── (auth)/          # Authentication views (Login, Token Exchange)
│   ├── (citizen)/       # Citizen-facing mobile-first views
│   ├── (authority)/     # Municipal Command Center & Incident triage
│   ├── (researcher)/    # BigQuery Data Studio & spatial explorer
│   ├── (admin)/         # System admin, sensor health, and RBAC
│   ├── layout.tsx       # Universal dark-mode technical shell
│   └── page.tsx         # Phase 0 architectural entrypoint
├── components/          # Shared atomic components (ui, layout, maps, feedback)
├── features/            # Feature modules (12 primary modules + citizen submodules)
├── hooks/               # Custom hooks (geolocation, pollution queries)
├── lib/                 # Base API client and common browser utilities
└── styles/              # Design tokens and Tailwind custom properties
```

---

## 3. Persona Interface Subsystems

### A. Citizen Experience (`app/(citizen)`)
- **Design Target**: Mobile-first, high-contrast, touch-optimized (48px touch targets), offline-resilient.
- **Key Modules**:
  - `home`: Current local AQI, immediate health risk category, 1-tap emergency action.
  - `map`: Simplified interactive vector map with GPS geolocation locator.
  - `report`: Camera capture, GPS reverse geocoding, multi-category picker.
  - `assistant`: Conversational Gemini 1.5 interface explaining air quality in plain local language.

### B. Authority Command Center (`app/(authority)`)
- **Design Target**: Desktop 24/7 command console, multi-monitor high-density layout.
- **Key Modules**:
  - `command-center`: Dual-pane live situational map and active incident triage feed.
  - `incidents`: Field officer dispatch, priority re-assignment, and verification reviews.
  - `predictions`: Forward-looking 6h-72h plume simulation overlays.
  - `interventions`: Anti-smog gun tracker and pre/post intervention measurement deltas.
  - `ai-copilot`: Grounded municipal reasoning assistant for rapid regulatory analysis.

### C. Researcher Data Explorer (`app/(researcher)`)
- **Design Target**: Large dataset manipulation, statistical charts, spatial query builder.
- **Key Modules**:
  - `data-explorer`: BigQuery query interface, spatial bounding-box filters, multi-parameter correlation plots.
  - `export`: Formatted data bundles (GeoJSON, Parquet, NetCDF, CSV).

---

## 4. Geospatial Map Architecture

Map rendering utilizes hardware-accelerated WebGL vector tiles:
- **Base Tiles**: Minimalist dark basemap emphasizing operational clarity over decorative labels.
- **Layer 1 (Sensors)**: Clustered GeoJSON circle markers colored dynamically by AQI severity.
- **Layer 2 (Plume Predictions)**: Interpolated raster/contour layers showing predicted atmospheric dispersion.
- **Layer 3 (Citizen Incidents)**: Pulsing threat indicators for high-confidence unverified events.
- **Layer 4 (Sensitive Receptors)**: Polygon buffers surrounding schools, daycares, and hospitals.
