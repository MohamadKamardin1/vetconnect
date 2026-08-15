from rest_framework import serializers
from notifications.models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "event_key", "template_key", "title", "body", "payload", "channel", "status", "sent_at", "created_at"]
        read_only_fields = fields


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ["locale", "timezone", "enabled_channels", "quiet_hours_start", "quiet_hours_end", "marketing_enabled", "clinical_enabled", "updated_at"]
        read_only_fields = ["updated_at"]
