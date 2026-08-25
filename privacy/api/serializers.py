from rest_framework import serializers
from privacy.models import DataDeletionRequest, DataExportRequest


class DataExportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataExportRequest
        fields = ["id", "status", "payload", "requested_at", "completed_at"]
        read_only_fields = fields


class DataDeletionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataDeletionRequest
        fields = ["id", "status", "reason", "requested_at", "completed_at"]
        read_only_fields = ["id", "status", "requested_at", "completed_at"]


class DataDeletionRequestCreateSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True, default="")
