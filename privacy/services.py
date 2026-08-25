from django.utils import timezone

from accounts.services import anonymize_user
from ai.models import AIInteraction
from animals.models import Animal
from disease.models import DiseaseAssessment
from feed.models import FeedCalculation
from notifications.models import NotificationPreference
from privacy.models import DataDeletionRequest, DataExportRequest


def collect_user_export(user):
    """
    Aggregate the minimum-necessary set of a user's own records across domain apps with a direct
    ownership relationship. This is additive, read-only, and does not modify any other app. Extending
    coverage to further apps (messaging, community, marketplace, professionals, billing) follows the
    same pattern and is a deliberately scoped follow-up, documented in the Phase 13 handoff.
    """
    return {
        "profile": {
            "id": str(user.pk),
            "email": user.email,
            "phone_number": user.phone_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat(),
            "email_verified_at": user.email_verified_at.isoformat() if user.email_verified_at else None,
        },
        "animals": [{"id": str(a.id), "name": a.name, "species": a.species, "breed": a.breed, "created_at": a.created_at.isoformat()} for a in Animal.objects.filter(owner=user)],
        "disease_assessments": [{"id": str(r.id), "status": r.status, "output": r.output, "created_at": r.created_at.isoformat()} for r in DiseaseAssessment.objects.filter(requested_by=user)],
        "feed_calculations": [{"id": str(r.id), "status": r.status, "result": r.result, "created_at": r.created_at.isoformat()} for r in FeedCalculation.objects.filter(requested_by=user)],
        "ai_interactions": [{"id": str(r.id), "feature_key": r.feature_key, "status": r.status, "created_at": r.created_at.isoformat()} for r in AIInteraction.objects.filter(user=user)],
        "notification_preferences": _export_notification_preferences(user),
    }


def _export_notification_preferences(user):
    preferences = NotificationPreference.objects.filter(user=user).first()
    if not preferences:
        return None
    return {"locale": preferences.locale, "timezone": preferences.timezone, "enabled_channels": preferences.enabled_channels}


def run_export(export_request):
    export_request.payload = collect_user_export(export_request.user)
    export_request.status = DataExportRequest.Status.COMPLETED
    export_request.completed_at = timezone.now()
    export_request.save(update_fields=["payload", "status", "completed_at"])
    return export_request


def confirm_deletion(deletion_request):
    """Execute a pending deletion request: anonymize the account via the same shared path administrator-triggered deletion uses."""
    anonymize_user(deletion_request.user)
    deletion_request.status = DataDeletionRequest.Status.COMPLETED
    deletion_request.completed_at = timezone.now()
    deletion_request.save(update_fields=["status", "completed_at"])
    return deletion_request
