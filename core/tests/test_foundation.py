import pytest
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError


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
