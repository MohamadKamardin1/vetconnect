import pytest
from rest_framework.test import APIClient
from accounts.models import User
from feed.models import FeedRule, FeedCalculation


@pytest.mark.django_db
def test_feed_missing_rule_is_explicit_and_history_is_isolated():
    user = User.objects.create_user(email="feed@example.com", password="StrongPass123!")
    client = APIClient(); client.force_authenticate(user=user)
    response = client.post("/api/v1/feed/calculations/", {"species_code": "cattle", "production_category": "dairy", "inputs": {"animal_count": 2, "average_weight_kg": 400, "feed_type": "hay"}}, format="json")
    assert response.status_code == 201
    assert response.data["status"] == "MISSING_CONFIGURATION"
    assert FeedCalculation.objects.filter(requested_by=user).count() == 1


@pytest.mark.django_db
def test_feed_configured_rule_is_deterministic():
    user = User.objects.create_user(email="feed2@example.com", password="StrongPass123!")
    FeedRule.objects.create(species_code="cattle", production_category="dairy", formula_key="body_weight_ratio", assumptions={"daily_ratio": "0.02"})
    client = APIClient(); client.force_authenticate(user=user)
    response = client.post("/api/v1/feed/calculations/", {"species_code": "cattle", "production_category": "dairy", "inputs": {"animal_count": 2, "average_weight_kg": 400, "feed_type": "hay"}}, format="json")
    assert response.status_code == 201
    assert response.data["result"]["daily_feed_kg"] == "16.000"
