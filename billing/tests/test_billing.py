from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch
import pytest
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from accounts.models import User
from billing.clickpesa import payload_checksum
from billing.models import BadgePlan, BadgeSubscription, BillingStatus, PaymentTransaction, PaymentWebhookEvent
from locations.models import District, Region, Territory
from professionals.models import ProfessionalProfile, VerificationStatus


@pytest.fixture
def location_tree(db):
    region = Region.objects.create(code="ZNZ", name="Zanzibar", territory=Territory.ZANZIBAR)
    district = District.objects.create(region=region, code="ZNZ-URB", name="Zanzibar Urban")
    return region, district


@pytest.fixture
def plan(db):
    return BadgePlan.objects.create(code="MONTHLY", name="Monthly verified badge", price_tzs=Decimal("15000.00"), duration_days=30)


@pytest.fixture
def verified_vet(location_tree):
    region, district = location_tree
    user = User.objects.create_user(email="verified-vet@example.tz", password="StrongPassword123!")
    profile = ProfessionalProfile.objects.create(user=user, professional_type="VETERINARIAN", registration_number="VET-BILL-001", issuing_body="VCT", region=region, district=district, verification_status=VerificationStatus.VERIFIED, verified_at=timezone.now())
    return user, profile


@pytest.mark.django_db
def test_unverified_vet_cannot_start_badge_payment(plan, location_tree):
    region, district = location_tree
    user = User.objects.create_user(email="unverified-vet@example.tz", password="StrongPassword123!")
    ProfessionalProfile.objects.create(user=user, professional_type="VETERINARIAN", registration_number="VET-BILL-002", issuing_body="VCT", region=region, district=district)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post("/api/v1/billing/badge-payments/", {"plan": str(plan.pk), "phone_number": "255700000000"}, format="json")
    assert response.status_code == 400
    assert PaymentTransaction.objects.count() == 0


@pytest.mark.django_db
@override_settings(CLICKPESA_CHECKSUM_KEY="test-checksum", CLICKPESA_WEBHOOK_REQUIRE_CHECKSUM=True, CELERY_TASK_ALWAYS_EAGER=False)
def test_verified_webhook_activates_badge_once_and_replay_is_idempotent(plan, verified_vet):
    user, profile = verified_vet
    payment = PaymentTransaction.objects.create(subscription=BadgeSubscription.objects.create(professional=profile, plan=plan), payer=user, client_reference="VKORDER001", provider_order_reference="VKORDER001", amount_tzs=plan.price_tzs, phone_number="255700000000")
    payload = {"event": "PAYMENT RECEIVED", "data": {"id": "CP-EVENT-001", "status": "SUCCESS", "paymentReference": "CP-PAY-001", "orderReference": "VKORDER001", "collectedAmount": "15000", "collectedCurrency": "TZS", "channel": "M-PESA"}}
    payload["checksum"] = payload_checksum(payload, "test-checksum")
    client = APIClient()
    first = client.post("/api/v1/billing/webhooks/clickpesa/", payload, format="json")
    second = client.post("/api/v1/billing/webhooks/clickpesa/", payload, format="json")
    assert first.status_code == 200 and first.data["duplicate"] is False
    assert second.status_code == 200 and second.data["duplicate"] is True
    payment.refresh_from_db()
    assert payment.status == BillingStatus.ACTIVE
    assert BadgeSubscription.objects.get(pk=payment.subscription_id).is_current
    assert PaymentWebhookEvent.objects.count() == 1


@pytest.mark.django_db
@override_settings(CLICKPESA_CHECKSUM_KEY="test-checksum", CLICKPESA_WEBHOOK_REQUIRE_CHECKSUM=True)
def test_invalid_checksum_is_rejected(plan, verified_vet):
    user, profile = verified_vet
    BadgeSubscription.objects.create(professional=profile, plan=plan)
    payload = {"event": "PAYMENT RECEIVED", "data": {"id": "CP-EVENT-002", "status": "SUCCESS", "orderReference": "UNKNOWN", "collectedAmount": "15000", "collectedCurrency": "TZS"}, "checksum": "bad"}
    response = APIClient().post("/api/v1/billing/webhooks/clickpesa/", payload, format="json")
    assert response.status_code == 400
    assert PaymentWebhookEvent.objects.count() == 0


@pytest.mark.django_db
@override_settings(CLICKPESA_CHECKSUM_KEY="test-checksum", CLICKPESA_WEBHOOK_REQUIRE_CHECKSUM=True)
def test_underpayment_never_activates_badge(plan, verified_vet):
    user, profile = verified_vet
    subscription = BadgeSubscription.objects.create(professional=profile, plan=plan)
    payment = PaymentTransaction.objects.create(subscription=subscription, payer=user, client_reference="VKORDER002", provider_order_reference="VKORDER002", amount_tzs=plan.price_tzs, phone_number="255700000000")
    payload = {"event": "PAYMENT RECEIVED", "data": {"id": "CP-EVENT-003", "status": "SUCCESS", "orderReference": "VKORDER002", "collectedAmount": "1000", "collectedCurrency": "TZS"}}
    payload["checksum"] = payload_checksum(payload, "test-checksum")
    response = APIClient().post("/api/v1/billing/webhooks/clickpesa/", payload, format="json")
    assert response.status_code == 200
    payment.refresh_from_db()
    subscription.refresh_from_db()
    assert payment.status == BillingStatus.FAILED
    assert subscription.status == BillingStatus.PENDING


@pytest.mark.django_db
@override_settings(CLICKPESA_CHECKSUM_KEY="test-checksum", CLICKPESA_WEBHOOK_REQUIRE_CHECKSUM=True)
def test_public_profile_badge_requires_active_subscription(plan, verified_vet, location_tree):
    user, profile = verified_vet
    public = APIClient().get("/api/v1/professionals/professionals/")
    assert public.data["results"][0]["is_verified_badge"] is False
    BadgeSubscription.objects.create(professional=profile, plan=plan, status=BillingStatus.ACTIVE, starts_at=timezone.now() - timedelta(days=1), ends_at=timezone.now() + timedelta(days=29))
    public = APIClient().get("/api/v1/professionals/professionals/")
    assert public.data["results"][0]["is_verified_badge"] is True
