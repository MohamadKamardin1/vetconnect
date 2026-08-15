import hashlib
import secrets
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from billing.clickpesa import ClickPesaClient, ClickPesaError, verify_payload_checksum
from billing.models import BadgePlan, BadgeSubscription, BillingStatus, PaymentTransaction, PaymentWebhookEvent
from professionals.models import VerificationStatus
from notifications.services import enqueue_notification
from notifications.tasks import deliver_notification_task


def normalize_tanzania_phone(value):
    digits = "".join(ch for ch in value if ch.isdigit())
    if digits.startswith("0") and len(digits) == 10:
        digits = "255" + digits[1:]
    if not digits.startswith("255") or len(digits) != 12:
        raise ValueError("Phone number must be a Tanzanian mobile number in 255XXXXXXXXX format.")
    return digits


def make_order_reference():
    return "VK" + secrets.token_hex(10).upper()


def create_badge_payment(*, professional, plan: BadgePlan, phone_number):
    if professional.professional_type.upper() not in {"VETERINARIAN", "VET_DOCTOR", "VETERINARY_DOCTOR"}:
        raise ValueError("Only veterinarian doctor profiles may purchase this verification badge.")
    if professional.verification_status != VerificationStatus.VERIFIED or not professional.is_active:
        raise ValueError("Professional KYC verification must be approved before purchasing a verification badge.")
    phone_number = normalize_tanzania_phone(phone_number)
    client_reference = make_order_reference()
    subscription = BadgeSubscription.objects.create(professional=professional, plan=plan, status=BillingStatus.PENDING)
    payment = PaymentTransaction.objects.create(subscription=subscription, payer=professional.user, client_reference=client_reference, provider_order_reference=client_reference, amount_tzs=plan.price_tzs, phone_number=phone_number, channel="USSD_PUSH", request_payload={"orderReference": client_reference, "amount": str(plan.price_tzs), "currency": "TZS", "phoneNumber": phone_number})
    return payment


def initiate_badge_payment(payment: PaymentTransaction):
    client = ClickPesaClient()
    preview = client.preview_ussd_push(amount=payment.amount_tzs, order_reference=payment.provider_order_reference, phone_number=payment.phone_number)
    initiation = client.initiate_ussd_push(amount=payment.amount_tzs, order_reference=payment.provider_order_reference, phone_number=payment.phone_number)
    payment.response_payload = {"preview": preview, "initiation": initiation}
    payment.provider_payment_reference = initiation.get("id", "")
    payment.status = BillingStatus.PENDING
    payment.save(update_fields=["response_payload", "provider_payment_reference", "status", "updated_at"])
    return payment


def _webhook_event_id(payload, data):
    return str(data.get("id") or data.get("paymentReference") or data.get("orderReference") or hashlib.sha256(str(payload).encode()).hexdigest())


def reconcile_clickpesa_webhook(*, payload, received_checksum):
    data = payload.get("data") or {}
    event_name = str(payload.get("event") or "").upper()
    checksum_valid = verify_payload_checksum(payload, received_checksum or payload.get("checksum", ""), settings.CLICKPESA_CHECKSUM_KEY)
    if settings.CLICKPESA_WEBHOOK_REQUIRE_CHECKSUM and not checksum_valid:
        raise ValueError("Invalid ClickPesa webhook checksum.")
    event_id = _webhook_event_id(payload, data)
    event, created = PaymentWebhookEvent.objects.get_or_create(provider="CLICKPESA", provider_event_id=event_id, defaults={"event_name": event_name, "order_reference": str(data.get("orderReference") or ""), "checksum_valid": checksum_valid, "payload": payload})
    if not created:
        return event, False
    order_reference = str(data.get("orderReference") or "")
    if not order_reference:
        event.processing_error = "Missing orderReference."
        event.save(update_fields=["processing_error"])
        return event, True
    with transaction.atomic():
        payment = PaymentTransaction.objects.select_for_update().filter(provider_order_reference=order_reference, provider="CLICKPESA").first()
        if payment is None:
            event.processing_error = "Unknown order reference."
            event.save(update_fields=["processing_error"])
            return event, True
        provider_status = str(data.get("status") or "").upper()
        if provider_status in {"SUCCESS", "SETTLED"} and event_name == "PAYMENT RECEIVED":
            collected_amount = Decimal(str(data.get("collectedAmount") or "0"))
            if data.get("collectedCurrency") and data.get("collectedCurrency") != payment.currency:
                payment.status = BillingStatus.FAILED
                payment.failure_reason = "Currency mismatch."
            elif collected_amount < payment.amount_tzs:
                payment.status = BillingStatus.FAILED
                payment.failure_reason = "Collected amount is lower than the subscription price."
            else:
                payment.status = BillingStatus.ACTIVE
                payment.paid_at = timezone.now()
                subscription = BadgeSubscription.objects.select_for_update().select_related("plan").get(pk=payment.subscription_id)
                start = max(timezone.now(), subscription.ends_at or timezone.now())
                subscription.status = BillingStatus.ACTIVE
                subscription.starts_at = subscription.starts_at or start
                subscription.ends_at = start + timedelta(days=subscription.plan.duration_days)
                subscription.save(update_fields=["status", "starts_at", "ends_at", "updated_at"])
                notification = enqueue_notification(recipient=payment.payer, event_key=f"badge.activated:{subscription.id}:{payment.id}", template_key="badge_activated", title="Verification badge activated", body="Your paid veterinarian verification badge is now active.", payload={"subscription_id": str(subscription.id), "ends_at": subscription.ends_at.isoformat()})
                transaction.on_commit(lambda: deliver_notification_task.apply(args=[str(notification.id)]) if settings.CELERY_TASK_ALWAYS_EAGER else deliver_notification_task.delay(str(notification.id)))
            payment.provider_payment_reference = str(data.get("paymentReference") or payment.provider_payment_reference)
        elif provider_status in {"FAILED", "CANCELLED", "REJECTED"} or event_name == "PAYMENT FAILED":
            payment.status = BillingStatus.FAILED
            payment.failure_reason = str(data.get("message") or "Payment failed.")[:500]
        payment.response_payload = payload
        payment.save(update_fields=["status", "paid_at", "failure_reason", "provider_payment_reference", "response_payload", "updated_at"])
        event.processed_at = timezone.now()
        event.save(update_fields=["processed_at"])
    return event, True
