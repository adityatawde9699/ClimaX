"""Small GCS adapter with lazy cloud imports for local development."""

from datetime import timedelta

import httpx

from core.config import settings


class GCSAdapter:
    def _client(self):
        try:
            from google.cloud import storage
        except ImportError as exc:
            raise RuntimeError("google-cloud-storage must be installed to use GCS") from exc
        return storage.Client(project=settings.GCP_PROJECT_ID)

    def generate_signed_upload_url(self, file_path: str, content_type: str) -> str:
        blob = self._client().bucket(settings.GCS_BUCKET).blob(file_path)
        return blob.generate_signed_url(
            version="v4", expiration=timedelta(minutes=15), method="PUT", content_type=content_type
        )

    def download_bytes(self, gcs_uri: str) -> bytes:
        if gcs_uri.startswith(("http://", "https://")):
            response = httpx.get(gcs_uri, timeout=15.0)
            response.raise_for_status()
            return response.content
        if not gcs_uri.startswith("gs://"):
            raise ValueError("Expected a gs:// URI")
        bucket_name, blob_name = gcs_uri[5:].split("/", 1)
        return self._client().bucket(bucket_name).blob(blob_name).download_as_bytes()
