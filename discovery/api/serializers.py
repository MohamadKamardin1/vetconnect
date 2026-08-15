from rest_framework import serializers
from discovery.models import Review, Service
from professionals.models import VerificationStatus


class ServiceSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(source="clinic.name", read_only=True)

    class Meta:
        model = Service
        fields = ["id", "clinic", "clinic_name", "professional", "name", "category", "description", "price_amount", "currency", "is_active"]
        read_only_fields = ["id", "clinic_name"]


class PublicReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.display_name", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "author", "clinic", "professional", "rating", "body", "created_at"]
        read_only_fields = fields


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["clinic", "professional", "rating", "body"]

    def validate(self, attrs):
        if bool(attrs.get("clinic")) == bool(attrs.get("professional")):
            raise serializers.ValidationError("Provide exactly one review target.")
        if attrs.get("professional") and attrs["professional"].verification_status != VerificationStatus.VERIFIED:
            raise serializers.ValidationError("The professional is not publicly reviewable.")
        if attrs.get("clinic") and attrs["clinic"].verification_status != VerificationStatus.VERIFIED:
            raise serializers.ValidationError("The clinic is not publicly reviewable.")
        return attrs

    def create(self, validated_data):
        return Review.objects.create(author=self.context["request"].user, **validated_data)
