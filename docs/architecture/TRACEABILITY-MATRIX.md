# Traceability Matrix

Maps `docs/specifications/19-product-backlog.md` against what is actually implemented, app by app, so a reviewer can check any backlog line against real code and real tests rather than a phase-name claim.

## Phase 1 — MVP (P0)

| ID | Epic | Implementing app(s) | Key endpoints | Tests |
|---|---|---|---|---|
| BL-001 | Identity, phone/email verification, RBAC | `accounts` | `/api/v1/auth/register,login,verify-email,me` | `accounts/tests/test_auth.py` (9) |
| BL-002 | Tanzania/Zanzibar geography, manual location | `locations` | `/api/v1/locations/` | `locations/tests/test_locations.py` (1 — thin, see Findings) |
| BL-003 | VCT-oriented professional verification | `professionals` | `/api/v1/professionals/` | `professionals/tests/test_professionals.py` (4) |
| BL-004 | Nearby professional/clinic discovery | `discovery` | `/api/v1/discovery/` | `discovery/tests/test_discovery.py` (2) |
| BL-005 | Professional/clinic public profiles | `professionals` | `/api/v1/professionals/` | shared with BL-003 |
| BL-006 | Animal records | `animals` | `/api/v1/animals/` | `animals/tests/test_animals.py` (2) |
| BL-007 | Messaging with retry queue | `messaging` | `/api/v1/messaging/` (Channels) | `messaging/tests/test_messaging.py` (2) |
| BL-008 | Emergency routing | `disease` (urgency/referral) + `professionals`/`discovery` (nearby availability) | `/api/v1/disease/assessments/` | `disease/tests/` (2) |
| BL-009 | Kiswahili/English i18n and PWA shell | `frontend/` (separate React/TS project, not part of the Django backend) | n/a (frontend build) | frontend's own `todo.md` checklist — not covered by this backend test suite |
| BL-010 | Security/privacy baseline (consent, export/delete, audit, rate limiting, private storage) | `privacy`, `audit`, `core` (throttling, error envelope) | `/api/v1/privacy/`, `/api/v1/audit/` | `privacy/tests/` (4), `audit/tests/` (3), `core/tests/test_foundation.py` (13) |

## Phase 2 — Growth (P1)

| Item | Implementing app(s) | Tests |
|---|---|---|
| Vendor profiles/catalog/inquiries | `marketplace` | `marketplace/tests/test_marketplace.py` (6 — added in Phase 15; app had **zero** tests before this phase, see Findings) |
| Clinic staff management | `professionals` (`Clinic`, staff relations) | covered under BL-003/005 |
| Reviews | `discovery` (ratings/reviews) | `discovery/tests/` |
| Forum moderation | `community` | `community/tests/test_community.py` (2) |
| Notifications | `notifications` | `notifications/tests/` (3) |
| Blog CMS | **Not implemented.** No `blog`/CMS app exists. | — |
| Payments abstraction | `billing` (ClickPesa badge subscriptions specifically; general payments abstraction beyond badges not built) | `billing/tests/test_billing.py` (5) |
| Appointments | **Not implemented.** No scheduling/appointment app or model exists anywhere in the codebase. | — |
| Saved profiles | **Not implemented.** No "favorites"/"saved" model exists. | — |
| Feed calculator | `feed` | `feed/tests/` (2) |
| Analytics | **Not implemented.** No analytics/reporting app exists. | — |

## Phase 3 — Advanced (P2/P3)

| Item | Implementing app(s) | Tests |
|---|---|---|
| Disease decision support | `disease` | `disease/tests/` (2) |
| Disease surveillance (population-level) | **Not implemented.** `disease` only covers per-animal decision support, not aggregate/regional surveillance. | — |
| AI scribe/SOAP, clinical guidance, client summaries, voice | **Not implemented.** `ai` app covers disease-assist/feed-assist narrative wrapping only (see `HANDOFF-12-AI-INTEGRATION.md`, "Not implemented in this phase"). | — |
| Regional dashboards | **Not implemented.** | — |
| Advanced marketplace settlement | **Not implemented.** `marketplace` has inquiries/inventory; no payment settlement between vendor and platform. | — |
| Interoperability | **Not implemented.** No external system integration (e.g. national livestock registries) exists. | — |
| Model evaluation | **Not implemented.** No evaluation harness for `ai` app outputs exists beyond the unit tests confirming fallback/redaction behavior. | — |

## Cross-cutting (spec 15 — security and privacy)

| Requirement | Implementing app(s) | Tests |
|---|---|---|
| Every high-impact action carries rationale, before/after values, actor, timestamp, request ID | `audit` (`AuditLogEntry`, `record_audit_event`) | `audit/tests/test_audit.py` |
| Access/correction/deletion/export workflows | `privacy` | `privacy/tests/test_privacy.py` |
| Rate limiting | `core` (`DEFAULT_THROTTLE_CLASSES`, `DEFAULT_THROTTLE_RATES`) | `core/tests/test_foundation.py::test_throttled_request_returns_standard_envelope` |
| Consistent error envelope, no internal leakage | `core/api/exceptions.py`, `core/views.py` | `core/tests/test_foundation.py` (9 dedicated tests, added in Phase 14) |

## Admin specification (spec 17)

Phase 13 built the shared primitives (`audit`, `privacy`) every module-specific admin console would use. The module-specific consoles themselves — verification queue UI, geography import tooling, moderation console, content CMS, payments reconciliation, analytics dashboards — are **not implemented**. See `HANDOFF-13-ADMIN-AUDIT-SECURITY.md`, "Not in scope for this phase."

## Findings from this audit

1. **`marketplace` had zero tests before this phase.** Every other backend app had at least one test file; `marketplace/tests/__init__.py` was the only file present. Fixed in this phase — see `HANDOFF-15-RELEASE-CERTIFICATION.md`.
2. **A real bug found and fixed in `marketplace`:** `VendorProductWriteSerializer` (used for both listing and creating a vendor's own products) omitted the `id` field entirely. A vendor listing their own products via `GET /api/v1/marketplace/vendor/products/` could not obtain a product's ID from the response — making it impossible to then call `PATCH .../inventory/` on that product without a separate lookup. Fixed by adding `id`/`created_at` as read-only output fields; no write behavior changed.
3. **`locations` has only 1 test** for an entire geography app (regions/districts/wards/PostGIS boundaries). Not expanded in this phase — flagged here rather than silently left off the record. A full audit of `locations`' edge cases (boundary precision, ward-level privacy) is recommended before next major release.
4. Several Phase 2/3 backlog items (blog CMS, appointments, saved profiles, analytics, disease surveillance, AI scribe, advanced settlement, interoperability, model evaluation) are **not implemented anywhere in the codebase** — not partially built, not stubbed. This matrix exists specifically so that isn't discovered by surprise later.
5. This audit reviewed every app's models/views/serializers/urls **that this matrix references**. It is not a claim that every line of every app was re-read; `locations`, `messaging`, `community`, `discovery`, `professionals`, `notifications`, `billing` were read only as deeply as needed to confirm their existing test files matched real endpoints, not re-audited for new bugs the way `marketplace` was. That deeper pass is the natural next increment if more audit time is available.
