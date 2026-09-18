from main import app
from sqlalchemy.exc import SQLAlchemyError


def test_required_user_and_report_routes_are_registered():
    paths = app.openapi()["paths"]
    assert "post" in paths["/api/v1/users/"]
    assert {"get", "patch"}.issubset(paths["/api/v1/users/{user_id}"])
    assert "get" in paths["/api/v1/reports/{report_id}"]


def test_user_write_routes_require_bearer_authentication():
    paths = app.openapi()["paths"]
    assert paths["/api/v1/users/"]["post"]["security"] == [{"HTTPBearer": []}]
    assert paths["/api/v1/users/{user_id}"]["patch"]["security"] == [{"HTTPBearer": []}]


def test_phase_three_weather_route_is_registered():
    assert "get" in app.openapi()["paths"]["/api/v1/weather"]


def test_google_and_manual_login_routes_are_registered():
    paths = app.openapi()["paths"]
    assert "post" in paths["/api/v1/auth/login"]
    assert "post" in paths["/api/v1/auth/google"]


def test_database_failures_have_a_service_unavailable_handler():
    assert SQLAlchemyError in app.exception_handlers
    assert ConnectionRefusedError in app.exception_handlers
