import uuid
from django.conf import settings
from django.db import models


class DiseaseRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    species_code = models.CharField(max_length=40)
    version = models.PositiveIntegerField(default=1)
    symptom_weights = models.JSONField(default=dict)
    high_risk_symptoms = models.JSONField(default=list)
    disclaimer = models.TextField(default="This is decision support, not a definitive diagnosis. Consult a qualified veterinary professional.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["species_code", "-version"]
        constraints = [models.UniqueConstraint(fields=["species_code", "version"], name="unique_disease_rule_version")]


class DiseaseAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="disease_assessments")
    rule = models.ForeignKey(DiseaseRule, on_delete=models.PROTECT, null=True, blank=True, related_name="assessments")
    inputs = models.JSONField()
    output = models.JSONField()
    status = models.CharField(max_length=32, choices=[("COMPLETED", "Completed"), ("MISSING_CONFIGURATION", "Missing configuration"), ("INVALID", "Invalid")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
