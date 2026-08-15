from rest_framework import serializers


class KYCActionSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=["VERIFIED", "REJECTED", "SUSPENDED"])
    reason_code = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(read_only=True)
