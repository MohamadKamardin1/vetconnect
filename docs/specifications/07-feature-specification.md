# DOCUMENT 07 — Feature Specification

| Feature ID | Feature | VetKonect evidence | Tanzania disposition | Priority |
|---|---|---|---|---|
| FTR-001 | Animal-care discovery platform | Homepage value proposition [1] | Preserve; localize | P0 |
| FTR-002 | Nearby veterinarian search | Homepage section and empty state [1] | PostGIS + admin hierarchy | P0 |
| FTR-003 | Professional/paraprofessional connection | Homepage CTA and privacy/terms [1] [3] [4] | VCT categories and scope | P0 |
| FTR-004 | Clinic discovery | Homepage and dev site [1] [6] | Verified facilities, hours, emergency | P0 |
| FTR-005 | Vendor discovery | Homepage and dev site [1] [6] | Local catalog, inquiry first | P1 |
| FTR-006 | Feed Calculator | Homepage/dev site [1] [6] | Versioned local formulas | P1 |
| FTR-007 | Disease Predictor | Homepage/dev site/privacy [1] [3] [6] | Decision support, not diagnosis | P0 |
| FTR-008 | Chat Forum | Homepage/footer [1] | Kiswahili moderation and low-data mode | P1 |
| FTR-009 | Blog/content | Public listing [7] | One Health/Tanzania editorial governance | P1 |
| FTR-010 | Mobile app/PWA | Homepage metric and privacy policy [1] [3] | PWA first; native later | P0 |
| FTR-011 | AI scribe/SOAP/guidance | VetifyPro [5] | Professional-only, human oversight | P2 |
| FTR-012 | Verification | Privacy/terms and VCT sources [3] [4] [11] [12] | VCT-backed workflow | P0 |
| FTR-013 | Payments | Terms says third-party gateway/service fee [4] | BoT-compliant abstraction | P1 |
| FTR-014 | Emergency routing | Original terms says no emergency replacement [4] | Add explicit local emergency discovery | P0 |
| FTR-015 | Disease surveillance | Blog/public-health themes [7] | Consent, aggregation, authority governance | P2 |

## Unknowns requiring confirmation

The exact search filters, account roles exposed in registration, messaging modality, appointment/order flows, formulas, disease dataset, notification channels, dashboard navigation, and admin interface remain **NOT VERIFIED**. The development team should not implement these as historical facts; it should implement the recommended contracts and label product decisions for owner approval.

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
