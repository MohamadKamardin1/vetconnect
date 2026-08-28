import pytest
from django.core.cache import cache
from django.test import Client, RequestFactory
from rest_framework.test import APIClient
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from accounts.models import User
from core.api.schema import add_common_error_responses
from core.views import error_400, error_403, error_404, error_500


@pytest.mark.django_db
def test_health_endpoint_is_public_and_machine_readable():
    response = Client().get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.django_db
def test_readiness_reports_database_health():
    response = Client().get("/readiness/")
    assert response.status_code == 200
    assert response.json()["checks"]["database"] == "ok"


def test_api_validation_uses_standard_error_envelope():
    client = APIClient()
    response = client.get("/api/v1/schema/does-not-exist/")
    assert response.status_code == 404
    assert "error" in response.json()
    assert "message" in response.json()["error"]


def test_html_404_contains_no_internal_details():
    response = Client().get("/definitely-not-a-real-route/")
    assert response.status_code == 404
    body = response.content.decode()
    assert "Page not found" in body
    assert "Traceback" not in body
    assert "/home/ubuntu" not in body


@pytest.mark.parametrize("handler,expected_status", [(error_400, 400), (error_403, 403), (error_404, 404)])
def test_every_html_error_handler_hides_internal_details(handler, expected_status):
    request = RequestFactory().get("/not-an-api-route/")
    response = handler(request)
    assert response.status_code == expected_status
    body = response.content.decode()
    assert "Traceback" not in body
    assert "/home/" not in body
    assert "SECRET_KEY" not in body


def test_html_500_handler_hides_internal_details():
    request = RequestFactory().get("/not-an-api-route/")
    response = error_500(request)
    assert response.status_code == 500
    body = response.content.decode()
    assert "Traceback" not in body
    assert "SECRET_KEY" not in body


@pytest.mark.parametrize("handler,expected_status,expected_code", [(error_400, 400, "bad_request"), (error_403, 403, "permission_denied"), (error_404, 404, "not_found")])
def test_every_api_error_handler_uses_standard_envelope(handler, expected_status, expected_code):
    request = RequestFactory().get("/api/v1/not-a-real-endpoint/")
    response = handler(request)
    assert response.status_code == expected_status
    payload = response.json() if hasattr(response, "json") else __import__("json").loads(response.content)
    assert payload["error"]["code"] == expected_code
    assert "message" in payload["error"]


def test_api_500_handler_uses_standard_envelope():
    request = RequestFactory().get("/api/v1/not-a-real-endpoint/")
    response = error_500(request)
    assert response.status_code == 500
    payload = response.json() if hasattr(response, "json") else __import__("json").loads(response.content)
    assert payload["error"]["code"] == "internal_error"


@pytest.mark.django_db
def test_unauthenticated_request_returns_standard_envelope():
    client = APIClient()
    response = client.get("/api/v1/audit/logs/")
    assert response.status_code == 401
    assert response.json()["error"]["message"]


@pytest.mark.django_db
def test_wrong_role_request_returns_standard_envelope():
    user = User.objects.create_user(email="foundation-ordinary@example.com", password="StrongPass123!")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/v1/audit/logs/")
    assert response.status_code == 403
    assert response.json()["error"]["message"]


@pytest.mark.django_db
def test_method_not_allowed_returns_standard_envelope():
    admin = User.objects.create_superuser(email="foundation-admin@example.com", password="StrongPass123!")
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.delete("/api/v1/audit/logs/")
    assert response.status_code == 405
    assert response.json()["error"]["code"] == "method_not_allowed"


@pytest.mark.django_db
def test_throttled_request_returns_standard_envelope():
    """
    DRF's SimpleRateThrottle binds THROTTLE_RATES from api_settings once at class-definition time,
    so override_settings(REST_FRAMEWORK=...) alone does not reach already-imported throttle classes.
    Patch AnonRateThrottle/UserRateThrottle's `rate` directly instead, which is the standard way to
    force a specific rate in a DRF test, and restore it afterward so no other test is affected.
    """
    cache.clear()
    original_anon_rate = getattr(AnonRateThrottle, "rate", None)
    original_user_rate = getattr(UserRateThrottle, "rate", None)
    AnonRateThrottle.rate = "1/day"
    UserRateThrottle.rate = "1/day"
    try:
        client = APIClient()
        first = client.post("/api/v1/auth/register/", {}, format="json")
        second = client.post("/api/v1/auth/register/", {}, format="json")
    finally:
        AnonRateThrottle.rate = original_anon_rate
        UserRateThrottle.rate = original_user_rate
        cache.clear()
    assert first.status_code != 429
    assert second.status_code == 429
    assert second.json()["error"]["code"] == "throttled"


def test_error_response_postprocessing_hook_only_fills_missing_status_codes():
    result = {
        "paths": {
            "/api/v1/example/": {
                "get": {"responses": {"200": {"description": "ok"}, "404": {"description": "custom not found"}}},
                "parameters": [{"name": "page", "in": "query"}],
            }
        }
    }
    processed = add_common_error_responses(result, generator=None, request=None, public=True)
    responses = processed["paths"]["/api/v1/example/"]["get"]["responses"]
    assert responses["200"] == {"description": "ok"}
    assert responses["404"] == {"description": "custom not found"}
    assert set(["400", "401", "403", "429", "500"]).issubset(responses.keys())
    assert responses["400"]["content"]["application/json"]["schema"] == {"$ref": "#/components/schemas/ErrorEnvelope"}
    assert "ErrorEnvelope" in processed["components"]["schemas"]
    assert processed["paths"]["/api/v1/example/"]["parameters"] == [{"name": "page", "in": "query"}]
