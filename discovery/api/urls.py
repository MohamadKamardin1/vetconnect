from django.urls import path
from discovery.api.views import PublicReviewListView, PublicServiceListView, ReviewCreateView, ReviewModerationView

urlpatterns = [
    path("services/", PublicServiceListView.as_view(), name="service-list"),
    path("reviews/", PublicReviewListView.as_view(), name="review-list"),
    path("reviews/create/", ReviewCreateView.as_view(), name="review-create"),
    path("reviews/<uuid:pk>/moderate/", ReviewModerationView.as_view(), name="review-moderate"),
]
