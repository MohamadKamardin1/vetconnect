# Ordered Backend Implementation Todo

This is the source-of-truth execution ledger. A phase is marked complete only after its code, tests, documentation, verification commands, and handoff are recorded.

| Phase | Prompt | Scope | Status |
|---:|---|---|---|
| 1 | Specification ingestion, competitive sanity check, foundation | Audit, synthesis, repository setup, infrastructure skeleton | **COMPLETE** |
| 2 | Identity, users, authentication, RBAC | Custom user, roles, auth, object permissions | **COMPLETE** |
| 3 | Location and geospatial foundation | Tanzania/Zanzibar hierarchy, PostGIS, privacy | **COMPLETE** |
| 4 | Professionals, clinics, KYC verification | Profiles, clinics, staff, credential workflow | **COMPLETE** |
| 5 | Animals and veterinary records | Ownership, health records, access grants | **COMPLETE** |
| 6 | Search, discovery, services, reviews | Filters, nearby search, ratings, moderation | **COMPLETE** |
| 7 | Vendors, products, inventory | Scoped commerce/catalog/inquiry features | **COMPLETE** |
| 8 | Messaging, realtime, webhooks | Channels, isolation, HMAC/idempotency | **COMPLETE** |
| 9 | Community, content, moderation | Forum, blog, reporting, blocks | **COMPLETE** |
| 10 | Feed and disease decision support | Deterministic engines, disclaimers, referral | **COMPLETE** |
| 11 | Notifications and background tasks | Celery, preferences, provider adapters | **COMPLETE** |
| 12 | AI integration | Provider boundary, privacy filtering, fallback | **NEXT** |
| 13 | Admin, audit, security hardening | Admin APIs, audit, export/deletion, operations | TODO |
| 14 | API documentation and error finalization | OpenAPI coverage, error envelope, HTML errors | TODO |
| 15 | Full audit and release certification | Traceability matrix, adversarial tests, certification | TODO |

## Rules

The phases execute strictly in order. Each phase creates a `HANDOFF-XX.md`, updates `COMPLETION-MEMORY.md`, and leaves a reproducible test/verification record. No later phase may silently bypass an unresolved security-critical decision from an earlier handoff.


## Post-Prompt extension — Paid veterinarian verification badges

The paid badge extension is complete independently of the ordered Prompt 01–15 sequence. It adds KYC-gated weekly/monthly/yearly badge plans, subscription lifecycle, ClickPesa USSD-PUSH initiation, signed webhook reconciliation, idempotency, expiry scheduling, APIs, notifications, and adversarial tests. Handoff: `docs/architecture/HANDOFF-BILLING-CLICKPESA-BADGES.md`.

Production prerequisites remain: configure approved plan prices, real ClickPesa credentials and checksum key, application webhooks, TLS, PostgreSQL/PostGIS, Redis, Celery workers/Beat, monitoring, and merchant test transactions.
