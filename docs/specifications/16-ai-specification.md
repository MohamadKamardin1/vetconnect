# DOCUMENT 16 — AI Specification

## Observed AI surface

The privacy policy says AI-powered Disease Predictor and Feed Calculator analyze user-provided data [3]. VetifyPro publicly advertises speech-to-text consultation capture, structured SOAP notes, real-time evidence-based differentials and treatment recommendations, plain-language client summaries, and AI chat [5]. The underlying models, validation studies, clinical corpus, uptime, pricing implementation, and actual integration with the main platform are **NOT VERIFIED**.

## Safe Tanzania architecture

Create an AI provider abstraction with model registry, prompt/version registry, retrieval/evidence layer, safety policy, redaction, evaluation suite, cost budgets, and human-review state. Clinical outputs are decision support for qualified professionals or educational guidance for owners; they never constitute a diagnosis, prescription, or emergency substitute. The disease module should show possible conditions, uncertainty, observed symptoms, warning signs, recommended next action, and referral options.

| AI feature | Input | Output | User | Guardrails |
|---|---|---|---|---|
| Disease decision support | species, symptoms, history, location | ranked possibilities, urgency, next step | Owner/professional | triage rules, disclaimer, referral, no certainty |
| Feed assistant | species, stage, weight, count, feed context | calculation plus assumptions | Farmer/professional | versioned formulas, range checks, expert review |
| Clinical scribe | consented audio/text | transcript and SOAP draft | Vet/VPP | recording notice, edit-before-save, no autonomous sign-off |
| Clinical guidance | case findings | evidence-linked differential/support | Vet/VPP | professional-only, source citation, escalation |
| Client summary | approved clinical notes | plain-language draft | Vet/VPP | human approval, translation review |
| Forum safety | text/media | spam/abuse signals | Moderator | human decision, appeal, no covert censorship |

Store AI input/output references with minimum necessary data, model/version, evidence version, reviewer, acceptance/edit history, and retention policy. Evaluate in English and Kiswahili, across species, local terminology, low-resource conditions, and harmful edge cases. Do not claim accuracy without a documented validation protocol.

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
