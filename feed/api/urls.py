from django.urls import path
from feed.api.views import FeedCalculationListCreateView

urlpatterns = [path("calculations/", FeedCalculationListCreateView.as_view(), name="feed-calculation-list-create")]
