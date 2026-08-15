from django.utils import timezone
from rest_framework import serializers
from professionals.models import Clinic, ClinicStaff, CredentialDocument, ProfessionalProfile


class ProfessionalPublicSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source="user.display_name", read_only=True)
    region = serializers.CharField(source="region.name", read_only=True)
    district = serializers.CharField(source="district.name", read_only=True)
    is_verified_badge = serializers.SerializerMethodField()

    def get_is_verified_badge(self, obj) -> bool:
        if obj.verification_status != "VERIFIED" or not obj.is_active:
            return False
        return obj.badge_subscriptions.filter(status="ACTIVE", starts_at__lte=timezone.now(), ends_at__gt=timezone.now()).exists()

    class Meta:
        model = ProfessionalProfile
        fields = ["id", "display_name", "professional_type", "region", "district", "bio", "is_available", "verification_status", "is_verified_badge"]
        read_only_fields = fields


class ProfessionalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = ["professional_type", "registration_number", "issuing_body", "region", "district", "bio"]

    def create(self, validated_data):
        return ProfessionalProfile.objects.create(user=self.context["request"].user, **validated_data)


class ClinicSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.display_name", read_only=True)
    region_name = serializers.CharField(source="region.name", read_only=True)
    district_name = serializers.CharField(source="district.name", read_only=True)

    class Meta:
        model = Clinic
        fields = ["id", "name", "registration_number", "owner", "region", "region_name", "district", "district_name", "phone_number", "email", "address", "verification_status", "verified_at", "is_active"]
        read_only_fields = ["id", "owner", "verification_status", "verified_at", "is_active"]


class CredentialDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialDocument
        fields = ["id", "document_type", "mime_type", "sha256", "submitted_at", "is_private"]
        read_only_fields = ["id", "sha256", "submitted_at", "is_private"]


class ClinicStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicStaff
        fields = ["id", "clinic", "user", "title", "is_active", "joined_at"]
        read_only_fields = ["id", "joined_at"]
