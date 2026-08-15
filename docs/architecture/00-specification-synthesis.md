# VetKonnect Tanzania/Zanzibar — Specification Synthesis

## Scope and evidence status

This synthesis is based on the 22 reviewed specification files copied into `docs/specifications/` and the ordered backend prompt series in `pasted_content_2.txt`. The backend is a greenfield Django/DRF/PostgreSQL/PostGIS/Redis/Celery/Channels service. Frontend documents are treated as API-shape context only.

The repository audit found no existing Django project, `manage.py`, `requirements.txt`, `pyproject.toml`, Docker configuration, migrations, CI configuration, or domain code. Python 3.12.3 is available. PostgreSQL, Redis, and Docker CLIs are not installed in the current sandbox, so local infrastructure must be provisioned through the project container configuration or an equivalent external environment before readiness can be claimed.

## Canonical roles

| Canonical role | Source aliases / interpretation |
|---|---|
| `OWNER` | Pet owner / animal owner |
| `FARMER` | Livestock farmer |
| `VETERINARIAN` | Registered veterinarian / veterinary specialist |
| `PARAPROFESSIONAL` | Veterinary paraprofessional / VPP |
| `CLINIC_OWNER` | Clinic/facility owner or authorized representative |
| `CLINIC_STAFF` | Clinic staff member with scoped membership role |
| `VENDOR` | Veterinary shop/vendor |
| `MODERATOR` | Community/content moderator |
| `CONTENT_MANAGER` | Official blog/content manager |
| `SUPPORT_OPERATOR` | Operations/support staff |
| `ADMINISTRATOR` | Platform administrator |

A user may have multiple roles. Organization membership is separate from a user's global role, and clinic staff permissions are object-scoped.

## Canonical Django apps

| App | Responsibility |
|---|---|
| `core` | UUID/timestamp primitives, shared exceptions, health, utilities, base API behavior |
| `accounts` | Custom user, roles, sessions/tokens, verification of contact details, account state |
| `locations` | Mainland/Zanzibar hierarchy, PostGIS locations, privacy precision, seed commands |
| `reference_data` | Species, breeds, symptoms, specialties, diseases, service categories, versioned reference tables |
| `professionals` | Veterinarian/paraprofessional profiles, expertise, services, availability |
| `clinics` | Facilities, clinic staff memberships, hours, emergency status |
| `verification` | Generic KYC/KYB/credential submissions, documents, review state machine |
| `animals` | Animal identity, ownership, health/vaccination/treatment records, access grants |
| `discovery` | Unified public search, filters, pagination, ranking, saved profiles |
| `reviews` | Interaction-linked reviews, ratings, moderation hooks, aggregates |
| `vendors` | Vendor profile, verification linkage, inquiry surface |
| `products` | Product catalog, categories, media, stock integrity |
| `messaging` | Conversations, participants, messages, read/delivery state, WebSockets |
| `webhooks` | HMAC/signature validation, idempotency, dead-letter processing |
| `community` | Forum posts, comments, tags, blocks, reports, moderation |
| `content` | Official blog/editorial content distinct from forum UGC |
| `feed` | Versioned feed formulas and calculation history |
| `disease` | Disease/symptom deterministic decision-support layer and service interface |
| `notifications` | In-app notifications, preferences, delivery logs, provider adapters |
| `ai` | Provider abstraction, clinical AI audit/privacy boundary, usage limits |
| `payments` | Provider-agnostic payment intents/settlement only where specification confirms scope |
| `audit` | Append-only audit events and sensitive mutation tracking |
| `admin_api` | Unified administrative APIs across prior app capabilities |
| `api` | URL aggregation, serializers/view conventions, OpenAPI and error envelope |

## Conflict resolutions

| Conflict | Resolution |
|---|---|
| `ROLE-CLINIC` and `ROLE-CLINIC_STAFF` are both implied | Use `CLINIC_OWNER`/organization ownership plus scoped `CLINIC_STAFF` memberships. A clinic is not a shared user account. |
| Vendor commerce scope is broader in the data model than the backlog | Implement vendor/product/catalog/inquiry/stock first. Orders and payments remain feature-flagged until a requirement explicitly confirms them. |
| Original public terms refer to Nigeria/Paystack while this product is Tanzania/Zanzibar | Preserve only the product pattern, not the provider or legal text. Use provider-agnostic adapters and Bank of Tanzania/legal review. |
| Disease “prediction” wording can imply diagnosis | API and serializers use decision-support language, mandatory disclaimer, urgency, and referral fields. No certainty claim is allowed. |
| Exact formulas and disease confidence logic are absent | Implement configuration-driven/domain interfaces with explicit missing-configuration states. No invented constants. |
| Location hierarchy uses “ward/shehia” | Model jurisdiction-aware administrative units so Mainland wards and Zanzibar shehias are represented without flattening them. |
| Prompt 01 says infrastructure only; later prompts require shared reference data | Foundation creates only abstract primitives. `reference_data` is introduced when the first domain requires species. |

