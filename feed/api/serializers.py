from rest_framework import serializers
from feed.models import FeedCalculation


class FeedCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedCalculation
        fields = ["id", "inputs", "result", "status", "rule", "created_at"]
        read_only_fields = ["id", "result", "status", "rule", "created_at"]


class FeedCalculationRequestSerializer(serializers.Serializer):
    species_code = serializers.CharField(max_length=40)
    production_category = serializers.CharField(max_length=80)
    inputs = serializers.DictField()
