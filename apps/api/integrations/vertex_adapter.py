from core.config import settings


class VertexAdapter:
    async def query_plume_prediction(self, features: dict) -> dict:
        if not settings.VERTEX_AI_ENDPOINT_POLLUTION_PREDICTION:
            raise RuntimeError("Vertex prediction endpoint is not configured")
        try:
            from google.cloud import aiplatform
        except ImportError as exc:
            raise RuntimeError("google-cloud-aiplatform must be installed") from exc
        endpoint = aiplatform.Endpoint(settings.VERTEX_AI_ENDPOINT_POLLUTION_PREDICTION)
        response = endpoint.predict(instances=[features], timeout=60)
        return response.predictions[0]
