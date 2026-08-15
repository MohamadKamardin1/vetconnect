from rest_framework import serializers


class ModerationActionSerializer(serializers.Serializer):
    moderation_status = serializers.ChoiceField(choices=["APPROVED", "REJECTED", "HIDDEN"])
    moderation_reason = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(read_only=True)
