from django.urls import path
from audit.api.views import AuditLogEntryDetailView, AuditLogEntryListView

urlpatterns = [
    path("logs/", AuditLogEntryListView.as_view(), name="audit-log-list"),
    path("logs/<uuid:pk>/", AuditLogEntryDetailView.as_view(), name="audit-log-detail"),
]
