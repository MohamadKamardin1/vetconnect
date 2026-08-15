import pytest
from rest_framework.test import APIClient
from accounts.models import User
from disease.models import DiseaseRule


@pytest.mark.django_db
def test_disease_requires_complete_intake():
    user = User.objects.create_user(email="disease@example.com", password="StrongPass123!")
    client = APIClient(); client.force_authenticate(user=user)
    response = client.post("/api/v1/disease/assessments/", {"species_code": "cattle", "inputs": {"symptoms": ["cough"]}}, format="json")
    assert response.status_code == 201
    assert response.data["status"] == "INVALID"
    assert "missing_inputs" in response.data["output"]


@pytest.mark.django_db
def test_disease_high_risk_escalates_and_disclaims():
    user = User.objects.create_user(email="disease2@example.com", password="StrongPass123!")
    DiseaseRule.objects.create(species_code="cattle", symptom_weights={"cough": {"respiratory_condition": 2}}, high_risk_symptoms=["collapse"], disclaimer="Decision support only; not a definitive diagnosis.")
    client = APIClient(); client.force_authenticate(user=user)
    payload = {"species_code": "cattle", "inputs": {"age": 4, "location": "Arusha", "symptoms": ["cough", "collapse"], "onset_days": 1, "severity": "SEVERE", "vaccination": "unknown", "exposure": "unknown"}}
    response = client.post("/api/v1/disease/assessments/", payload, format="json")
    assert response.status_code == 201
    assert response.data["output"]["urgency"] == "EMERGENCY"
    assert response.data["output"]["referral_required"] is True
    assert "not a definitive diagnosis" in response.data["output"]["disclaimer"]
