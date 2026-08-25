import pytest
from rest_framework.test import APIClient
from accounts.models import User
from ai.models import AIFeatureConfig, AIInteraction, AIProviderConfig, HumanReviewStatus
from disease.models import DiseaseRule
from feed.models import FeedRule


def _client(email):
    user = User.objects.create_user(email=email, password="StrongPass123!")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
def test_disease_assist_suppressed_when_feature_disabled():
    client, _user = _client("ai1@example.com")
    DiseaseRule.objects.create(species_code="cattle", symptom_weights={"cough": {"respiratory_condition": 2}}, high_risk_symptoms=[], disclaimer="Decision support only.")
    payload = {"species_code": "cattle", "inputs": {"age": 4, "location": "Arusha", "symptoms": ["cough"], "onset_days": 1, "severity": "MILD", "vaccination": "unknown", "exposure": "unknown"}}
    response = client.post("/api/v1/ai/disease-assist/", payload, format="json")
    assert response.status_code == 200
    assert response.data["ai_status"] == "SUPPRESSED"
    assert response.data["ai_narrative"] is None
    assert response.data["possible_conditions"] is not None  # deterministic result always present
    interaction = AIInteraction.objects.get(user__email="ai1@example.com")
    assert interaction.status == "SUPPRESSED"
    assert "location" not in interaction.redacted_input  # never leaves the boundary: not allowlisted


@pytest.mark.django_db
def test_disease_assist_falls_back_when_no_provider_configured():
    client, _user = _client("ai2@example.com")
    DiseaseRule.objects.create(species_code="cattle", symptom_weights={"cough": {"respiratory_condition": 2}}, high_risk_symptoms=[], disclaimer="Decision support only.")
    AIFeatureConfig.objects.create(feature_key="DISEASE_ASSIST", is_enabled=True, allowed_context_fields=["species_code", "symptoms", "severity"])
    payload = {"species_code": "cattle", "inputs": {"age": 4, "location": "Arusha", "symptoms": ["cough"], "onset_days": 1, "severity": "MILD", "vaccination": "unknown", "exposure": "unknown"}}
    response = client.post("/api/v1/ai/disease-assist/", payload, format="json")
    assert response.status_code == 200
    assert response.data["ai_status"] == "FALLBACK"
    assert response.data["ai_narrative"] is None
    assert response.data["status"] == "COMPLETED"  # deterministic engine still fully answered
    interaction = AIInteraction.objects.get(user__email="ai2@example.com")
    assert interaction.status == "FALLBACK"
    assert set(interaction.redacted_input.keys()) <= {"species_code", "symptoms", "severity"}
    assert "location" not in interaction.redacted_input


@pytest.mark.django_db
def test_disease_assist_redacts_and_completes_with_console_provider():
    client, _user = _client("ai3@example.com")
    DiseaseRule.objects.create(species_code="cattle", symptom_weights={"cough": {"respiratory_condition": 2}}, high_risk_symptoms=[], disclaimer="Decision support only.")
    provider = AIProviderConfig.objects.create(provider_key="console", display_name="Console", model_name="offline-stub", model_version="v1", is_enabled=True)
    AIFeatureConfig.objects.create(feature_key="DISEASE_ASSIST", is_enabled=True, provider=provider, allowed_context_fields=["species_code", "symptoms", "severity"])
    payload = {"species_code": "cattle", "inputs": {"age": 4, "location": "Arusha, near the river", "symptoms": ["cough"], "onset_days": 1, "severity": "MILD", "vaccination": "unknown", "exposure": "unknown"}}
    response = client.post("/api/v1/ai/disease-assist/", payload, format="json")
    assert response.status_code == 200
    assert response.data["ai_status"] == "COMPLETED"
    assert response.data["ai_narrative"]
    assert "not a diagnosis" in response.data["disclaimer"]
    interaction = AIInteraction.objects.get(user__email="ai3@example.com")
    assert interaction.model_version == "v1"
    assert "location" not in interaction.redacted_input
    assert "Arusha" not in str(interaction.redacted_input)


@pytest.mark.django_db
def test_disease_assist_emergency_requires_human_review():
    client, _user = _client("ai4@example.com")
    DiseaseRule.objects.create(species_code="cattle", symptom_weights={"collapse": {"critical_condition": 5}}, high_risk_symptoms=["collapse"], disclaimer="Decision support only.")
    provider = AIProviderConfig.objects.create(provider_key="console", display_name="Console", model_name="offline-stub", model_version="v1", is_enabled=True)
    AIFeatureConfig.objects.create(feature_key="DISEASE_ASSIST", is_enabled=True, provider=provider, requires_human_review_on_urgent=True, allowed_context_fields=["species_code", "symptoms", "severity"])
    payload = {"species_code": "cattle", "inputs": {"age": 4, "location": "Arusha", "symptoms": ["collapse"], "onset_days": 1, "severity": "SEVERE", "vaccination": "unknown", "exposure": "unknown"}}
    response = client.post("/api/v1/ai/disease-assist/", payload, format="json")
    assert response.status_code == 200
    assert response.data["urgency"] == "EMERGENCY"
    assert response.data["human_review_status"] == HumanReviewStatus.PENDING
    interaction = AIInteraction.objects.get(user__email="ai4@example.com")
    assert interaction.human_review_status == HumanReviewStatus.PENDING


@pytest.mark.django_db
def test_feed_assist_never_alters_deterministic_calculation():
    client, _user = _client("ai5@example.com")
    FeedRule.objects.create(species_code="cattle", production_category="dairy", formula_key="body_weight_ratio", assumptions={"daily_ratio": "0.03"})
    provider = AIProviderConfig.objects.create(provider_key="console", display_name="Console", model_name="offline-stub", model_version="v1", is_enabled=True)
    AIFeatureConfig.objects.create(feature_key="FEED_ASSIST", is_enabled=True, provider=provider, allowed_context_fields=["species_code", "production_category", "feed_type"])
    payload = {"species_code": "cattle", "production_category": "dairy", "inputs": {"animal_count": 10, "average_weight_kg": 300, "feed_type": "silage"}}
    response = client.post("/api/v1/ai/feed-assist/", payload, format="json")
    assert response.status_code == 200
    assert response.data["status"] == "COMPLETED"
    assert response.data["daily_feed_kg"] == "90.000"
    assert response.data["ai_narrative"]


@pytest.mark.django_db
def test_ai_interactions_are_user_scoped():
    client_a, user_a = _client("ai6@example.com")
    client_b, _user_b = _client("ai7@example.com")
    AIInteraction.objects.create(user=user_a, feature_key="DISEASE_ASSIST", input_hash="x", status="SUPPRESSED")
    response = client_b.get("/api/v1/ai/interactions/")
    assert response.status_code == 200
    assert response.data["count"] == 0
    response = client_a.get("/api/v1/ai/interactions/")
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_disease_assist_requires_authentication():
    client = APIClient()
    response = client.post("/api/v1/ai/disease-assist/", {"species_code": "cattle", "inputs": {}}, format="json")
    assert response.status_code == 401
