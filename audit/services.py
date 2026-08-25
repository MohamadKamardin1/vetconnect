from audit.models import AuditLogEntry


def record_audit_event(*, actor=None, action, target=None, before=None, after=None, reason="", request_id=""):
    """
    Record one audit entry. `target`, if given, is any model instance; its class name and primary
    key are captured so the log never depends on the target still existing later. Never raises on
    missing optional fields — callers should be able to log best-effort even from exception handlers.
    """
    target_type = type(target).__name__ if target is not None else ""
    target_id = str(getattr(target, "pk", "")) if target is not None else ""
    return AuditLogEntry.objects.create(
        actor=actor,
        action=action,
        target_type=target_type,
        target_id=target_id,
        before=before or {},
        after=after or {},
        reason=reason or "",
        request_id=request_id or "",
    )
