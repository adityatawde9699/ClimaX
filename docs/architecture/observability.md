# Observability & Telemetry Architecture Specification

## 1. Architectural Strategy

ClimaX operates in mission-critical environmental governance contexts where unobserved pipeline failures or AI hallucination can compromise public health responses. Observability is architected across four distinct pillars:

```
┌───────────────────────────┬───────────────────────────┐
│ 1. API & SYSTEM HEALTH    │ 2. DATA PIPELINE HEALTH   │
│ • Cloud Run CPU/Memory    │ • IoT Ingest Latency      │
│ • Endpoint p95 Latency    │ • Dead-letter Pub/Sub DLQ │
│ • 4xx/5xx Error Rates     │ • Stuck Sensor Detection  │
├───────────────────────────┼───────────────────────────┤
│ 3. AI & MODEL GOVERNANCE  │ 4. OPERATIONAL OUTCOMES   │
│ • Gemini Token Ledger     │ • Incident Triage Time    │
│ • Vision Inference Latency│ • Alert Delivery Rate     │
│ • Prediction Drift (RMSE) │ • Intervention Delta AQI  │
└───────────────────────────┴───────────────────────────┘
```

---

## 2. Structured Logging Standards

All application logs are emitted as structured JSON to `stdout`, automatically indexed by Google Cloud Logging:
```json
{
  "time": "2026-09-08T16:30:00.124Z",
  "level": "INFO",
  "name": "climax.ai.multimodal",
  "message": "Processed citizen report media through Gemini 1.5",
  "report_id": "rep-4c28f11a",
  "model": "gemini-1.5-pro",
  "latency_ms": 1420.5,
  "confidence": 0.88,
  "token_count": { "prompt": 1240, "completion": 185 }
}
```

---

## 3. Dedicated AI Cost & Latency Ledger

To prevent unanticipated billing spikes during widespread pollution crises:
1. **Per-Invocation Token Counter**: Tracks prompt and completion tokens for every Gemini 1.5 Pro and Flash invocation.
2. **Quota Throttling**: Automatically cascades requests from Gemini 1.5 Pro to Gemini 1.5 Flash if hourly token budgets exceed predefined municipal safety ceilings.
3. **Model Drift Monitoring**: Compares 24-hour ahead AQI predictions against realized sensor ground truth daily, recording Root Mean Square Error (RMSE) and Mean Absolute Error (MAE) into BigQuery metrics tables.
