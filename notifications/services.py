from django.conf import settings
from django.utils import timezone
from notifications.models import Notification, NotificationChannel, NotificationDeliveryAttempt, NotificationPreference, NotificationStatus


class ProviderResult:
    def __init__(self, ok, provider, reference="", metadata=None):
        self.ok = ok
        self.provider = provider
        self.reference = reference
        self.metadata = metadata or {}


def get_preferences(user):
    preferences, _ = NotificationPreference.objects.get_or_create(user=user)
    return preferences


def channel_enabled(user, channel, *, clinical=False):
    preferences = get_preferences(user)
    if clinical and not preferences.clinical_enabled:
        return False
    if channel != NotificationChannel.IN_APP and channel not in preferences.enabled_channels:
        return False
    return True


def enqueue_notification(*, recipient, event_key, template_key, title, body, payload=None, channel=NotificationChannel.IN_APP, clinical=False):
    if not channel_enabled(recipient, channel, clinical=clinical):
        return Notification.objects.create(recipient=recipient, event_key=event_key, template_key=template_key, title=title, body=body, payload=payload or {}, channel=channel, status=NotificationStatus.SUPPRESSED)
    notification, _ = Notification.objects.get_or_create(recipient=recipient, event_key=event_key, channel=channel, defaults={"template_key": template_key, "title": title, "body": body, "payload": payload or {}, "status": NotificationStatus.QUEUED})
    return notification


def send_via_provider(notification):
    if notification.channel == NotificationChannel.IN_APP:
        return ProviderResult(True, "in_app", str(notification.id), {"stored": True})
    provider = getattr(settings, f"NOTIFICATION_{notification.channel}_PROVIDER", "noop").lower()
    if provider in {"noop", "console"}:
        return ProviderResult(provider == "console", provider, "", {"configured": provider == "console"})
    return ProviderResult(False, provider, "", {"error": "Provider adapter is not implemented for this environment."})


def deliver_notification(notification):
    if notification.status == NotificationStatus.SUPPRESSED:
        return notification
    attempt_number = notification.attempts.count() + 1
    result = send_via_provider(notification)
    NotificationDeliveryAttempt.objects.create(notification=notification, attempt_number=attempt_number, provider=result.provider, provider_reference=result.reference, status=NotificationStatus.SENT if result.ok else NotificationStatus.FAILED, response_metadata=result.metadata)
    notification.status = NotificationStatus.SENT if result.ok else NotificationStatus.FAILED
    if result.ok:
        notification.sent_at = timezone.now()
    notification.save(update_fields=["status", "sent_at"])
    return notification
