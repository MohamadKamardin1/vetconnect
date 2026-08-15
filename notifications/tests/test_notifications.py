from celery import current_app
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from accounts.models import User
from notifications.models import Notification, NotificationChannel, NotificationStatus
from notifications.services import enqueue_notification
from notifications.tasks import deliver_notification_task


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, NOTIFICATION_EMAIL_PROVIDER="console")
class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner@example.com", "Passw0rd!", first_name="Asha")
        self.other = User.objects.create_user("other@example.com", "Passw0rd!")

    def test_in_app_delivery_is_eager_and_idempotent(self):
        notification = enqueue_notification(recipient=self.user, event_key="animal.created:1", template_key="animal_created", title="Animal added", body="Your animal was added.")
        current_app.conf.update(task_always_eager=True, task_eager_propagates=True)
        deliver_notification_task.delay(str(notification.id))
        notification.refresh_from_db()
        self.assertEqual(notification.status, NotificationStatus.SENT)
        self.assertEqual(notification.attempts.count(), 1)
        duplicate = enqueue_notification(recipient=self.user, event_key="animal.created:1", template_key="animal_created", title="Changed", body="Changed")
        self.assertEqual(duplicate.id, notification.id)
        self.assertEqual(Notification.objects.filter(recipient=self.user).count(), 1)

    def test_disabled_email_is_suppressed(self):
        notification = enqueue_notification(recipient=self.user, event_key="billing:1", template_key="billing", title="Receipt", body="Receipt", channel=NotificationChannel.EMAIL)
        self.assertEqual(notification.status, NotificationStatus.SUPPRESSED)

    def test_api_cannot_read_another_users_notification(self):
        notification = Notification.objects.create(recipient=self.user, event_key="private:1", template_key="private", title="Private", body="Private")
        client = APIClient()
        client.force_authenticate(self.other)
        response = client.get(f"/api/v1/notifications/{notification.id}/")
        self.assertEqual(response.status_code, 404)
