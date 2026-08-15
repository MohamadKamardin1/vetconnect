# DOCUMENT 14 — Tanzania/Zanzibar Localization Specification

## Geography

NBS describes a five-level geodatabase: region, district, ward/shehia, villages/mitaa, and enumeration areas [8] [9]. Zanzibar's Regional Administration Authority Act describes division into regions, districts, and other administrative areas, and states that districts are subdivided into shehias [10]. Therefore model an extensible `AdministrativeUnit` table with `jurisdiction = MAINLAND | ZANZIBAR`, `level`, `parent_id`, official code/name, geometry, effective dates, and source version. Do not flatten Zanzibar into Mainland regions or invent a single “state” level.

Recommended user hierarchy: Country → jurisdiction branch → region → district → ward or shehia → village/mtaa/area. For Unguja and Pemba, store island as a geographic grouping, not as a substitute for official administrative units; validate current names/codes against authoritative datasets before production import.

## Phone and communications

Use E.164 canonical storage with `+255`; accept common local-format input only as a convenience and normalize before uniqueness checks. Reject ambiguous or impossible lengths after confirming the current TCRA numbering plan. Store channel preferences for SMS, voice, WhatsApp deep-link, email, and push. Never assume WhatsApp delivery is guaranteed; offer SMS/voice fallback for critical alerts.

## Language

English and Kiswahili are first-class locales. Use translation keys for every label, validation message, notification, safety disclaimer, and transactional template. Default language should be selected by user/device and confirmed during onboarding, not assumed from geography. Editorial content requires human review; AI translation may draft but must not publish clinical or legal content without review.

## Veterinary domain

Support companion species and livestock categories with a reference-data system rather than hard-coded enums: dogs, cats, birds, rabbits, cattle, goats, sheep, poultry, pigs, fish, and additional locally relevant species. Capture species, breed/local type, sex, age, weight, production purpose, location, health status, vaccination, and treatment history. VCT publicly identifies registration of veterinarians, veterinary specialists, veterinary practice facilities, and enrolment/listing of veterinary paraprofessionals [11] [12]; onboarding should map to those categories and preserve evidence without inventing credentials.

## Low-connectivity and mobile-first requirements

Target slow 3G, high latency, intermittent service, and rural coverage. Use text-first pages, compressed images, lazy loading, cached administrative/species reference data, resumable uploads, retry queues with idempotency keys, and offline-safe drafts. Never cache unencrypted sensitive clinical data in a shared device by default. Emergency actions should show phone/voice options even when the app cannot complete a network request.

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
