from rest_framework import serializers
from animals.models import Animal, RecordAccessGrant, VeterinaryRecord


class AnimalSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.display_name", read_only=True)

    class Meta:
        model = Animal
        fields = ["id", "owner", "name", "species", "breed", "sex", "date_of_birth", "identification_code", "is_active", "created_at"]
        read_only_fields = ["id", "owner", "is_active", "created_at"]


class VeterinaryRecordSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.display_name", read_only=True)

    class Meta:
        model = VeterinaryRecord
        fields = ["id", "animal", "author", "clinic", "professional", "record_type", "title", "body", "occurred_at", "is_sensitive", "created_at"]
        read_only_fields = ["id", "author", "created_at"]


class RecordAccessGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordAccessGrant
        fields = ["id", "record", "granted_by", "grantee", "permission", "expires_at", "revoked_at", "created_at"]
        read_only_fields = ["id", "granted_by", "revoked_at", "created_at"]
