# Handoff 14 — API documentation and error finalization

## Scope

`docs/architecture/IMPLEMENTATION-TODO.md` Phase 14: "OpenAPI coverage, error envelope, HTML errors." A close audit found the core error-envelope infrastructure (`core/api/exceptions.py`, `core/views.py`, `templates/{400,403,404,500}.html`, `handler400/403/404/500` in `config/urls.py`) was already built in Phase 2 and working correctly — so this phase is narrower and more precise than a from-scratch build: close the two concrete, verifiable gaps that were actually open, and add the test coverage that was missing for behavior that already existed.

## Gap 1 — OpenAPI schema warnings (enum collisions)

`python manage.py spectacular --file schema.yaml --validate` was passing with 0 errors but 2 non-blocking warnings after Phase 13 (`StatusF5aEnum`/`StatusA65Enum`, auto-generated hash-suffixed names). Root cause, confirmed by reading every model with a `status`-shaped field: `ENUM_NAME_OVERRIDES` in `SPECTACULAR_SETTINGS` already resolved collisions for classes literally named `Status` in `community` (and the shared inline-tuple choices in `disease`/`feed`), but three more classes also literally named `Status` were added later without a matching override — `marketplace.ProductInquiry.Status`, `privacy.DataExportRequest.Status`, `privacy.DataDeletionRequest.Status`. Since drf-spectacular names enum components from the Python class name, these three (plus community's, already handled) all collided under the same bucket. Added three new override entries with their exact choice values (`MarketplaceInquiryStatusEnum`, `DataExportStatusEnum`, `DataDeletionStatusEnum`). No model changed — this is purely a schema-documentation fix, so no migration is needed.

## Gap 2 — error responses undocumented in the schema

The error *behavior* (JSON envelope for every 4xx/5xx) was already correct and consistent, but the OpenAPI schema itself never documented what an error response looks like — only success responses were described per-operation, matching AutoSchema's default. Added `core/api/schema.py`: an `ErrorEnvelope` component schema matching `core.api.exceptions.api_exception_handler`'s actual output shape, registered via a `POSTPROCESSING_HOOKS` entry (`add_common_error_responses`) that adds the 400/401/403/404/429/500 response documentation to every operation **that doesn't already define that status code** — it never overwrites an operation's existing, more specific response. This is the standard drf-spectacular pattern for global error documentation and touches no view code.

**Verified logically before relying on real Django**, since this sandbox still can't run `manage.py`: the hook function was executed directly in this sandbox against a synthetic OpenAPI `paths` dict (no Django needed — it's a pure dict-transforming function) and confirmed to (a) add missing status codes, (b) leave an existing `200` and a custom `404` completely untouched, (c) leave non-operation keys like a path-level `parameters` list untouched, (d) register the `ErrorEnvelope` component exactly once.

## Test coverage added

`core/tests/test_foundation.py` previously covered: health/readiness endpoints, a generic 404-under-`/api/`-returns-envelope check, and HTML-404-hides-internals. Added, all either exercising real HTTP behavior or the exact functions involved:

- Every HTML error handler (400/403/404/500) directly, confirming no traceback/path/secret leakage — not just 404.
- Every API error handler (400/403/404/500) directly, confirming the JSON envelope's `code` matches DRF's actual `default_code` for that exception type.
- A real unauthenticated request to an admin-only endpoint → 401 with envelope.
- A real authenticated-but-wrong-role request → 403 with envelope.
- A real method-not-allowed request (admin client, `DELETE` on a GET-only endpoint) → 405 with `code: "method_not_allowed"`.
- A real throttled request (temporarily overriding `DEFAULT_THROTTLE_RATES` to `1/day` and firing two requests) → second returns 429 with `code: "throttled"`.
- A direct unit test of `add_common_error_responses` (the same synthetic-dict check described above, made permanent).

## Verification

**Real verification, executed by the operator, surfaced two genuine issues — both fixed here:**

1. **A pre-existing migration/model drift, unrelated to this phase**, found because this was the first time `makemigrations --check` was run across the *whole* project rather than scoped to one app. `accounts.OneTimeToken` had a real, actively-used composite index (`accounts_otp_verification_idx`, on `user, purpose, expires_at, used_at`) created by an existing migration (`0002_onetimetoken_attempt_count.py`), but the model's `Meta.indexes` declaring it had gone missing from `accounts/models.py` at some point before this phase — I never touched that file in any of phases 12–14. Django's suggested fix was to *remove* the index, which would have deleted a real, useful index (confirmed against an actual query in `accounts/services.py`'s email-verification flow: `user.one_time_tokens.filter(purpose=..., used_at__isnull=True)`). Restored the missing `Meta.indexes` instead, matching the existing migration exactly — zero new migration needed, zero database change, just correcting the model to reflect what was already true.
2. **A real test bug**, not an application bug: `test_throttled_request_returns_standard_envelope` used `override_settings(REST_FRAMEWORK=...)` to change `DEFAULT_THROTTLE_RATES`, but DRF's `SimpleRateThrottle.THROTTLE_RATES` is bound from `api_settings` once at class-definition/import time — `override_settings` doesn't reach it. Fixed using the standard DRF-testing pattern: directly patch `AnonRateThrottle.rate`/`UserRateThrottle.rate` for the duration of the test, restored in a `finally` block.

```
python manage.py makemigrations --check
python -m pytest -q
python manage.py check
python manage.py spectacular --file schema.yaml --validate
```

Confirmed by the operator: `makemigrations --check` now reports no changes for `accounts` (after both the fix above and deleting the stray auto-generated `accounts/migrations/0003_remove_onetimetoken_accounts_otp_verification_idx.py` the operator's first run produced — that migration should never be applied). 70/71 tests passed on the first real run across the whole suite (the one throttle-test failure was the test bug above, now fixed); `manage.py check` passed cleanly.

## Not in scope for this phase

Per-endpoint OpenAPI tags/groupings for Swagger UI navigation were considered and deliberately not added — doing so broadly would mean touching dozens of existing view files across every app for a cosmetic benefit, which doesn't clear the "necessary" bar for editing already-working code under the do-no-harm rule. If Swagger UI organization becomes a real pain point, it's a clean, low-risk follow-up (tags are additive `@extend_schema(tags=[...])` calls, no behavior change).

## Next phase

Proceed to Phase 15: full audit and release certification (traceability matrix, adversarial tests, certification) — the final item in the ordered ledger.
