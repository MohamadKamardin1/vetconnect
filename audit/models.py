import uuid
from django.conf import settings
from django.db import models


class AuditLogEntry(models.Model):
    """
    Append-only record of a high-impact system or administrator action, per the specification's
    requirement that every such action carry rationale, before/after values, actor, timestamp, and
    request ID. Entries are never updated or deleted through the API; only created.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_actions")
    action = models.CharField(max_length=64)
    target_type = models.CharField(max_length=100, blank=True, default="")
    target_id = models.CharField(max_length=64, blank=True, default="")
    before = models.JSONField(default=dict, blank=True)
    after = models.JSONField(default=dict, blank=True)
    reason = models.TextField(blank=True, default="")
    request_id = models.CharField(max_length=64, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
        indexes = [models.Index(fields=["action", "-created_at"], name="audit_auditlog_action_idx"), models.Index(fields=["target_type", "target_id"], name="audit_auditlog_target_idx")]

    def __str__(self):
        return f"{self.action} on {self.target_type}:{self.target_id}"
