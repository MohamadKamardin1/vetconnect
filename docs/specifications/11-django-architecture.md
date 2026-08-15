# DOCUMENT 11 — Django Architecture

## Module boundaries

```text
apps/
  identity/        users, roles, sessions, consent
  profiles/        owner, professional, clinic, vendor projections
  verification/    submissions, review queue, VCT evidence
  locations/       admin hierarchy, PostGIS, geocoding
  animals/         animal records and health events
  discovery/       filters, ranking, saved profiles
  communications/  conversations, messages, attachments
  community/       forum, reports, moderation
  reviews/         interaction reviews and reputation
  tools_feed/      versioned feed rules and calculations
  tools_disease/  symptoms, rules, assessments, safety gates
  content/         blog, media, SEO
  payments/        intents, provider adapters, refunds, disputes
  notifications/  templates, preferences, delivery
  emergency/       urgency and routing
  ai/              provider abstraction, safety, audit
  analytics/       events and aggregates
  governance/      admin, audit, retention, exports
```

Use Django REST Framework serializers and ViewSets only for straightforward CRUD. Put cross-object rules in application services, such as `VerificationReviewService`, `NearbyDiscoveryService`, `DiseaseAssessmentService`, `PaymentOrchestrator`, and `AccountDeletionService`. Use explicit permission classes plus object-level checks. Use Celery for notifications, document scanning, geocoding, media processing, analytics aggregation, and retryable provider calls. Use Channels/Redis for messaging presence and delivery events; persist messages transactionally before emitting events.

## Security and operations

Use PostgreSQL with PostGIS, Redis, object storage, a CDN, a secrets manager, error tracking, centralized logs, health checks, migrations, and separate development/staging/production environments. Treat veterinary health data and professional documents as sensitive. Every admin action, verification decision, export, deletion, moderation action, payment state change, and AI output review is auditable.

## References

[1]: https://www.vetkonect.com/ — Vet Konect live homepage, accessed 2026-08-12.
[2]: https://www.vetkonect.com/about — Vet Konect About page, accessed 2026-08-12.
[3]: https://www.vetkonect.com/privacy — Vet Konect Privacy Policy, last updated 2026, accessed 2026-08-12.
[4]: https://www.vetkonect.com/terms-condition — Vet Konect User Policy & Terms of Service, last updated 2026, accessed 2026-08-12.
[5]: https://www.vetkonect.com/vetifypro — VetifyPro AI-powered clinical assistant page, accessed 2026-08-12.
[6]: https://dev.vetkonect.com/ — public development-site content, accessed 2026-08-12.
[7]: https://www.vetkonect.com/blog — Vet Konect blog listing, accessed 2026-08-12.
[8]: https://www.nbs.go.tz/statistics/topic/gis — Tanzania National Bureau of Statistics GIS/shapefile hierarchy, accessed 2026-08-12.
[9]: https://microdata.nbs.go.tz/index.php/catalog/49/related-materials — NBS 2022 census geodatabase metadata, accessed 2026-08-12.
[10]: https://www.zanzibarassembly.go.tz/storage/documents/acts/english/all/1674628539.pdf — Zanzibar Regional Administration Authority Act No. 1 of 1998.
[11]: https://www.vct.go.tz/ — Veterinary Council of Tanzania official site, accessed 2026-08-12.
[12]: https://www.vct.go.tz/pages/how-to-register — VCT registration/enrolment requirements, accessed 2026-08-12.
[13]: https://www.bot.go.tz/PaymentSystem — Bank of Tanzania payment-system overview, accessed 2026-08-12.
[14]: https://www.bot.go.tz/PaymentSystem/regulations — Bank of Tanzania payment laws and regulations, accessed 2026-08-12.
[15]: https://www.dlapiperdataprotection.com/?t=law&c=TZ — Tanzania data-protection legal overview, accessed 2026-08-12.
