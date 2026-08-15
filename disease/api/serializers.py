from rest_framework import serializers
from disease.models import DiseaseAssessment


class DiseaseAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseAssessment
        fields = ["id", "inputs", "output", "status", "rule", "created_at"]
        read_only_fields = ["id", "output", "status", "rule", "created_at"]


class DiseaseAssessmentRequestSerializer(serializers.Serializer):
    species_code = serializers.CharField(max_length=40)
    inputs = serializers.DictField()
