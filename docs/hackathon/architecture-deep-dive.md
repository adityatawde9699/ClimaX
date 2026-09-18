# Architecture deep dive

ClimaX uses FastAPI, PostgreSQL/PostGIS, Pub/Sub workers, Gemini inference, Vertex AI forecasting, and a Next.js MapLibre command interface. Data carries an observed, inferred, predicted, or verified tier end-to-end. If the prediction provider is unavailable, the API returns an explicit service-unavailable response rather than synthetic output.