## Implied requirements

The prompt series requires state machines for account, verification, moderation, payment/order if enabled, notification delivery, webhook processing, and data export/deletion. It also requires idempotency for mutations and webhooks, object-level permissions, audit provenance, safe file storage, provider mocks, feature flags for AI fallback, and a clean fresh-database migration path. These are cross-cutting requirements and must not be reimplemented separately in each domain app.

## Duplicate requirements to implement once

RBAC/object authorization is specified in documents 03, 09, 15, 17, and 20 and belongs in `accounts` plus reusable permission classes. Verification appears in documents 03, 07, 09, 15, 17, and prompts 04/07 and belongs in `verification`. Location privacy and nearby search appear in documents 09, 14, 15, and prompts 03/06 and belong in `locations` plus reusable discovery query utilities. Audit logging appears in documents 09, 15, 17, and prompts 05/08/13 and belongs in `audit`. Notifications are cross-cutting and belong only in `notifications`, consuming domain events.

## App dependency graph

```text
core → accounts → locations → reference_data
accounts + locations + reference_data → professionals → clinics → verification
accounts + reference_data → animals
locations + professionals + clinics + vendors → discovery
animals + professionals + clinics → reviews
verification + locations → vendors → products
accounts + animals + professionals → messaging → webhooks
accounts → community → content
reference_data + animals → feed + disease
all domain apps → notifications → provider adapters
animals + disease + professionals → ai
all domain/admin mutations → audit
all apps → api + admin_api
```

## Cross-cutting ownership rules

`core` owns the error envelope and base primitives. `accounts` owns authentication and role authorization. `verification` owns credential/KYC workflows. `audit` owns append-only audit recording. `notifications` owns delivery and preferences. `webhooks` owns inbound event authenticity/idempotency. `api` owns versioning, OpenAPI, pagination conventions, and global exception mapping. Domain apps emit typed events; they do not create duplicate notification or audit implementations.

## External sanity-check note

A future external competitive scan may identify capabilities such as appointment scheduling, teleconsultation, offline-first workflows, livestock finance, vaccination reminders, and supply-chain traceability. These are **Potential Gaps — Not In Scope Unless Confirmed**. The local specification remains the sole source of truth for implementation scope.

## Infrastructure constraints observed

The current sandbox has Python but does not have PostgreSQL, Redis, or Docker command-line tools installed. The project will include Docker Compose and native setup instructions, and tests will use SQLite-compatible fallbacks only where PostGIS-specific behavior can be isolated; geospatial and readiness verification must also be run in a real PostGIS/Redis environment before production certification.


## Competitive sanity-check evidence (notes only; not added scope)

A brief external scan found comparable platforms with capabilities that validate the specification and identify potential gaps. VetNOW Kenya describes mobile-based support connecting livestock farmers, veterinarians, and veterinary paraprofessionals, with disease awareness, preventive care, diagnostics, record keeping, regulatory compliance, real-time interaction, and transaction analytics [16]. GALVmed describes a telehealth/e-commerce concept with clinical-sign recognition, prescriptions, product ordering, laboratory case submission, product barcode/licensing checks, disease surveillance, and demand aggregation; these are potential gaps, not silently added scope [17]. Shurokkha describes structured livestock case capture using photos/audio, veterinarian consultation, digital prescriptions, SMS summaries, and treatment records [18]. VetAfrica describes differential disease support, disease surveillance, data sharing, and a dashboard for live surveillance data [19].

These findings reinforce the value of: structured case intake, media evidence, SMS fallback, treatment history, disease surveillance governance, regulatory/compliance metadata, and operations analytics. They remain **Potential Gaps — Not In Scope Unless Confirmed** because the local specification does not unambiguously require every capability.

[16]: https://www.vetnow.com/in-kenya — VetNOW Telehealth Platform Live in Kenya.
[17]: https://www.galvmed.org/tag/telehealth-platforms/ — GALVmed telehealth and e-commerce platform overview.
[18]: https://www.isdb.org/sti/success-stories/shurokkha-livestock-consultation-with-vets — IsDB Shurokkha livestock consultation case study.
[19]: https://www.engineeringforchange.org/solutions/product/vetafrica/ — Engineering for Change VetAfrica profile.
