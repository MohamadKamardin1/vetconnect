# DOCUMENT 04 — Screen Specification

## Master screen inventory

| ID | Screen | Role | Auth | Priority | Status |
|---|---|---|---|---|---|
| SCR-001 | Homepage | Public | No | P0 | Confirmed |
| SCR-002 | About | Public | No | P1 | Confirmed |
| SCR-003 | Privacy | Public | No | P0 | Confirmed |
| SCR-004 | Terms | Public | No | P0 | Confirmed |
| SCR-005 | VetifyPro | Public/professional | No | P1 | Confirmed |
| SCR-006 | Blog listing | Public | No | P1 | Confirmed |
| SCR-007 | Article detail | Public | No | P1 | Partially confirmed |
| SCR-008 | Login | All | No | P0 | Not verified |
| SCR-009 | Registration role selector | All | No | P0 | Not verified |
| SCR-010 | Owner/farmer dashboard | Owner/Farmer | Yes | P0 | Recommended |
| SCR-011 | Professional discovery | All | Optional | P0 | Confirmed concept / workflow not verified |
| SCR-012 | Professional profile | All | Optional | P0 | Recommended |
| SCR-013 | Clinic discovery/profile | All | Optional | P0 | Confirmed concept / workflow not verified |
| SCR-014 | Vendor discovery/profile | All | Optional | P1 | Confirmed concept / workflow not verified |
| SCR-015 | Animal list/detail | Owner/Farmer/assigned professional | Yes | P0 | Recommended |
| SCR-016 | Feed calculator | All | Optional | P1 | Confirmed existence / form not verified |
| SCR-017 | Disease predictor | All | Optional | P0 | Confirmed existence / form not verified |
| SCR-018 | Forum feed/post/detail | Community | Yes to post | P1 | Confirmed existence / workflow not verified |
| SCR-019 | Conversation list/thread | Allowed roles | Yes | P0 | Recommended |
| SCR-020 | Notifications | All authenticated | Yes | P1 | Recommended |
| SCR-021 | Professional workspace | Vet/VPP | Yes + verified | P0 | Not verified |
| SCR-022 | Clinic workspace | Clinic staff | Yes + approved | P1 | Not verified |
| SCR-023 | Vendor workspace | Vendor | Yes + approved | P1 | Not verified |
| SCR-024 | Verification center | Professional/clinic/vendor/admin | Yes | P0 | Recommended |
| SCR-025 | Admin console | Admin/mod/support | Yes | P0 | Recommended |
| SCR-026 | Emergency discovery | Owner/professional/clinic | Optional/Yes | P0 | Recommended |
| SCR-027 | Settings/privacy controls | Authenticated | Yes | P0 | Recommended |

## Standard page specification

Every authenticated screen must provide a title, breadcrumb or contextual back action, loading skeleton, empty state, retryable error state, permission-denied state, mobile layout, keyboard order, analytics event, and audit implication. Every data mutation must show client validation before submission, server validation after submission, success confirmation, idempotency behavior, and an undo or recovery path when safe.

## Confirmed visual/content components

The homepage visibly uses location affordances, country labels/flags, CTA image cards, feature cards, testimonials, metric cards, footer quick links, social links, and a newsletter/contact pattern [1] [2]. Exact typography tokens, breakpoints, and component states are **NOT VERIFIED** and must be measured during a screenshot/DOM pass.

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
