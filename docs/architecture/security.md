# Security & Privacy Architecture Specification

## 1. Authentication & Role-Based Access Control (RBAC)

ClimaX implements a multi-tier authorization hierarchy separating public citizen actions from statutory municipal enforcement:

| Role | Permissions & Access Scope |
| :--- | :--- |
| **Anonymous Citizen** | View public AQI map; submit unauthenticated pollution reports; query citizen assistant. |
| **Registered Citizen** | View personal submission history; subscribe to localized geofenced SMS/Push notifications. |
| **Field Officer** | View assigned incidents; record certified ground-truth verifications; upload inspection photos. |
| **Municipal Authority** | Full command center access; incident triage; dispatch enforcement teams; issue citywide advisories. |
| **Environmental Researcher** | Query BigQuery data warehouse; execute bulk historical exports; access raw anonymized sensor feeds. |
| **System Administrator** | User provisioning; secret rotation; model endpoint configuration; audit log inspection. |

---

## 2. Citizen Privacy & Location Obfuscation

1. **Dual-Coordinate Storage**:
   - **Internal Coordinate** (`geom`): Exact physical coordinate stored in encrypted database partitions accessible exclusively to certified enforcement officers for physical site visits.
   - **Public Coordinate** (`obfuscated_geom`): Randomly jittered coordinate within a 200m radius circle published to public citizen maps and external APIs to protect whistleblower and resident anonymity.
2. **Media Sanitization Pipeline**:
   - Ingested citizen photos are stripped of EXIF metadata (camera serial, precise GPS, device model) before public availability.
   - Automated Computer Vision redaction blurs detected human faces and vehicle license plates.

---

## 3. AI Safety, Input Validation & Prompt Injection Defense

1. **System Prompt Hardening**:
   - The Gemini AI Copilot system instructions are strictly fenced with immutable system boundaries preventing jailbreaking or arbitrary code execution.
2. **Strict Schema Output Validation**:
   - Model responses are constrained to Pydantic schemas via structured JSON mode. Any un-parseable output or instruction violation is rejected before reaching the UI.
3. **Citizen Text Sanitization**:
   - Citizen descriptions are sanitized using multi-language profanity and injection filters before passing into LLM reasoning contexts.

---

## 4. Operational API Protection & Secret Management

- **Zero Secret Commits**: All keys and credentials reside in Google Cloud Secret Manager and are injected as environment variables into Cloud Run containers.
- **Rate Limiting**: Public submission endpoints are protected with sliding-window IP and device fingerprint rate limiting (max 10 submissions per hour per IP) to prevent spam attacks.
- **End-to-End Encryption**: Enforced TLS 1.3 in transit; AES-256 encryption at rest across PostgreSQL, BigQuery, and Google Cloud Storage.
