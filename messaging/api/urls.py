from django.urls import path
from messaging.api.views import ConversationDetailView, ConversationListCreateView, MessageListCreateView, WebhookEndpointCreateView

urlpatterns = [
    path("conversations/", ConversationListCreateView.as_view(), name="conversation-list-create"),
    path("conversations/<uuid:pk>/", ConversationDetailView.as_view(), name="conversation-detail"),
    path("conversations/<uuid:conversation_id>/messages/", MessageListCreateView.as_view(), name="message-list-create"),
    path("webhooks/", WebhookEndpointCreateView.as_view(), name="webhook-create"),
]
