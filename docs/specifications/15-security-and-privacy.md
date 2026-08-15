# DOCUMENT 15 — Security & Privacy

## Legal research boundary

Tanzania's Personal Data Protection Act 2022 and related regulations are identified by the secondary legal guide as the primary framework; the guide states principles including lawful, fair, transparent, secure, purpose-limited, accurate, necessary, time-limited processing and constraints on transfers outside Tanzania [15]. This is legal research, not legal advice. Obtain Tanzanian counsel and confirm the current primary text, regulator guidance, sector rules, Zanzibar implications, and any cross-border hosting position before launch.

## Engineering controls

Use secure password hashing, verified phone/email, device/session management, short-lived access tokens or secure HttpOnly cookies, refresh-token rotation, CSRF protection where cookies are used, strict CORS, CSP, HSTS, output encoding, parameterized ORM queries, rate limiting, bot/brute-force controls, and step-up authentication for administrators and document access. Use deny-by-default RBAC plus object-level permissions.

File uploads require allowlisted MIME/type and size, content sniffing, malware scanning, image re-encoding, quarantine before publication, signed URLs, private buckets, retention rules, and audit trails. Protect against XSS in forum/blog content, SSRF in external media, SQL injection, insecure direct object references, path traversal, and abuse of messaging.

## Privacy controls

Collect the minimum data needed for discovery and service. Separate public profile location from precise private coordinates. Provide consent records, purpose notices, access/correction/deletion/export workflows, retention schedules, processor register, breach response, DPO ownership, and data-subject support. Animal health data linked to a person may be sensitive in context; restrict access and avoid using it for model training without a defined lawful basis and explicit governance.

## Safety and abuse

Add report/block/mute, rate limits, professional verification, review fraud controls, controlled-product policy, emergency disclaimers, content moderation, appeals, and transparent sanctions. AI outputs require logging, human oversight, privacy minimization, prompt/output redaction, model-version tracking, and a “not a diagnosis” boundary.

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
