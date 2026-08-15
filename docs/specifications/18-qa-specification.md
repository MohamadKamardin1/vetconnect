# DOCUMENT 18 — QA Specification

## Acceptance criteria examples

| ID | Requirement | Acceptance criterion |
|---|---|---|
| AC-AUTH-001 | Tanzanian account registration | Given a valid +255 phone and consent, the system creates a pending account, sends OTP, and does not expose the account publicly before verification. |
| AC-LOC-001 | Nearby discovery | Given a permitted GPS point, the system returns verified profiles within the configured radius ranked by distance and service fit; when GPS is denied, manual hierarchy remains available. |
| AC-VET-001 | Professional verification | Given valid VCT evidence, the record enters review; approval creates a verified badge and public scope; rejection includes a reason and resubmission path. |
| AC-ANIMAL-001 | Animal save | Given valid species, sex, age/weight, and owner, the system saves the animal and displays it in the owner's list. |
| AC-DIS-001 | Disease safety | Given emergency symptoms, the system shows an urgent referral and does not present an autonomous diagnosis or treatment prescription. |
| AC-MSG-001 | Offline message | Given temporary network loss, the composer queues a message, shows queued status, and sends once connectivity returns without duplication. |
| AC-PRIV-001 | Deletion | Given an authenticated deletion request, the system confirms scope, executes retention/legal-hold rules, revokes sessions, and records an audit event. |

## High-priority test cases

| Test ID | Preconditions | Steps | Expected | Priority |
|---|---|---|---|---|
| TC-AUTH-001 | No account | Register duplicate phone | Generic duplicate error; no data leak | P0 |
| TC-AUTH-002 | Account exists | Fail login repeatedly | Rate limit and alert; no account enumeration | P0 |
| TC-LOC-001 | GPS denied | Choose manual Zanzibar hierarchy | Results use selected shehia/district and explain precision | P0 |
| TC-SEARCH-001 | No nearby providers | Search rural location | Clear empty state, radius expansion, referral/contact alternatives | P0 |
| TC-VERIFY-001 | Pending professional | View as owner | No verified badge or gated consultation access | P0 |
| TC-FEED-001 | Valid inputs | Run calculation twice with same version | Deterministic result and assumptions | P1 |
| TC-DIS-001 | Severe symptoms | Submit assessment | Emergency escalation, disclaimer, audit snapshot | P0 |
| TC-FORUM-001 | Auth user | Upload disallowed file | Rejected before publication with localized error | P1 |
| TC-MSG-001 | Blocked user | Attempt message | Denied, no delivery, actionable explanation | P0 |
| TC-SEC-001 | Auth user | Request another user's record URL | 403/404 without existence leak | P0 |
| TC-A11Y-001 | Any screen | Keyboard-only complete form | Logical focus, labels, errors, submit success | P0 |
| TC-MOBILE-001 | 320px device | Use dashboard and map/list toggle | No horizontal overflow; core tasks complete | P0 |

## Edge/error library

Include no GPS, invalid hierarchy, no results, unverified provider, suspended account, deleted profile, duplicate animal, stale feed rules, model timeout, dangerous symptom, upload failure, malware quarantine, blocked user, spam flood, offline mutation, payment timeout, webhook replay, map provider failure, 401/403/404/409/422/429/500/503, and expired verification. All messages require English and Kiswahili keys and a recovery action.

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
