from rest_framework import generics
from audit.api.serializers import AuditLogEntrySerializer
from audit.models import AuditLogEntry
from accounts.permissions import IsAdministrator


class AuditLogEntryListView(generics.ListAPIView):
    """Administrator-only, read-only audit trail. Entries are never created, edited, or deleted through this API."""

    permission_classes = [IsAdministrator]
    serializer_class = AuditLogEntrySerializer
    queryset = AuditLogEntry.objects.select_related("actor").all()
    filterset_fields = ["action", "target_type", "actor"]


class AuditLogEntryDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = AuditLogEntrySerializer
    queryset = AuditLogEntry.objects.select_related("actor").all()
