from rest_framework import serializers


class ReportModerationSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["REVIEWED", "DISMISSED"])
