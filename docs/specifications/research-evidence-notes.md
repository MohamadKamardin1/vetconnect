# VetKonect research notes

## Research date
2026-08-12 (user timezone)

## Initial live-site evidence
The homepage at https://www.vetkonect.com/ was successfully extracted on first navigation. It presents the service as “Quality animal care at your fingertips” and lists country coverage including Nigeria, Ghana, Kenya, South Africa, Egypt, Ethiopia, Tanzania, Uganda, and Rwanda. The homepage exposes or describes: nearby veterinarians; connecting with animal health professionals; locating veterinary clinics; connecting to vendors; a Feed Calculator; a Disease Predictor; and a Chat Forum. CTAs observed include `/dashboard/vet-vendor` for professional/clinic/vendor discovery and `/dashboard/chat-forum` for the community forum.

The homepage includes a nearby-veterinarian empty state (“No veterinarians found” / “We couldn't find any veterinarians in your area”), indicating location-based discovery and a user-facing no-results state. It also includes testimonials, social/video testimonials, and metric cards for veterinarians, social media presence, vendor store & vet clinic, mobile app downloads, and pet owners/livestock farmers. The homepage references a mobile app via its metrics but the app route/download link was not yet verified.

## Access limitation
A subsequent browser HTML view failed with `ERR_CONNECTION_CLOSED` at `chrome-error://chromewebdata/` after the initial successful extraction. Therefore all later behaviors, authentication-only flows, and route details must be explicitly marked NOT VERIFIED unless independently confirmed through public sources or a later successful access attempt.

## Classification rule
Observed homepage claims are CONFIRMED only for the exact content extracted. Dashboard, registration, login, admin, calculators, disease predictor, messaging, and mobile-app workflows remain NOT VERIFIED until directly observed. Recommendations for Tanzania/Zanzibar are RECOMMENDED; deductions from homepage CTAs are INFERRED.

## Initial route evidence
- `/dashboard/vet-vendor` — linked from multiple homepage “Get Started” CTAs; destination behavior not verified.
- `/dashboard/chat-forum` — linked from the homepage Chat Forum CTA; destination behavior not verified.
- Homepage `/` — public, CONFIRMED from live extraction.

## Asset/page clues
Homepage image and SVG asset names include `feedCalculator`, `diseasePredictor`, `chatImage`, `cta`, `secondCta`, `thirdCta`, and `marker`, which corroborate the named homepage sections but do not independently establish workflow behavior.

## Source
Primary evidence: https://www.vetkonect.com/ (homepage extraction, 2026-08-12).
