import pytest
from rest_framework.test import APIClient
from accounts.models import User
from animals.models import Animal, AnimalSpecies
from privacy.models import DataDeletionRequest, DataExportRequest


def _client(email):
    user = User.objects.create_user(email=email, password="StrongPass123!")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
def test_data_export_includes_only_own_records():
    client_a, user_a = _client("privacy-a@example.com")
    _client_b, user_b = _client("privacy-b@example.com")
    Animal.objects.create(owner=user_a, name="Bella", species=AnimalSpecies.CATTLE)
    Animal.objects.create(owner=user_b, name="NotYours", species=AnimalSpecies.CATTLE)

    response = client_a.post("/api/v1/privacy/export/", {}, format="json")
    assert response.status_code == 201
    assert response.data["status"] == "COMPLETED"
    animal_names = [a["name"] for a in response.data["payload"]["animals"]]
    assert animal_names == ["Bella"]
    assert response.data["payload"]["profile"]["email"] == user_a.email


@pytest.mark.django_db
def test_data_export_list_is_user_scoped():
    client_a, user_a = _client("privacy-c@example.com")
    client_b, _user_b = _client("privacy-d@example.com")
    DataExportRequest.objects.create(user=user_a)

    response = client_b.get("/api/v1/privacy/export/")
    assert response.data["count"] == 0
    response = client_a.get("/api/v1/privacy/export/")
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_deletion_requires_explicit_confirm_step():
    client, user = _client("privacy-e@example.com")

    confirm_without_request = client.post("/api/v1/privacy/deletion/confirm/", {}, format="json")
    assert confirm_without_request.status_code == 400

    create_response = client.post("/api/v1/privacy/deletion/", {"reason": "no longer needed"}, format="json")
    assert create_response.status_code == 201
    assert create_response.data["status"] == "PENDING"
    user.refresh_from_db()
    assert user.is_active is True  # nothing destructive happens until confirm

    confirm_response = client.post("/api/v1/privacy/deletion/confirm/", {}, format="json")
    assert confirm_response.status_code == 200
    assert confirm_response.data["status"] == "COMPLETED"
    user.refresh_from_db()
    assert user.is_active is False
    assert user.email.startswith("deleted+")


@pytest.mark.django_db
def test_deletion_request_is_user_scoped_and_requires_auth():
    anon_client = APIClient()
    response = anon_client.post("/api/v1/privacy/deletion/", {}, format="json")
    assert response.status_code == 401

    client_a, user_a = _client("privacy-f@example.com")
    client_b, _user_b = _client("privacy-g@example.com")
    DataDeletionRequest.objects.create(user=user_a)

    response = client_b.get("/api/v1/privacy/deletion/")
    assert response.data["count"] == 0
