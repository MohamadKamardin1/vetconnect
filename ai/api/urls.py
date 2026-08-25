from django.urls import path
from ai.api.views import AIDiseaseAssistView, AIFeedAssistView, AIInteractionListView

urlpatterns = [
    path("disease-assist/", AIDiseaseAssistView.as_view(), name="ai-disease-assist"),
    path("feed-assist/", AIFeedAssistView.as_view(), name="ai-feed-assist"),
    path("interactions/", AIInteractionListView.as_view(), name="ai-interaction-list"),
]
