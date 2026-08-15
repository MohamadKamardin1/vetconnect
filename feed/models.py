import uuid
from django.conf import settings
from django.db import models


class FeedRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    species_code = models.CharField(max_length=40)
    production_category = models.CharField(max_length=80)
    version = models.PositiveIntegerField(default=1)
    formula_key = models.CharField(max_length=120)
    assumptions = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["species_code", "production_category", "-version"]
        constraints = [models.UniqueConstraint(fields=["species_code", "production_category", "version"], name="unique_feed_rule_version")]


class FeedCalculation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="feed_calculations")
    rule = models.ForeignKey(FeedRule, on_delete=models.PROTECT, null=True, blank=True, related_name="calculations")
    inputs = models.JSONField()
    result = models.JSONField()
    status = models.CharField(max_length=32, choices=[("COMPLETED", "Completed"), ("MISSING_CONFIGURATION", "Missing configuration"), ("INVALID", "Invalid")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
