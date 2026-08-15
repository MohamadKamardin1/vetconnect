# DOCUMENT 19 — Product Backlog

## Phase 1 — MVP

| ID | Epic | Priority | Complexity | Definition of done |
|---|---|---:|---:|---|
| BL-001 | Identity, phone/email verification, RBAC | P0 | M | Secure registration and login for owner, professional, clinic, vendor |
| BL-002 | Tanzania/Zanzibar geography and manual location | P0 | M | Versioned hierarchy and PostGIS boundaries imported from authoritative sources |
| BL-003 | VCT-oriented professional verification | P0 | L | Document queue, review, badge, expiry, resubmission |
| BL-004 | Nearby professional/clinic discovery | P0 | L | Verified nearby-first search with no-results recovery |
| BL-005 | Professional/clinic public profiles | P0 | M | Services, species, location precision, hours, emergency status |
| BL-006 | Animal records | P0 | M | Owner CRUD, consented sharing, vaccination/history fields |
| BL-007 | Messaging with retry queue | P0 | L | Authenticated conversation, delivery states, attachments scanned |
| BL-008 | Emergency routing | P0 | M | Urgency gate, call/SMS/WhatsApp options, nearby availability |
| BL-009 | Kiswahili/English i18n and PWA shell | P0 | M | Localized core flows and offline-safe public/reference content |
| BL-010 | Security/privacy baseline | P0 | L | Consent, export/delete, audit, rate limiting, private storage |

## Phase 2 — Growth

Add vendor profiles/catalog/inquiries, clinic staff management, reviews, forum moderation, notifications, blog CMS, payments abstraction, appointments, saved profiles, feed calculator, and analytics. The original site publicly signals vendor, forum, blog, and calculator capabilities [1] [6] [7], but their private workflow details remain to be confirmed.

## Phase 3 — Advanced

Add disease decision support, disease surveillance, AI scribe/SOAP, clinical guidance, client summaries, voice, regional dashboards, advanced marketplace settlement, interoperability, and model evaluation. Gate all clinical AI behind professional oversight and documented validation.

## Priority reasoning

P0 is required for a trustworthy Tanzania service: identity, location, verification, discovery, communication, emergency safety, privacy, and low-connectivity access. P1 expands utility and monetization after supply quality. P2 adds advanced clinical/workflow capability. P3 includes research-heavy or scale-dependent enhancements.

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
