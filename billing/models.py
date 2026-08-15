import uuid
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from professionals.models import ProfessionalProfile


class BadgePlanCode(models.TextChoices):
    WEEKLY = "WEEKLY", "Weekly"
    MONTHLY = "MONTHLY", "Monthly"
    YEARLY = "YEARLY", "Yearly"


class BillingStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    FAILED = "FAILED", "Failed"
    EXPIRED = "EXPIRED", "Expired"
    CANCELLED = "CANCELLED", "Cancelled"
    REFUNDED = "REFUNDED", "Refunded"


class PaymentChannel(models.TextChoices):
    USSD_PUSH = "USSD_PUSH", "USSD Push"
    BILLPAY = "BILLPAY", "BillPay"
    CARD = "CARD", "Card"
    UNKNOWN = "UNKNOWN", "Unknown"


class BadgePlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=16, choices=BadgePlanCode.choices, unique=True)
    name = models.CharField(max_length=80)
    price_tzs = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["duration_days", "price_tzs"]


class BadgeSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.PROTECT, related_name="badge_subscriptions")
    plan = models.ForeignKey(BadgePlan, on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(max_length=16, choices=BillingStatus.choices, default=BillingStatus.PENDING)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    auto_renew_requested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "id"]
        indexes = [models.Index(fields=["professional", "status", "ends_at"])]

    @property
    def is_current(self):
        return self.status == BillingStatus.ACTIVE and self.starts_at and self.ends_at and self.starts_at <= timezone.now() < self.ends_at


class PaymentTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(BadgeSubscription, on_delete=models.PROTECT, related_name="payments")
    payer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payment_transactions")
    provider = models.CharField(max_length=40, default="CLICKPESA")
    client_reference = models.CharField(max_length=64, unique=True)
    provider_payment_reference = models.CharField(max_length=180, blank=True, db_index=True)
    provider_order_reference = models.CharField(max_length=180, blank=True, db_index=True)
    amount_tzs = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    currency = models.CharField(max_length=3, default="TZS")
    channel = models.CharField(max_length=16, choices=PaymentChannel.choices, default=PaymentChannel.USSD_PUSH)
    status = models.CharField(max_length=16, choices=BillingStatus.choices, default=BillingStatus.PENDING)
    phone_number = models.CharField(max_length=20)
    request_payload = models.JSONField(default=dict)
    response_payload = models.JSONField(default=dict)
    failure_reason = models.CharField(max_length=500, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "id"]
        constraints = [models.UniqueConstraint(fields=["provider", "provider_order_reference"], name="unique_provider_order_reference")]


class PaymentWebhookEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=40, default="CLICKPESA")
    event_name = models.CharField(max_length=80)
    provider_event_id = models.CharField(max_length=180)
    order_reference = models.CharField(max_length=180, blank=True, db_index=True)
    checksum_valid = models.BooleanField(default=False)
    payload = models.JSONField(default=dict)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_error = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["-received_at", "id"]
        constraints = [models.UniqueConstraint(fields=["provider", "provider_event_id"], name="unique_provider_webhook_event")]
