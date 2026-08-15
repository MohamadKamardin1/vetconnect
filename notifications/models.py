import uuid
from django.conf import settings
from django.db import models


def default_enabled_channels():
    return ["IN_APP"]


class NotificationChannel(models.TextChoices):
    IN_APP = "IN_APP", "In app"
    EMAIL = "EMAIL", "Email"
    SMS = "SMS", "SMS"
    PUSH = "PUSH", "Push"


class NotificationStatus(models.TextChoices):
    QUEUED = "QUEUED", "Queued"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"
    SUPPRESSED = "SUPPRESSED", "Suppressed"


class NotificationPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_preferences")
    locale = models.CharField(max_length=12, default="sw-TZ")
    timezone = models.CharField(max_length=64, default="Africa/Dar_es_Salaam")
    enabled_channels = models.JSONField(default=default_enabled_channels)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    marketing_enabled = models.BooleanField(default=False)
    clinical_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notifications")
    event_key = models.CharField(max_length=180)
    template_key = models.CharField(max_length=120)
    title = models.CharField(max_length=240)
    body = models.TextField(max_length=8000)
    payload = models.JSONField(default=dict)
    channel = models.CharField(max_length=16, choices=NotificationChannel.choices, default=NotificationChannel.IN_APP)
    status = models.CharField(max_length=16, choices=NotificationStatus.choices, default=NotificationStatus.QUEUED)
    available_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
        constraints = [models.UniqueConstraint(fields=["recipient", "event_key", "channel"], name="unique_notification_event_channel")]


class NotificationDeliveryAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="attempts")
    attempt_number = models.PositiveIntegerField()
    provider = models.CharField(max_length=64)
    provider_reference = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=16, choices=NotificationStatus.choices)
    response_metadata = models.JSONField(default=dict)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-attempted_at", "id"]
        constraints = [models.UniqueConstraint(fields=["notification", "attempt_number"], name="unique_notification_attempt")]
