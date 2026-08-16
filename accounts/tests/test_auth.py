import pytest
import re
from django.core import mail
from django.utils import timezone
from rest_framework.test import APIClient
from accounts.models import OneTimeToken, RoleCode, User


@pytest.mark.django_db
def test_registration_sends_six_digit_email_code_and_keeps_account_inactive():
    response = APIClient().post("/api/v1/auth/register/", {"email": "owner@example.tz", "password": "StrongPassword123!", "first_name": "Asha"}, format="json")
    assert response.status_code == 201
    user = User.objects.get(email="owner@example.tz")
    assert user.has_role(RoleCode.OWNER)
    assert user.is_active is False
    assert user.email_verified_at is None
    assert "password" not in response.data
    assert response.data["status"] == "verification_pending"
    assert re.search(r"\b\d{6}\b", mail.outbox[-1].body)


@pytest.mark.django_db
def test_email_code_activates_account_and_returns_tokens():
    client = APIClient()
    registered = client.post("/api/v1/auth/register/", {"email": "verify@example.tz", "password": "StrongPassword123!", "first_name": "Asha"}, format="json")
    assert registered.status_code == 201
    code = re.search(r"\b(\d{6})\b", mail.outbox[-1].body).group(1)
    verified = client.post("/api/v1/auth/verify-email/", {"email": "verify@example.tz", "code": code}, format="json")
    assert verified.status_code == 200
    assert verified.data["access"]
    user = User.objects.get(email="verify@example.tz")
    assert user.is_active is True
    assert user.email_verified_at is not None


@pytest.mark.django_db
def test_email_code_expires_after_failed_attempt_limit():
    client = APIClient()
    client.post("/api/v1/auth/register/", {"email": "limited@example.tz", "password": "StrongPassword123!", "first_name": "Asha"}, format="json")
    for _ in range(5):
        response = client.post("/api/v1/auth/verify-email/", {"email": "limited@example.tz", "code": "000000"}, format="json")
        assert response.status_code == 400
    token = OneTimeToken.objects.get(user__email="limited@example.tz", purpose=OneTimeToken.Purpose.EMAIL_VERIFY)
    assert token.used_at is not None
    assert token.attempt_count == 5


@pytest.mark.django_db
def test_login_returns_access_and_refresh_tokens():
    User.objects.create_user(email="vet@example.tz", password="StrongPassword123!")
    response = APIClient().post("/api/v1/auth/login/", {"email": "vet@example.tz", "password": "StrongPassword123!"}, format="json")
    assert response.status_code == 200
    assert response.data["access"]
    assert response.data["refresh"]


@pytest.mark.django_db
def test_login_does_not_enumerate_invalid_credentials():
    response = APIClient().post("/api/v1/auth/login/", {"email": "missing@example.tz", "password": "wrong-password"}, format="json")
    assert response.status_code == 400
    assert "does not exist" not in str(response.data).lower()


@pytest.mark.django_db
def test_me_is_object_scoped_to_authenticated_user():
    user = User.objects.create_user(email="one@example.tz", password="StrongPassword123!")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/v1/users/me/")
    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_suspended_user_cannot_login():
    user = User.objects.create_user(email="suspended@example.tz", password="StrongPassword123!")
    user.is_active = False
    user.suspended_at = timezone.now()
    user.save(update_fields=["is_active", "suspended_at"])
    response = APIClient().post("/api/v1/auth/login/", {"email": user.email, "password": "StrongPassword123!"}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_one_time_token_is_single_use_and_expiry_bound():
    user = User.objects.create_user(email="token@example.tz", password="StrongPassword123!")
    token, raw = OneTimeToken.issue(user, OneTimeToken.Purpose.PASSWORD_RESET)
    assert token.consume(raw) is True
    assert token.consume(raw) is False
    expired, expired_raw = OneTimeToken.issue(user, OneTimeToken.Purpose.PASSWORD_RESET, ttl_minutes=-1)
    assert expired.consume(expired_raw) is False


@pytest.mark.django_db
def test_only_administrator_can_suspend_and_delete_users():
    admin = User.objects.create_superuser(email="admin@example.tz", password="StrongPassword123!")
    target = User.objects.create_user(email="target@example.tz", password="StrongPassword123!")
    ordinary = User.objects.create_user(email="ordinary@example.tz", password="StrongPassword123!")

    ordinary_client = APIClient()
    ordinary_client.force_authenticate(user=ordinary)
    denied = ordinary_client.post(f"/api/v1/auth/admin/users/{target.pk}/suspend/", {}, format="json")
    assert denied.status_code == 403

    admin_client = APIClient()
    admin_client.force_authenticate(user=admin)
    suspended = admin_client.post(f"/api/v1/auth/admin/users/{target.pk}/suspend/", {}, format="json")
    assert suspended.status_code == 200
    target.refresh_from_db()
    assert target.is_active is False

    reactivated = admin_client.post(f"/api/v1/auth/admin/users/{target.pk}/reactivate/", {}, format="json")
    assert reactivated.status_code == 200
    target.refresh_from_db()
    assert target.is_active is True

    deleted = admin_client.delete(f"/api/v1/auth/admin/users/{target.pk}/delete/")
    assert deleted.status_code == 204
    target.refresh_from_db()
    assert target.is_active is False
    assert target.has_usable_password() is False
