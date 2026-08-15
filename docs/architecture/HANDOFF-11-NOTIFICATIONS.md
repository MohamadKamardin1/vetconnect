# Handoff 11 — Notifications and Background Tasks

## Scope

Prompt 11 is complete for the unified notification subsystem. The implementation provides in-app notification records, per-user delivery preferences, delivery-attempt audit records, provider-neutral delivery boundaries, Celery delivery tasks with bounded exponential retry, authenticated notification APIs, and signal-driven account/message notification hooks.

## Implemented

- `NotificationPreference` with locale, timezone, channel opt-ins, quiet-hour fields, marketing consent, and clinical-notification control.
- `Notification` with recipient ownership, event/template keys, payload, channel, lifecycle status, timestamps, and idempotency uniqueness by recipient/event/channel.
- `NotificationDeliveryAttempt` with provider, attempt number, provider reference, status, response metadata, and uniqueness per notification attempt.
- Provider-neutral delivery service with explicit in-app storage behavior and configurable Email/SMS/Push adapter boundaries. No credentials are hard-coded.
- Celery delivery task with retry backoff, a configurable maximum attempt count, idempotent terminal-state handling, and queued-dispatch task.
- Authenticated list/detail/read/preference endpoints under `/api/v1/notifications/`, all recipient-scoped at queryset and object lookup level.
- Account signal that creates default preferences and messaging signal that creates recipient-only new-message notifications.

## Verification

- `python3 manage.py makemigrations notifications` generated `notifications/migrations/0001_initial.py`.
- `python3 manage.py check` passed with no issues.
- `python3 manage.py test notifications --verbosity 1` passed: 3 tests.
- `python3 manage.py test --verbosity 1` passed: 3 tests currently present in the repository.
- Tests cover eager Celery delivery, delivery-attempt creation, notification idempotency, disabled-channel suppression, and cross-user IDOR protection.

## Production boundaries

The provider adapters intentionally remain configuration boundaries until real email/SMS/push credentials and vendor contracts are provisioned. The default local behavior does not send external messages. Production must configure a real broker/worker, provider adapters, verified sender identities, delivery webhooks if supported, rate limits, and operational alerting. Quiet-hour enforcement is represented in the preference model but requires product-approved policy before it should suppress clinical or emergency notifications.

## Next phase

Proceed to Phase 13 / Prompt 12: AI integration. AI must remain behind explicit provider interfaces, privacy filtering, auditability, timeout/fallback behavior, and clinical safety boundaries. Do not let notification delivery expose protected clinical payloads to unapproved providers.
