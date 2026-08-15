from celery import shared_task
from django.conf import settings
from notifications.models import Notification, NotificationStatus
from notifications.services import deliver_notification


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def deliver_notification_task(self, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if notification.status in {NotificationStatus.SENT, NotificationStatus.SUPPRESSED}:
        return notification.status
    if notification.attempts.count() >= settings.NOTIFICATION_MAX_ATTEMPTS:
        notification.status = NotificationStatus.FAILED
        notification.save(update_fields=["status"])
        return notification.status
    deliver_notification(notification)
    if notification.status == NotificationStatus.FAILED and notification.attempts.count() < settings.NOTIFICATION_MAX_ATTEMPTS:
        raise self.retry(countdown=min(300, 2 ** notification.attempts.count()))
    return notification.status


@shared_task
def dispatch_queued_notifications(limit=100):
    queued = Notification.objects.filter(status=NotificationStatus.QUEUED).order_by("created_at")[:limit]
    for notification in queued:
        deliver_notification_task.delay(str(notification.id))
    return len(queued)
