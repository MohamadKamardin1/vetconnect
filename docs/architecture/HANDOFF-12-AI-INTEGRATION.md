# Handoff 12 — AI Integration

## Scope

Prompt 12 is complete for the AI provider-boundary foundation described in `docs/specifications/16-ai-specification.md`. It introduces a standalone `ai` app that wraps two already-complete deterministic engines (`disease.services.assess_disease`, `feed.services.calculate_feed`) with an optional, auditable, privacy-filtered AI narrative layer. Neither `disease` nor `feed` was modified: this phase is strictly additive, satisfying the do-no-harm/backward-compatibility constraint.

## Implemented

- `AIProviderConfig` — DB-configured provider record (key, display name, model name/version, enabled flag, timeout), mirroring the existing `FeedRule`/`DiseaseRule` versioned-config pattern rather than hard-coding provider identity.
- `AIFeatureConfig` — per-feature enable flag, human-review requirement, linked provider, and an explicit **allowlist** of field names (`allowed_context_fields`) permitted to leave the process boundary for that feature.
- `AIInteraction` — the audit record: user, feature key, provider key/model version, SHA-256 hash of the redacted payload, the redacted payload itself (never the raw request), output, status, latency, and human-review state. Cross-user reads are queryset-scoped exactly like every other audit-bearing model in the repository (`NotificationDeliveryAttempt`, `AccessLog`, etc.).
- `ai/services.py` — the provider abstraction:
  - `BaseAIProvider` / `NoopProvider` (no adapter configured — matches the notifications `noop` pattern) / `ConsoleProvider` (offline, deterministic stand-in for local/dev verification; makes no outbound call).
  - `redact_context()` — allowlist-only redaction. Nothing outside `AIFeatureConfig.allowed_context_fields` is ever included in what is hashed, logged, or handed to a provider. Free-text fields (e.g. `location`) are excluded by omission from the allowlist, not by pattern-matching.
  - `invoke_ai_feature()` — always computes the deterministic result **locally first**, independent of provider availability. If the feature is disabled → `SUPPRESSED`. If no provider is configured/enabled, or the provider call raises → `FALLBACK`, deterministic result returned unchanged. On success → `COMPLETED`, deterministic fields unchanged, only a non-authoritative `ai_narrative` string appended. A fixed non-diagnostic disclaimer is always attached.
  - Human review: `AIFeatureConfig.requires_human_review_on_urgent` forces `AIInteraction.human_review_status = PENDING` whenever the caller marks the request urgent (wired for disease `EMERGENCY` urgency).
- API (`/api/v1/ai/`): `POST disease-assist/`, `POST feed-assist/` (both `IsAuthenticated`, wrap the existing engines), `GET interactions/` (authenticated, user-scoped audit read).
- Admin registration for provider/feature configuration and read-only interaction review, matching the `billing` app's admin pattern.
- Wiring: `ai` appended to `INSTALLED_APPS`; one new `include()` line in `config/urls.py`. No existing route, model, or service function was edited.

## Safety boundaries enforced

- The deterministic engines' outputs (`possible_conditions`, `urgency`, `referral_required`, `daily_feed_kg`, etc.) are **never** altered by AI involvement — the AI layer can only append a narrative field.
- No free-text or identifying field (owner identity, raw location text, notes) is sent to a provider unless explicitly allowlisted per feature; the shipped `DISEASE_ASSIST`/`FEED_ASSIST` configs used in tests intentionally exclude `location`.
- Every AI-assisted request produces an `AIInteraction` audit record, whether it completes, falls back, fails, or is suppressed.
- A provider exception is caught and degrades to `FALLBACK`, never a 500 and never a lost deterministic result.
- Emergency/high-urgency disease outputs are always flagged for human review; no feature is described as diagnostic anywhere in the response payload (fixed disclaimer is always attached).

## Verification

- `python3 -m py_compile` passed for every new/modified file (`ai/*`, `config/urls.py`, `config/settings/base.py`).
- `ai/migrations/0001_initial.py` was **hand-authored** in this sandbox and manually cross-checked field-for-field against `ai/models.py` (types, `on_delete`, `related_name`, choices, defaults, index names match exactly).
- `ai/tests/test_ai.py` (7 tests) was written to cover: feature-disabled suppression, no-provider fallback, redaction (allowlisted fields only, free text never present in the stored payload), successful completion with the console provider, emergency escalation to pending human review, feed-assist result integrity under AI wrapping, cross-user audit isolation (IDOR), and unauthenticated rejection.

**Real verification — completed and confirmed by the operator:**

- `python manage.py makemigrations ai --check` → "No changes detected in app 'ai'" — the hand-authored migration matches `ai/models.py` exactly.
- `python manage.py check` → passed, 0 issues.
- `python manage.py spectacular --file schema.yaml --validate` → 0 errors, 2 warnings (non-blocking `status` field enum-name collisions across unrelated apps' choice sets — the same pre-existing, documented class of warning noted in Phases 7 and 11; not introduced by this phase). Confirmed after fixing `responses={200: dict}` → `responses={200: OpenApiTypes.OBJECT}` on the two `APIView`-based endpoints, which drf-spectacular cannot resolve a bare `dict` type for.
- `python -m pytest ai -q` → 7/7 passed, after one test fix: `test_ai_interactions_are_user_scoped` originally asserted a bare list length; the project's global `DEFAULT_PAGINATION_CLASS` (`PageNumberPagination`, `config/settings/base.py`) wraps list responses in `{count, next, previous, results}`, so the assertion was corrected to check `response.data["count"]`. This was a test-authoring bug, not an application defect — the cross-user scoping itself was already correct (`count: 0` for the other user).

Environment note for future phases: the operator's first `python -m venv .venv` silently produced an empty `.venv/bin/` (no `python` binary) while an unrelated venv from a different project remained active in the same shell, making early diagnostics misleading (`ModuleNotFoundError` for different packages on each run, `check` passing while `pytest`/`spectacular` failed). Recreating the venv from a clean shell (`deactivate` first, confirm `$VIRTUAL_ENV` is empty, then `python3 -m venv .venv`) resolved it. Verified working versions: Python 3.14.6, Django 5.2.17, djangorestframework 3.18.0, daphne 4.2.3, drf-spectacular 0.30.0 — all newer than the ranges most recently exercised in Phase 2's foundation verification (Django 5.2.x vs the `<6.0` ceiling), and everything in this phase is compatible.

## Production boundaries

`NoopProvider`/`ConsoleProvider` are the only adapters implemented; a real model provider (with its own SDK, credentials, and rate limits) is a deployment-configuration boundary, added by implementing `BaseAIProvider` and registering it in `PROVIDER_REGISTRY` — no other code changes required. Clinical scribe, clinical guidance, client-summary, and forum-safety AI features from the specification table are **not implemented** in this phase; only disease-assist and feed-assist narrative wrapping is in scope, matching the two features that already have a deterministic engine to wrap safely.

## Next phase

Phase 12 is now verified COMPLETE (see `docs/architecture/COMPLETION-MEMORY.md`). Proceed to Phase 13 / Prompt 13: Admin, audit, security hardening.
