import uuid
from django.conf import settings
from django.db import models


class AIInteractionStatus(models.TextChoices):
    COMPLETED = "COMPLETED", "Completed"
    FALLBACK = "FALLBACK", "Fallback"
    FAILED = "FAILED", "Failed"
    SUPPRESSED = "SUPPRESSED", "Suppressed"


class HumanReviewStatus(models.TextChoices):
    NOT_REQUIRED = "NOT_REQUIRED", "Not required"
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class AIProviderConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider_key = models.CharField(max_length=40, unique=True)
    display_name = models.CharField(max_length=120)
    model_name = models.CharField(max_length=120)
    model_version = models.CharField(max_length=40)
    is_enabled = models.BooleanField(default=False)
    timeout_seconds = models.PositiveSmallIntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["provider_key"]

    def __str__(self):
        return self.provider_key


class AIFeatureConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feature_key = models.CharField(max_length=40, unique=True)
    is_enabled = models.BooleanField(default=False)
    requires_human_review_on_urgent = models.BooleanField(default=True)
    provider = models.ForeignKey(AIProviderConfig, on_delete=models.SET_NULL, null=True, blank=True, related_name="features")
    allowed_context_fields = models.JSONField(default=list, help_text="Allowlist of field names permitted to leave the process boundary for this feature.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["feature_key"]

    def __str__(self):
        return self.feature_key


class AIInteraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ai_interactions")
    feature_key = models.CharField(max_length=40)
    provider_key = models.CharField(max_length=40, blank=True, default="")
    model_version = models.CharField(max_length=40, blank=True, default="")
    input_hash = models.CharField(max_length=64)
    redacted_input = models.JSONField(default=dict)
    output = models.JSONField(default=dict)
    status = models.CharField(max_length=16, choices=AIInteractionStatus.choices)
    latency_ms = models.PositiveIntegerField(default=0)
    human_review_status = models.CharField(max_length=16, choices=HumanReviewStatus.choices, default=HumanReviewStatus.NOT_REQUIRED)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="ai_reviews")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
        indexes = [models.Index(fields=["user", "feature_key"], name="ai_aiintera_user_id_1f6c4a_idx"), models.Index(fields=["human_review_status"], name="ai_aiintera_human_r_9b2d3e_idx")]
