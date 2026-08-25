from django.urls import path
from privacy.api.views import DataDeletionConfirmView, DataDeletionRequestListCreateView, DataExportRequestListCreateView

urlpatterns = [
    path("export/", DataExportRequestListCreateView.as_view(), name="privacy-export"),
    path("deletion/", DataDeletionRequestListCreateView.as_view(), name="privacy-deletion"),
    path("deletion/confirm/", DataDeletionConfirmView.as_view(), name="privacy-deletion-confirm"),
]
