# DOCUMENT 03 — User Roles and Permissions

## Role catalogue

| Role ID | Role | Status | Core purpose |
|---|---|---|---|
| ROLE-OWNER | Pet owner / animal owner | CONFIRMED in public positioning; exact account flow NOT VERIFIED | Manage animals and find help |
| ROLE-FARMER | Livestock farmer | CONFIRMED in public positioning | Manage herds/flocks and farm-health needs |
| ROLE-VET | Veterinarian | CONFIRMED | Offer professional animal-health services |
| ROLE-VPP | Veterinary paraprofessional | CONFIRMED in homepage/privacy/terms | Offer services within permitted scope |
| ROLE-CLINIC | Veterinary clinic/facility | CONFIRMED as concept; workflow NOT VERIFIED | Publish facility and staff services |
| ROLE-VENDOR | Veterinary shop/vendor | CONFIRMED as concept; catalog/order workflow NOT VERIFIED | Offer animal-health products |
| ROLE-MOD | Moderator | INFERRED | Review reports and community content |
| ROLE-CONTENT | Content manager | INFERRED from blog | Manage educational content |
| ROLE-SUPPORT | Support/operations | RECOMMENDED | Resolve user, verification, and safety cases |
| ROLE-ADMIN | Platform administrator | RECOMMENDED | Govern configuration, roles, audit, and safety |

## Permission matrix

Legend: **✓** allowed, **O** own records only, **S** scoped/verified records, **—** denied, **R** requires policy review.

| Capability | Owner/Farmer | Vet | VPP | Clinic | Vendor | Moderator | Admin |
|---|---:|---:|---:|---:|---:|---:|---:|
| Create account | ✓ | ✓ | ✓ | ✓ | ✓ | R | ✓ |
| Manage own profile | O | O | O | O | O | O | S |
| Search professionals | ✓ | ✓ | ✓ | ✓ | ✓ | S | ✓ |
| View verified public profile | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Contact professional | ✓ | ✓ | ✓ | ✓ | R | S | ✓ |
| Create animal record | O | O | O | S | — | S | ✓ |
| Upload health records | O | O | O | S | — | — | S |
| Submit verification documents | — | O | O | O | O | — | S |
| Approve verification | — | — | — | — | — | R | ✓ |
| Create clinic services | — | — | — | O | — | — | S |
| Manage clinic staff | — | — | — | O | — | — | ✓ |
| Create product listing | — | — | — | — | O | — | S |
| Manage inventory/orders | — | — | — | — | O | — | S |
| Use feed calculator | ✓ | ✓ | ✓ | ✓ | R | S | ✓ |
| Use disease decision support | ✓ | ✓ | ✓ | ✓ | R | S | ✓ |
| Publish forum post | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Comment/report/block | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Moderate content | — | — | — | — | — | ✓ | ✓ |
| Submit review | After interaction | After interaction | After interaction | After interaction | After interaction | R | ✓ |
| Manage own availability | — | O | O | S | — | — | S |
| Emergency request | ✓ | ✓ | ✓ | ✓ | — | S | ✓ |
| View sensitive health data | O/consented | Assigned cases | Assigned cases | Assigned cases | — | — | S/audited |
| Export/delete account | O | O | O | O | O | R | S |

## RBAC rules

Authorization is deny-by-default and evaluated at API/service level. A user may have multiple roles, but role elevation requires verification and approval. A clinic account is an organization with staff memberships, not a shared password. Sensitive animal or consultation records require object-level permissions, explicit relationship checks, consent where applicable, and audit logging. Moderators must not see private clinical records unless a safety investigation is approved and logged.

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
