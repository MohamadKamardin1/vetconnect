import uuid
import pytest
from rest_framework.test import APIClient
from accounts.models import User
from messaging.models import Conversation, ConversationParticipant, Message, WebhookEndpoint


@pytest.mark.django_db
def test_conversation_isolation_and_idempotent_messages():
    alice = User.objects.create_user(email="alice@example.com", password="StrongPass123!", first_name="Alice")
    bob = User.objects.create_user(email="bob@example.com", password="StrongPass123!", first_name="Bob")
    mallory = User.objects.create_user(email="mallory@example.com", password="StrongPass123!", first_name="Mallory")
    conversation = Conversation.objects.create(created_by=alice, subject="Animal case")
    ConversationParticipant.objects.create(conversation=conversation, user=alice)
    ConversationParticipant.objects.create(conversation=conversation, user=bob)

    client = APIClient()
    client.force_authenticate(user=mallory)
    response = client.get(f"/api/v1/messaging/conversations/{conversation.pk}/")
    assert response.status_code == 404

    client.force_authenticate(user=alice)
    payload = {"body": "Please review the record.", "client_message_id": "client-1"}
    first = client.post(f"/api/v1/messaging/conversations/{conversation.pk}/messages/", payload, format="json")
    second = client.post(f"/api/v1/messaging/conversations/{conversation.pk}/messages/", payload, format="json")
    assert first.status_code == 201
    assert second.status_code == 200
    assert Message.objects.filter(conversation=conversation, sender=alice, client_message_id="client-1").count() == 1


@pytest.mark.django_db
def test_webhook_secret_is_not_returned_and_is_hashed():
    user = User.objects.create_user(email="owner@example.com", password="StrongPass123!")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post("/api/v1/messaging/webhooks/", {"url": "https://example.com/hook", "secret": "a" * 40}, format="json")
    assert response.status_code == 201
    assert response.data["secret"] == "stored-as-hash"
    endpoint = WebhookEndpoint.objects.get(owner=user)
    assert endpoint.secret_hash != "a" * 40
