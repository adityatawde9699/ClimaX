# Trust & Explainability Architecture

## 1. The 4-Tier Environmental Information Taxonomy

Environmental intelligence platforms frequently suffer from public distrust when black-box AI predictions are confused with ground reality. ClimaX establishes an uncompromising architectural standard: **every piece of data displayed across the platform belongs to exactly one of four distinct information tiers**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. OBSERVED DATA                                                            │
│    Direct physical measurements or unmodified citizen multimedia.           │
│    • Sensor PM2.5 = 186.4 µg/m³                                             │
│    • Wind speed = 14.2 km/h (WNW 290°)                                      │
│    • Citizen uploaded JPEG image with EXIF coordinate                       │
│    • Sentinel-5P Level-2 tropospheric NO2 column density                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. AI INFERENCE                                                             │
│    Probabilistic interpretations deduced by machine learning models.        │
│    • "Possible industrial emission plume — 81% confidence"                  │
│    • Ringelmann Smoke Opacity Grade 3.5 detected in visual bounding box     │
│    • Must cite contributing sensors and meteorological evidence             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. PREDICTION                                                               │
│    Forward-looking projections of future environmental state.               │
│    • "Predicted AQI at Anand Vihar in 6 hours: 191 (Unhealthy for Sensitive)│
│    • Gaussian plume dispersion envelope extending 3.5 km southeast          │
│    • Accompanied by confidence intervals [175 - 208]                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. HUMAN VERIFICATION                                                       │
│    Certified ground truth recorded by accredited municipal field officers.  │
│    • "Industrial emission verified by field officer Rajesh Sharma (ID: 412)"│
│    • Official cease-and-desist notice served to boiler #2                   │
│    • High-resolution ground inspection photographs attached                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Standardized AI Response Envelope Contract

Every AI model inference (Gemini Multimodal, Environmental Reasoning, Vertex AI Plume Predictor) must serialize into the canonical `AIExplanationSchema`:

```typescript
export interface AIExplanationMetadata {
  /** The core summary finding */
  result: string;
  
  /** Normalized score between 0.00 and 1.00 */
  confidence: number;
  
  /** Confidence categorization bracket */
  confidence_tier: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  
  /** Human-readable list of physical, visual, or sensor observations */
  evidence: string[];
  
  /** Traceable data lineage (URIs, sensor IDs, dataset references) */
  data_sources: string[];
  
  /** Explicit model version identifier */
  model: string;
  
  /** Inference timestamp */
  timestamp: string;
  
  /** Human review state */
  verification_status: 'UNVERIFIED' | 'FIELD_VERIFIED' | 'REJECTED' | 'DISPUTED';
}
```

---

## 3. UI Representation Guidelines

1. **Information Tier Badges**:
   - `OBSERVED`: Dark Emerald badge (`bg-emerald-950 text-emerald-300 border-emerald-700`)
   - `INFERRED`: Dark Indigo badge (`bg-indigo-950 text-indigo-300 border-indigo-700`)
   - `PREDICTED`: Dark Cyan badge (`bg-cyan-950 text-cyan-300 border-cyan-700`)
   - `VERIFIED`: High-contrast Blue badge (`bg-blue-950 text-blue-200 border-blue-600`)
2. **Mandatory Evidence Drawers**:
   - Any UI element displaying an AI inference or prediction must offer a 1-click inspection drawer presenting the full `evidence` array, `data_sources`, and `model` version.
   - Predictions must display confidence intervals rather than deceptive single-number pseudo-certainties.
