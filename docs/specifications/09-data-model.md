# DOCUMENT 09 — Conceptual Data Model

## Entity classification

| Entity | Status | Key fields |
|---|---|---|
| User, Role, UserRole | RECOMMENDED/strongly inferred | id, phone, email, status, locale, consent, timestamps |
| PersonProfile | RECOMMENDED | name, avatar, bio, privacy settings |
| ProfessionalProfile | Confirmed concept / schema recommended | category, VCT identifier, scope, specialties, species, service radius, verification |
| Clinic, ClinicStaff, ClinicService | Confirmed concept / schema recommended | facility, address, point, hours, emergency, services |
| Vendor, Product, Category, Inventory | Confirmed concept / vendor workflow not verified | seller, SKU, price, stock, compliance, expiry |
| Animal, Species, Breed, AnimalEvent | Privacy-confirmed animal data [3] | owner, species, breed, sex, age, weight, purpose, health |
| Location, AdministrativeUnit, LocationBoundary | Recommended from NBS/Zanzibar sources | branch, level, code, parent, geometry |
| Conversation, Participant, Message, Attachment | Recommended | participants, body, delivery, moderation, encryption metadata |
| ForumPost, Comment, Reaction, Report | Confirmed forum concept / details not verified | author, content, thread, status |
| Disease, Symptom, DiseaseRule, Prediction | Predictor confirmed; data model recommended | version, species, evidence, urgency, disclaimer |
| FeedRule, FeedCalculation | Calculator confirmed; formulas not verified | ruleset version, inputs, result, assumptions |
| Review, Verification, Document, AuditLog | Reviews/verification partly evidenced | target, author, status, reviewer, evidence |
| Notification, NotificationPreference | Notifications stated in policy [3] | channel, template, delivery, locale |
| Order, Payment, Refund, Dispute | Payments/service fee stated [4] | provider ref, state machine, amount, currency |
| BlogPost, Tag, MediaAsset | Blog confirmed [7] | slug, author, content, publication, SEO |

## Relationships

A User has many Roles and one or more Profiles. A Farmer owns many Animals. A Professional belongs to zero or more Clinics through ClinicStaff. A Professional has one Verification record per credential version. A Conversation has Participants and Messages. A Review references a completed interaction, not merely a profile view. A Prediction references an input snapshot and rules/model version. An AdministrativeUnit has a parent and a PostGIS boundary; a profile or animal location may reference an administrative unit and optionally a point with privacy precision.

## PostgreSQL/PostGIS requirements

Use UUID primary keys, UTC timestamps, soft-delete only where legally appropriate, immutable audit events, `geography(Point,4326)` for nearby queries, GIST indexes, and versioned reference data. Store location precision separately from exact coordinates. Separate personally identifying data from public profile projections. Encrypt sensitive documents at rest; use object storage references and signed URLs rather than public buckets. Maintain provenance for disease/feed content and AI outputs.

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
