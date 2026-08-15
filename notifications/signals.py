from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from messaging.models import Message
from notifications.models import NotificationPreference
from notifications.services import enqueue_notification
from notifications.tasks import deliver_notification_task


@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    if created:
        NotificationPreference.objects.get_or_create(user=instance)


@receiver(post_save, sender=Message)
def notify_conversation_participants(sender, instance, created, **kwargs):
    if not created:
        return
    participants = instance.conversation.participants.exclude(user=instance.sender).select_related("user")
    for participant in participants:
        notification = enqueue_notification(
            recipient=participant.user,
            event_key=f"message.created:{instance.id}",
            template_key="message_created",
            title="New message",
            body=f"You have a new message in {instance.conversation.subject or 'your conversation'}.",
            payload={"conversation_id": str(instance.conversation_id), "message_id": str(instance.id)},
        )
        if notification.status == "QUEUED":
            if getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False):
                deliver_notification_task.apply(args=[str(notification.id)])
            else:
                deliver_notification_task.delay(str(notification.id))
