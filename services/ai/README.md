# AI Domain Service (`services/ai`)

Responsible for all Google Gemini API, Google AI Studio, and multimodal reasoning tasks.

## Responsibilities:
- **Citizen Report Multimodal Vision**: Ingests citizen uploaded photos and video clips, running them through Gemini 1.5 Pro / Flash to detect smoke plumes, industrial chimneys, garbage incineration, and particulate haze.
- **Explainable Evidence Extraction**: Formulates visual bounding box coordinates and textual evidence justifications conforming to `AIExplanationMetadata`.
- **Environmental Reasoning Pipeline**: Correlates localized meteorological vectors (wind speed, direction) and stationary sensor spikes to attribute likely pollution emitters.
- **Municipal AI Copilot**: Grounded conversational assistant enabling municipal commissioners to ask questions in plain language (e.g. "What caused the AQI spike in North Ward between 2 AM and 5 AM?").

## Planned Implementation Phase:
- Phase 5 (Gemini Multimodal Analysis) & Phase 10 (AI Copilot).
