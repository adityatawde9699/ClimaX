# ClimaX User Roles & Personas

ClimaX bridges four distinct stakeholder groups into a unified collaborative platform:

---

## 1. Persona: The Concerned Citizen (Aarav, 34)

- **Context**: Parent of an asthmatic child living in an urban hotspot prone to industrial smoke and dust.
- **Pain Points**:
  - Legacy apps only show city-wide averages from a sensor 12 km away, masking acute hyper-local spikes.
  - Complaints sent to municipal hotlines vanish into administrative black holes with zero follow-up.
- **ClimaX Journey**:
  1. Opens mobile web app (`/citizen`) to check immediate neighborhood AQI and personalized mask/ventilation recommendations.
  2. Notices illegal open waste burning near a public park; taps "Report Pollution", takes a photo with GPS auto-tagged.
  3. Receives instant feedback: Gemini AI categorizes "Biomass Burning (86% confidence)" and indicates municipal triage status.
  4. Receives a push notification 90 minutes later: *"Municipal field team dispatched and fire extinguished."*

---

## 2. Persona: The Municipal Command Officer (Sunita, 42)

- **Context**: Assistant Commissioner of Environment overseeing urban pollution emergency response.
- **Pain Points**:
  - Overwhelmed with thousands of unverified social media complaints containing vague locations and no evidence.
  - Reactive field teams arrive hours after smoke has already dissipated.
- **ClimaX Journey**:
  1. Monitors Command Center dashboard (`/command-center`) displaying live sensor heatmaps and incoming AI-triaged reports.
  2. Inspects a high-priority incident: Gemini has flagged an industrial chimney with Ringelmann Opacity 3.5 corroborated by a downwind sensor spike.
  3. Queries the AI Copilot: *"Identify nearby inspection units available within 15 minutes."*
  4. Dispatches the field officer with 1 tap, serving an immediate inspection notice.
  5. Reviews the Before/After impact card showing a 45 µg/m³ PM2.5 reduction within 3 hours of operation halt.

---

## 3. Persona: The Climate Researcher (Dr. Elena, 38)

- **Context**: Postdoctoral atmospheric scientist investigating aerosol dispersion and health correlations.
- **Pain Points**:
  - Frustrated by proprietary data silos, missing metadata, and lack of ground-truth validation.
- **ClimaX Journey**:
  1. Logs into Researcher Data Explorer (`/data-explorer`).
  2. Queries BigQuery directly across 2 years of continuous sensor telemetry, satellite NO2 rasters, and verified incidents.
  3. Evaluates the efficacy of seasonal anti-smog gun deployments across wards using exportable NetCDF / Parquet bundles.

---

## 4. Persona: The Platform Administrator (Dev, 29)

- **Context**: DevOps and data governance lead ensuring 99.9% uptime during peak pollution months.
- **Pain Points**:
  - Drifting low-cost sensor calibrations, runaway AI inference bills, and unauthorized access.
- **ClimaX Journey**:
  1. Accesses Admin Console (`/admin`) to monitor sensor heartbeat pings and stuck values.
  2. Audits Gemini token burn rates and latency distributions.
  3. Configures statutory alert thresholds and manages officer role permissions.
