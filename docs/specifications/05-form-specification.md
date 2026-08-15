# DOCUMENT 05 — Form Specification

The exact private forms were not accessible. The following inventory is the minimum production specification derived from confirmed product surfaces and Tanzania requirements; it must be validated against a second authenticated research pass.

| Form ID | Form | Role | Required fields | Validation / conditional logic |
|---|---|---|---|---|
| FRM-AUTH-001 | Register owner/farmer | Owner/Farmer | name, phone/email, password, language, location, consent | Normalize +255 phone; unique identity; strong password; location manual fallback; terms required |
| FRM-AUTH-002 | Register professional | Vet/VPP | identity, phone/email, password, category, VCT details, location, scope, consent | Registration category controls documents; VCT number format is verified server-side; no public badge before approval |
| FRM-AUTH-003 | Register clinic | Clinic representative | legal name, facility name, contact, address, coordinates, services, staff, documents | Facility approval; coordinates optional but discovery requires a location; duplicate detection |
| FRM-AUTH-004 | Register vendor | Vendor | business name, owner, phone, location, categories, compliance documents | Product-sale permissions gated by approval; prohibited/controlled product policy |
| FRM-AUTH-005 | Login | All | phone/email, password, remember device | Generic failure message; rate limit; optional OTP step-up |
| FRM-AUTH-006 | Forgot/reset password | All | phone/email, OTP/token, new password | Token expiry, one-time use, password reuse block |
| FRM-PROFILE-001 | Professional profile | Vet/VPP | bio, specialties, species, services, languages, radius, availability, fees, contacts | Verified scope and specialties; public contact privacy controls |
| FRM-CLINIC-001 | Clinic profile | Clinic | name, address hierarchy, GPS, hours, emergency, services, species, photos | Hours cross-midnight support; emergency status requires contact and escalation policy |
| FRM-VENDOR-001 | Product listing | Vendor | name, category, description, price, unit, stock, image, compliance metadata | Positive money/quantity; expiry and regulated-category review; image scan |
| FRM-ANIMAL-001 | Animal record | Owner/Farmer/assigned professional | name/tag, species, breed, sex, birth/age, weight, purpose, location, health status | Species controls breed; age/weight units; consented professional access |
| FRM-FEED-001 | Feed calculation | All | species, category, age/stage, count, weight/production, feed type, units | Metric units; range validation; explain assumptions; no result if required inputs missing |
| FRM-DISEASE-001 | Disease decision support | All | species, age, location, symptoms, onset, severity, vaccination, exposure | High-risk symptom gate; emergency escalation; never label as definitive diagnosis |
| FRM-FORUM-001 | Post/comment/report | Authenticated | text, category/tag, attachments, consent | Size/type limits; malware scan; profanity/abuse detection; report reason |
| FRM-MSG-001 | Message | Allowed users | recipient, text/attachment | Relationship/blocked checks; rate limits; offline queue; delivery state |
| FRM-REVIEW-001 | Review | Verified interaction participant | rating, text, interaction reference | One review per interaction; moderation; edit window; no retaliation exposure |
| FRM-VERIFY-001 | Verification submission | Professional/clinic/vendor | documents, identifiers, declarations | Virus scan, encryption, reviewer queue, rejection reason, resubmission versioning |
| FRM-ADMIN-001 | Content/report action | Admin/mod | action, rationale, duration, notification | Mandatory audit reason; separation of duties for severe sanctions |

## Common field rules

Every field has a stable key, label, help text, translated error key, input type, requiredness, server schema, audit sensitivity, and retention classification. Errors must be actionable and localized. Client-only validation is never authoritative. For slow networks, preserve draft state locally with explicit consent and encrypt or minimize sensitive drafts.

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
