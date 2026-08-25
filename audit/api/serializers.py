from rest_framework import serializers
from audit.models import AuditLogEntry


class AuditLogEntrySerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(source="actor.email", read_only=True, default="")

    class Meta:
        model = AuditLogEntry
        fields = ["id", "actor", "actor_email", "action", "target_type", "target_id", "before", "after", "reason", "request_id", "created_at"]
        read_only_fields = fields
