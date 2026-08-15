from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from accounts.models import User
from messaging.models import Conversation, ConversationParticipant, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.display_name", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "sender_name", "body", "client_message_id", "created_at", "edited_at"]
        read_only_fields = ["id", "conversation", "sender", "sender_name", "created_at", "edited_at"]

    def validate_client_message_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("client_message_id is required for idempotent message submission.")
        return value.strip()


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "subject", "created_by", "participants", "last_message", "created_at", "updated_at"]
        read_only_fields = fields

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_participants(self, obj):
        return [{"id": str(p.user_id), "display_name": p.user.display_name} for p in obj.participants.select_related("user").all()]

    @extend_schema_field(MessageSerializer(allow_null=True))
    def get_last_message(self, obj):
        message = obj.messages.select_related("sender").order_by("-created_at").first()
        return MessageSerializer(message).data if message else None


class ConversationCreateSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=180, required=False, allow_blank=True)
    participant_ids = serializers.ListField(child=serializers.UUIDField(), min_length=1, max_length=20)

    def validate_participant_ids(self, value):
        request = self.context["request"]
        ids = set(value)
        ids.add(request.user.pk)
        existing = set(User.objects.filter(pk__in=ids, is_active=True).values_list("pk", flat=True))
        if existing != ids:
            raise serializers.ValidationError("Every participant must be an active user.")
        return list(ids)


class WebhookEndpointSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=500)
    secret = serializers.CharField(min_length=32, max_length=200, write_only=True)
