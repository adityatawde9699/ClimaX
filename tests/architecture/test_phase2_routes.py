from main import app


def test_required_user_and_report_routes_are_registered():
    paths = app.openapi()["paths"]
    assert "post" in paths["/api/v1/users/"]
    assert {"get", "patch"}.issubset(paths["/api/v1/users/{user_id}"])
    assert "get" in paths["/api/v1/reports/{report_id}"]


def test_user_write_routes_require_bearer_authentication():
    paths = app.openapi()["paths"]
    assert paths["/api/v1/users/"]["post"]["security"] == [{"HTTPBearer": []}]
    assert paths["/api/v1/users/{user_id}"]["patch"]["security"] == [{"HTTPBearer": []}]
