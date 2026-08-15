import uuid
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from professionals.models import Clinic, ProfessionalProfile


class ModerationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    HIDDEN = "HIDDEN", "Hidden"


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="services")
    professional = models.ForeignKey(ProfessionalProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name="services")
    name = models.CharField(max_length=180)
    category = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    price_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="TZS")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "id"]
        indexes = [models.Index(fields=["category", "is_active"]), models.Index(fields=["clinic", "is_active"])]


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reviews_written")
    clinic = models.ForeignKey(Clinic, null=True, blank=True, on_delete=models.CASCADE, related_name="reviews")
    professional = models.ForeignKey(ProfessionalProfile, null=True, blank=True, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    body = models.TextField(max_length=2000)
    moderation_status = models.CharField(max_length=20, choices=ModerationStatus.choices, default=ModerationStatus.PENDING)
    moderation_reason = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "id"]
        constraints = [
            models.CheckConstraint(condition=(models.Q(clinic__isnull=False) | models.Q(professional__isnull=False)), name="review_has_target"),
            models.UniqueConstraint(fields=["author", "clinic"], name="unique_review_author_clinic"),
            models.UniqueConstraint(fields=["author", "professional"], name="unique_review_author_professional"),
        ]
        indexes = [models.Index(fields=["moderation_status", "created_at"])]

    @property
    def is_public(self):
        return self.moderation_status == ModerationStatus.APPROVED
