import pytest
from rest_framework.test import APIClient
from accounts.models import User
from audit.models import AuditLogEntry


def _client(email, is_admin=False):
    user = User.objects.create_superuser(email=email, password="StrongPass123!") if is_admin else User.objects.create_user(email=email, password="StrongPass123!")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
def test_admin_suspend_reactivate_delete_creates_audit_entries():
    admin_client, admin = _client("audit-admin@example.com", is_admin=True)
    _target_client, target = _client("audit-target@example.com")

    response = admin_client.post(f"/api/v1/auth/admin/users/{target.pk}/suspend/", {"reason": "policy violation"}, format="json")
    assert response.status_code == 200
    target.refresh_from_db()
    assert target.is_active is False

    response = admin_client.post(f"/api/v1/auth/admin/users/{target.pk}/reactivate/", {}, format="json")
    assert response.status_code == 200

    response = admin_client.delete(f"/api/v1/auth/admin/users/{target.pk}/delete/")
    assert response.status_code == 204
    target.refresh_from_db()
    assert target.is_active is False
    assert target.email.startswith("deleted+")

    actions = set(AuditLogEntry.objects.filter(target_id=str(target.pk)).values_list("action", flat=True))
    assert actions == {"USER_SUSPENDED", "USER_REACTIVATED", "USER_DELETED"}
    suspend_entry = AuditLogEntry.objects.get(action="USER_SUSPENDED", target_id=str(target.pk))
    assert suspend_entry.actor == admin
    assert suspend_entry.reason == "policy violation"
    assert suspend_entry.before == {"is_active": True}
    assert suspend_entry.after == {"is_active": False}


@pytest.mark.django_db
def test_audit_log_is_admin_only():
    ordinary_client, _ordinary = _client("audit-ordinary@example.com")
    admin_client, _admin = _client("audit-admin2@example.com", is_admin=True)
    AuditLogEntry.objects.create(action="SYSTEM_EVENT")

    denied = ordinary_client.get("/api/v1/audit/logs/")
    assert denied.status_code == 403

    allowed = admin_client.get("/api/v1/audit/logs/")
    assert allowed.status_code == 200
    assert allowed.data["count"] == 1


@pytest.mark.django_db
def test_audit_log_filters_by_action():
    admin_client, _admin = _client("audit-admin3@example.com", is_admin=True)
    AuditLogEntry.objects.create(action="USER_SUSPENDED")
    AuditLogEntry.objects.create(action="USER_DELETED")

    response = admin_client.get("/api/v1/audit/logs/?action=USER_DELETED")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["action"] == "USER_DELETED"
