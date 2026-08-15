from celery import shared_task
from django.utils import timezone
from billing.clickpesa import ClickPesaClient
from billing.models import BadgeSubscription, BillingStatus, PaymentTransaction
from billing.services import initiate_badge_payment, reconcile_clickpesa_webhook


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def initiate_clickpesa_payment_task(self, payment_id):
    payment = PaymentTransaction.objects.get(id=payment_id)
    if payment.status != BillingStatus.PENDING:
        return payment.status
    initiate_badge_payment(payment)
    return payment.status


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def refresh_clickpesa_payment_status_task(self, payment_id):
    payment = PaymentTransaction.objects.get(id=payment_id)
    if payment.status in {BillingStatus.ACTIVE, BillingStatus.FAILED, BillingStatus.REFUNDED}:
        return payment.status
    result = ClickPesaClient().payment_status(payment.provider_order_reference)
    items = result if isinstance(result, list) else [result]
    latest = items[-1] if items else {}
    payload = {"event": "PAYMENT RECEIVED" if str(latest.get("status", "")).upper() in {"SUCCESS", "SETTLED"} else "PAYMENT FAILED", "data": latest}
    reconcile_clickpesa_webhook(payload=payload, received_checksum=latest.get("checksum", ""))
    payment.refresh_from_db()
    return payment.status


@shared_task
def expire_badge_subscriptions():
    now = timezone.now()
    return BadgeSubscription.objects.filter(status=BillingStatus.ACTIVE, ends_at__lte=now).update(status=BillingStatus.EXPIRED, updated_at=now)
