# DOCUMENT 17 — Admin Specification

The public site does not expose an admin console; all admin capabilities below are **RECOMMENDED** and inferred from the observed product surface, legal claims, and operational needs.

## Admin modules

| Module | Functions |
|---|---|
| Identity | users, roles, sessions, suspension, deletion, export |
| Verification | vet/VPP/clinic/vendor queues, evidence, decisions, expiry, resubmission |
| Geography | import/version NBS and Zanzibar units, boundaries, aliases |
| Reference data | species, breeds, symptoms, diseases, feed rules, services |
| Discovery | ranking policy, public visibility, duplicate merge, report review |
| Community | posts, comments, reports, blocks, moderation actions, appeals |
| Reviews | fraud signals, removal requests, response policy |
| Content | blog CMS, authors, categories, SEO, translation review |
| Safety | emergency content, clinical disclaimers, controlled product policy |
| Payments | provider events, refunds, disputes, reconciliation |
| Notifications | templates, locale variants, delivery health, opt-outs |
| Analytics | funnel, geographic coverage, supply/demand, safety metrics |
| Security | audit logs, alerts, retention, processor access, incident response |

Every high-impact action requires role separation where practical, rationale, before/after values, actor, timestamp, request ID, and notification to affected users. Verification decisions must preserve document versions and reviewer notes. Moderation must support appeal and legal hold. Admin search should mask sensitive data by default and watermark exports.

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
