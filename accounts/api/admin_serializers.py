from rest_framework import serializers


class AdminActionSerializer(serializers.Serializer):
    status = serializers.CharField(read_only=True)
