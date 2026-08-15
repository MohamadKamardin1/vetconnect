from rest_framework import serializers
from billing.models import BadgePlan, BadgeSubscription, PaymentTransaction


class BadgePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgePlan
        fields = ["id", "code", "name", "price_tzs", "duration_days"]
        read_only_fields = fields


class BadgeSubscriptionSerializer(serializers.ModelSerializer):
    plan = BadgePlanSerializer(read_only=True)
    is_current = serializers.BooleanField(read_only=True)

    class Meta:
        model = BadgeSubscription
        fields = ["id", "plan", "status", "starts_at", "ends_at", "auto_renew_requested", "is_current", "created_at"]
        read_only_fields = fields


class BadgePaymentCreateSerializer(serializers.Serializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=BadgePlan.objects.filter(is_active=True))
    phone_number = serializers.CharField(max_length=20)


class ClickPesaWebhookSerializer(serializers.Serializer):
    event = serializers.CharField(max_length=80)
    data = serializers.JSONField()
    checksum = serializers.CharField(required=False, allow_blank=True)


class PaymentTransactionSerializer(serializers.ModelSerializer):
    subscription = BadgeSubscriptionSerializer(read_only=True)

    class Meta:
        model = PaymentTransaction
        fields = ["id", "subscription", "client_reference", "provider_payment_reference", "amount_tzs", "currency", "channel", "status", "phone_number", "failure_reason", "paid_at", "created_at"]
        read_only_fields = fields
