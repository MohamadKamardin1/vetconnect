from django.urls import path
from community.api.views import MyPostDetailView, MyPostListCreateView, PublicPostListView, ReportCreateView, ReportListView, ReportModerationView, UserBlockCreateView, UserBlockListView

urlpatterns = [
    path("posts/", PublicPostListView.as_view(), name="public-post-list"),
    path("my-posts/", MyPostListCreateView.as_view(), name="my-post-list-create"),
    path("my-posts/<uuid:pk>/", MyPostDetailView.as_view(), name="my-post-detail"),
    path("reports/", ReportCreateView.as_view(), name="report-create"),
    path("reports/admin/", ReportListView.as_view(), name="report-admin-list"),
    path("reports/<uuid:pk>/moderate/", ReportModerationView.as_view(), name="report-moderate"),
    path("blocks/", UserBlockListView.as_view(), name="block-list"),
    path("blocks/create/", UserBlockCreateView.as_view(), name="block-create"),
]
