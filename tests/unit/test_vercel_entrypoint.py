"""The repository-root entrypoint must expose the same local FastAPI app."""

from main import app as local_app

from app import app as vercel_app


def test_vercel_entrypoint_exports_existing_app():
    assert vercel_app is local_app
    assert any(route.path == "/health" for route in vercel_app.routes)
