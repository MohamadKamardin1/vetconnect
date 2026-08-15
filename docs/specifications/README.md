# Tanzania + Zanzibar Veterinary Digital Platform — Documentation Package

**Research basis.** This package reverse-engineers the publicly observable VetKonect product and translates it into a build-ready specification for a distinct Tanzania/Zanzibar platform. It does not reproduce VetKonect trademarks, logos, copyrighted copy, proprietary images, or branding.

**Important evidence discipline.** Every statement is classified as **CONFIRMED**, **PARTIALLY CONFIRMED**, **INFERRED**, **RECOMMENDED**, or **NOT VERIFIED**. The live homepage, public About, privacy, terms, VetifyPro, development site, and blog were accessible through public extraction on 2026-08-12. Direct access to dashboard, registration, and calculator routes was not reliably available; those workflows are therefore not claimed as observed. The package deliberately distinguishes product evidence from engineering recommendations.

## Deliverables

| Document | File | Purpose |
|---|---|---|
| 01 | `01-executive-product-analysis.md` | Executive product analysis and opportunity |
| 02 | `02-complete-sitemap.md` | Observed and proposed route tree |
| 03 | `03-user-roles-and-permissions.md` | Personas, RBAC, and permission matrix |
| 04 | `04-screen-specification.md` | Master screen inventory and page contracts |
| 05 | `05-form-specification.md` | Form and validation inventory |
| 06 | `06-workflow-specification.md` | End-to-end workflows |
| 07 | `07-feature-specification.md` | Feature inventory with evidence status |
| 08 | `08-ux-ui-specification.md` | Design-system and responsive UX |
| 09 | `09-data-model.md` | Conceptual PostgreSQL/PostGIS model |
| 10 | `10-api-specification.md` | Recommended REST/service API inventory |
| 11 | `11-django-architecture.md` | Backend module architecture |
| 12 | `12-nextjs-architecture.md` | Frontend architecture |
| 13 | `13-lit-architecture.md` | Focused Web Components strategy |
| 14 | `14-tanzania-zanzibar-localization.md` | Geography, language, phone, veterinary, connectivity |
| 15 | `15-security-and-privacy.md` | Security, privacy, and compliance requirements |
| 16 | `16-ai-specification.md` | AI safety and VetifyPro-derived capability design |
| 17 | `17-admin-specification.md` | Administration, verification, moderation |
| 18 | `18-qa-specification.md` | Acceptance criteria, test cases, edge/error states |
| 19 | `19-product-backlog.md` | MVP/Growth/Advanced prioritized backlog |
| 20 | `20-master-requirements.md` | Consolidated uniquely identified requirements |

## Research limitations

The public site identifies a broad product surface: professional, clinic, and vendor discovery; nearby-veterinarian search; Feed Calculator; Disease Predictor; Chat Forum; blog/content; mobile app presence; privacy and terms; and VetifyPro AI clinical workflows. Public dashboard and authentication flows could not be completed in this run because the site intermittently returned `ERR_CONNECTION_CLOSED`, and no research account was created. The implementation team must run a credentialed discovery pass before treating private screens, exact form fields, formulas, or backend behavior as confirmed.

## Recommended next action

Use Document 20 as the source-of-truth baseline, Document 19 to sequence delivery, and schedule a second evidence pass with a safe research account. The second pass should capture screenshots, DOM routes, validation messages, network contracts, and all authenticated role dashboards.

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
