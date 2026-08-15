# DOCUMENT 06 — Workflow Specification

## Evidence note

Only public flows were directly observed. The homepage establishes CTA entry points and public empty states; legal and VetifyPro pages establish policy and AI claims. The following private workflows are implementation requirements, not claims about the current VetKonect internals.

### WF-001 Registration

1. User selects Owner/Farmer, Veterinarian, VPP, Clinic, or Vendor. 2. System collects role-specific identity and contact data. 3. User verifies phone or email. 4. System collects location using GPS or manual hierarchy. 5. Professional/clinic/vendor users upload required evidence. 6. User accepts terms/privacy and clinical disclaimers where applicable. 7. System creates a pending account, sends confirmation, and routes gated roles to verification. 8. Approval changes search visibility and enables role-specific actions.

### WF-002 Login and recovery

1. User submits phone/email and password. 2. Rate limiter and credential service evaluate the request. 3. Optional OTP is required for new device or risk event. 4. Session is issued with secure cookies/tokens. 5. Failed attempts use generic errors. 6. Recovery uses single-use, expiring token and notification; old sessions can be revoked.

### WF-003 Professional verification

Registration → document upload → malware scan → completeness check → human review → approve/reject/request resubmission → verified badge and scope → periodic renewal. The VCT website describes registration/enrolment categories and qualifications; the platform should verify against authoritative workflows rather than inventing regulatory requirements [11] [12].

### WF-004 Nearby professional search

1. Request location permission. 2. If denied, select country/region/district/ward/shehia/village manually. 3. Query verified profiles using PostGIS radius and administrative fallback. 4. Rank by verified status, species/service fit, distance, availability, response rate, and quality signals without covert pay-to-rank. 5. Show result cards and no-results recovery. 6. Open profile, save, call, message, or request service.

### WF-005 Contact / consultation request

1. Owner chooses professional/clinic. 2. Selects animal, reason, urgency, preferred channel, and availability. 3. Safety gate routes emergency signals to emergency workflow. 4. Professional accepts, rejects, or requests more information. 5. System opens a consented conversation and logs state transitions. 6. On completion, both parties may access a review flow; records are retained per policy.

### WF-006 Vendor discovery and order

Search → vendor profile → product detail → inquiry/cart where enabled → price/availability confirmation → payment abstraction → order status → delivery/pickup → dispute/review. Product authenticity, expiry, controlled substances, and seller compliance require human/admin safeguards.

### WF-007 Feed calculation

Select species and production stage → enter weight/count/feed type and metric units → validate → calculate with versioned formula/ruleset → explain assumptions and range → save/export/share → allow professional review. Exact original formulas are **NOT VERIFIED**.

### WF-008 Disease decision support

Select species → collect symptoms, onset, severity, vaccination and exposure → run versioned rules/model → classify urgency → show possible conditions and reasoning → provide warning signs and next step → refer to professional/emergency service → save with consent. Never use “diagnose” as an unconditional claim in the Tanzania UX.

### WF-009 Forum moderation

Create post → scan/validate → publish or queue → comments/replies/mentions → report/block → moderator triage → action/appeal → audit and notification. Attachments require malware scanning and signed access.

### WF-010 AI clinical assistance

Professional starts consultation → consent and recording indicator → speech-to-text → structured SOAP draft → evidence-linked differentials/clinical guidance → professional edits/accepts → owner summary draft → human review → share → immutable audit of AI output and final professional action. VetifyPro advertises these capabilities [5], but the model, evidence corpus, and operational safeguards are not publicly verified.

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
