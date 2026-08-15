# DOCUMENT 20 — Master Requirements

## Functional requirements

| ID | Requirement |
|---|---|
| REQ-AUTH-001 | The system shall allow account creation with a normalized Tanzanian phone number or email. |
| REQ-AUTH-002 | The system shall verify contact ownership before enabling public or role-gated actions. |
| REQ-AUTH-003 | The system shall enforce deny-by-default RBAC and object-level permissions. |
| REQ-LOC-001 | The system shall support Tanzania Mainland and Zanzibar as distinct jurisdiction branches. |
| REQ-LOC-002 | The system shall support region, district, ward/shehia, and village/mtaa/area references with versioned authoritative codes. |
| REQ-LOC-003 | The system shall support GPS, manual location, permission denial, stale location, and low-accuracy states. |
| REQ-DISC-001 | The system shall allow users to discover verified professionals, clinics, and vendors using geography and service/species filters. |
| REQ-DISC-002 | The system shall provide a useful no-results state with radius expansion and alternative contact paths. |
| REQ-VET-001 | The system shall support veterinarian and paraprofessional verification workflows aligned to VCT evidence categories. |
| REQ-CLINIC-001 | The system shall support approved clinic profiles, services, hours, location, emergency status, and staff membership. |
| REQ-VENDOR-001 | The system shall support approved vendor profiles and a policy-controlled product catalog. |
| REQ-ANIMAL-001 | The system shall allow owners/farmers to create and manage animal records with species, breed, sex, age, weight, purpose, location, health, vaccination, and treatment history. |
| REQ-CHAT-001 | The system shall allow authorized users to exchange real-time messages with delivery, retry, blocking, reporting, and attachment controls. |
| REQ-FORUM-001 | The system shall support moderated posts, comments, reports, blocks, and localized notifications. |
| REQ-TOOL-001 | The system shall provide a versioned feed calculator with metric units, transparent assumptions, and validation. |
| REQ-TOOL-002 | The system shall provide disease decision support that clearly distinguishes educational information from professional diagnosis and emergency care. |
| REQ-EMER-001 | The system shall provide an emergency workflow with urgent messaging, calling, location, and referral options. |
| REQ-REV-001 | The system shall permit reviews only after an eligible interaction and shall prevent duplicate reviews. |
| REQ-NOTIF-001 | The system shall support in-app, email, SMS, push, and optional WhatsApp notification adapters with preferences and fallback. |
| REQ-I18N-001 | The system shall support English and Kiswahili through translation keys for all user-facing text. |
| REQ-PWA-001 | The system shall remain usable on 320px+ mobile screens and slow/intermittent networks. |
| REQ-PRIV-001 | The system shall provide consent, access, correction, export, deletion, retention, and processor-governance controls subject to legal review. |
| REQ-SEC-001 | The system shall protect against common web/API threats, brute force, abuse, unsafe uploads, and insecure object access. |
| REQ-AI-001 | The system shall log AI model/version, input provenance, output, human review, and safety escalation for clinical AI. |
| REQ-ADMIN-001 | The system shall allow authorized administrators to manage users, roles, verification, content, reports, reference data, configuration, and audit logs. |
| REQ-API-001 | The system shall expose versioned, documented REST/service APIs with idempotency, pagination, consistent errors, and correlation IDs. |
| REQ-DATA-001 | The system shall use PostgreSQL/PostGIS with spatial indexes, versioned reference data, private media storage, and immutable audit events. |
| REQ-OBS-001 | The system shall provide logs, metrics, traces, error tracking, security alerts, health checks, and business analytics. |

## Gap analysis

| VetKonect capability | Tanzania requirement | Gap | Recommended solution |
|---|---|---|---|
| Location discovery | Mainland + Zanzibar hierarchy | Original public evidence does not expose Tanzanian hierarchy behavior | NBS-based administrative model + PostGIS + manual fallback [8] [9] |
| Professional connection | VCT-backed local trust | Nigerian terms cite VCN, not Tanzania | VCT evidence and local reviewer workflow [4] [11] [12] |
| Chat/forum | Rural and intermittent connectivity | Standard online flows are insufficient | Offline queue, SMS fallback, compressed media |
| Feed calculator | Local species/feed systems | Original formulas not verified | Versioned rulesets with Tanzanian expert review |
| Disease predictor | Local disease patterns and safe triage | Original model/data not verified | Explainable decision support, local review, emergency escalation |
| Payments | Mobile money and BoT oversight | Original terms reference Paystack/Nigeria | Provider abstraction, BoT-compliant adapters [13] [14] |
| Privacy | Tanzania PDPA and potentially Zanzibar-specific review | Original privacy policy is generic and Nigeria-based | Tanzanian legal review, consent/retention/DPO controls [3] [15] |
| AI clinical assistant | Professional oversight and local language | VetifyPro capability is advertised, implementation unknown | Human-in-loop, bilingual evaluation, audit, provider abstraction [5] |

## Development-readiness checklist

Before implementation sign-off, confirm every private route, registration field, validation message, dashboard submenu, calculator formula, disease rule, notification channel, role permission, and mobile state through a credentialed evidence pass. Mark unknowns as **NOT VERIFIED** rather than silently converting recommendations into historical claims.

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
