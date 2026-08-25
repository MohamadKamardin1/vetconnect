from rest_framework import serializers
from ai.models import AIInteraction


class AIDiseaseAssistRequestSerializer(serializers.Serializer):
    species_code = serializers.CharField(max_length=40)
    inputs = serializers.DictField()


class AIFeedAssistRequestSerializer(serializers.Serializer):
    species_code = serializers.CharField(max_length=40)
    production_category = serializers.CharField(max_length=80)
    inputs = serializers.DictField()


class AIInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInteraction
        fields = ["id", "feature_key", "provider_key", "model_version", "redacted_input", "output", "status", "latency_ms", "human_review_status", "created_at"]
        read_only_fields = fields
