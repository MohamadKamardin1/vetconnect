# DOCUMENT 10 — Recommended API Specification

These endpoints are **RECOMMENDED API DESIGN FOR THE TANZANIA IMPLEMENTATION**, not claims about VetKonect's actual APIs.

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Create role-specific account | Public |
| POST | `/api/v1/auth/verify` | Verify OTP/email token | Public |
| POST | `/api/v1/auth/login` | Authenticate | Public |
| POST | `/api/v1/auth/logout` | Revoke session | Auth |
| POST | `/api/v1/auth/password-reset` | Start/reset recovery | Public |
| GET | `/api/v1/me` | Current user/profile | Auth |
| PATCH | `/api/v1/me` | Edit profile/preferences | Auth |
| GET | `/api/v1/locations` | Hierarchy lookup | Public |
| GET | `/api/v1/discovery/professionals` | Nearby/filter search | Optional |
| GET | `/api/v1/professionals/{id}` | Public profile | Optional |
| GET | `/api/v1/discovery/clinics` | Clinic search | Optional |
| GET | `/api/v1/discovery/vendors` | Vendor search | Optional |
| POST | `/api/v1/animals` | Create animal | Auth |
| GET/PATCH/DELETE | `/api/v1/animals/{id}` | Manage animal | Object permission |
| POST | `/api/v1/verification-submissions` | Submit evidence | Auth |
| GET | `/api/v1/conversations` | List conversations | Auth |
| POST | `/api/v1/conversations` | Start conversation | Auth |
| POST | `/api/v1/conversations/{id}/messages` | Send message | Participant |
| POST | `/api/v1/forum/posts` | Publish post | Auth |
| POST | `/api/v1/forum/reports` | Report content | Auth |
| POST | `/api/v1/reviews` | Review interaction | Auth + interaction |
| POST | `/api/v1/tools/feed-calculations` | Calculate feed | Optional |
| POST | `/api/v1/tools/disease-assessments` | Decision support | Optional |
| GET | `/api/v1/notifications` | Notification inbox | Auth |
| POST | `/api/v1/emergency-requests` | Emergency routing | Auth/guest policy |
| POST | `/api/v1/payments/intents` | Provider-agnostic payment intent | Auth |
| POST | `/api/v1/webhooks/payments/{provider}` | Verify provider events | Server |
| GET | `/api/v1/admin/verification-queue` | Review queue | Admin |

## API non-functional rules

Use versioned JSON, consistent problem-details errors, cursor pagination, idempotency keys for mutations/payments, ETags for reference data, rate limits by identity/IP/device, correlation IDs, structured audit events, and explicit scopes. Do not expose model prompts, internal moderation signals, or private coordinates. WebSocket channels should authorize each conversation and support reconnect/resume tokens.

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
