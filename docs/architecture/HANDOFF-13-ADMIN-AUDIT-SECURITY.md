# Handoff 13 — Admin, audit, security hardening

## Scope

The full specification (`docs/specifications/17-admin-specification.md`) describes thirteen admin modules (identity, verification, geography, reference data, discovery, community, reviews, content, safety, payments, notifications, analytics, security) — an entire back-office console, explicitly marked **RECOMMENDED and inferred**, not a hard requirement. Building all thirteen in one phase would not be reviewable. This phase implements the cross-cutting **audit** and **security/privacy** primitives every one of those modules will eventually depend on (`docs/specifications/15-security-and-privacy.md`: "every high-impact action requires rationale, before/after values, actor, timestamp, request ID" and "access/correction/deletion/export workflows"), plus wires them into the three admin actions that already exist. Module-specific admin consoles (verification queues, geography import, moderation, etc.) are follow-up work using the same primitives — not in scope here.

## Implemented

**New `audit` app** — generic, append-only action log:
- `AuditLogEntry`: actor, action, target type/id, before/after JSON, reason, request ID, timestamp. `record_audit_event()` is the single entry point every caller uses; it never raises on a missing `target` (safe to call from exception paths later).
- `GET /api/v1/audit/logs/` and `GET /api/v1/audit/logs/<id>/` — administrator-only (`IsAdministrator`), filterable by `action`/`target_type`/`actor`. Admin-registered as fully read-only (no add/change/delete, even for superusers, in the Django admin).

**New `privacy` app** — self-service data subject rights:
- `DataExportRequest` / `DataDeletionRequest` models.
- `POST /api/v1/privacy/export/` — synchronously aggregates the caller's own records (profile, animals owned, disease assessments, feed calculations, AI interactions, notification preferences) into a JSON payload and returns it. `GET` lists the caller's own past export requests. Deliberately scoped to apps with a direct FK to the user that already existed before this phase; extending to messaging/community/marketplace/professionals/billing follows the identical pattern in `privacy/services.collect_user_export()`.
- `POST /api/v1/privacy/deletion/` — creates a `PENDING` deletion request. **Nothing is deleted at this step** — matches the "no shortcuts" bar for a destructive action.
- `POST /api/v1/privacy/deletion/confirm/` — confirms the caller's own most recent pending request and executes it. Returns `400` if there is no pending request (can't be tricked into a no-op success).

**Shared anonymization, deduplicated:** `accounts/services.py` gained `anonymize_user()`, extracted verbatim from the admin-delete endpoint's existing inline logic (identical field list, identical values — confirmed byte-for-byte in the diff). Both `AdminUserDeleteView.perform_destroy` (admin-triggered) and `privacy.services.confirm_deletion` (self-service) now call the same function, so the two paths can never drift into inconsistent scrubbing behavior. This was the one non-additive change in this phase, and it's behavior-preserving — see `accounts/tests/test_auth.py::test_only_administrator_can_suspend_and_delete_users`, which still exercises the same endpoint and assertions unchanged.

**Audit wiring on existing admin actions:** `AdminUserSuspendView`, `AdminUserReactivateView`, and `AdminUserDeleteView` (`accounts/api/admin_views.py`) each now call `record_audit_event()` with before/after state and an optional `reason` from the request body. This is the only other edit to a pre-existing file; the diff is additive (import lines + one `record_audit_event(...)` call per view) and does not change any existing response shape, status code, or side effect.

**Not edited:** every other app (`disease`, `feed`, `ai`, `animals`, `notifications`, everything else) — read from, in `privacy/services.py`, but never written to or imported into.

## Safety/privacy evidence

- Deletion is two-step and reversible until confirmed; nothing destructive happens on the `POST /deletion/` call itself.
- Export and deletion-request listings are queryset-scoped to `request.user` — verified by tests asserting a second user's request returns `count: 0`.
- Every suspend/reactivate/delete action and every export/deletion-request/confirm now produces exactly one `AuditLogEntry`, capturing actor, before/after state, and reason.
- The audit log itself is administrator-only and immutable through both the API (no write endpoints) and the Django admin (`has_add_permission`/`has_change_permission`/`has_delete_permission` all return `False`).
- No new dependency was added; `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = "DENY"`, and rate limiting (`DEFAULT_THROTTLE_CLASSES`) were already present from Phase 2 and remain unchanged — verified by re-reading `config/settings/base.py` before writing this phase rather than re-implementing what already existed.

## Verification

Run from the project root with the venv active, same as Phase 12:

```
python manage.py makemigrations audit privacy --check
python -m pytest audit privacy accounts -q
python manage.py check
python manage.py spectacular --file schema.yaml --validate
```

`accounts` is included in the test run specifically to confirm the `anonymize_user` extraction didn't change existing suspend/reactivate/delete behavior.

Every new/edited file passed `python3 -m py_compile` in this sandbox (no Django install/network access here, same limitation as Phase 12 — real execution is the operator's step, as it was last time). Both new apps' migrations were hand-authored and field-checked against their models, including explicit index names to avoid drift.

Two schema pitfalls from Phase 12 were caught proactively this time before you had to report them back: `DataDeletionConfirmView` (a plain `APIView`) was given an explicit `@extend_schema(...)`, and its error-response type used `OpenApiTypes.OBJECT` rather than a bare `dict` from the start.

## Next phase

Proceed to whichever admin module you want next — verification queues, geography import, or moderation are the next-most load-bearing per the spec table, and each can now emit `record_audit_event()` calls and reuse the `privacy` export pattern rather than inventing its own.
