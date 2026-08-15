# DOCUMENT 08 — UX/UI Specification

## Observed visual language

The live homepage uses a warm animal-health marketing aesthetic with globe/organic decorative assets, location markers, photo-led CTA cards, feature illustrations, testimonials, metric cards, and a footer with social/legal navigation [1]. Exact color values, font family, breakpoints, focus states, and component tokens are **NOT VERIFIED** because a stable screenshot/DOM measurement pass was not completed.

## Tanzania design system recommendation

Use a distinct brand identity. Define design tokens as CSS variables: `--color-primary`, `--color-secondary`, `--color-surface`, `--color-danger`, `--color-warning`, `--color-success`, `--color-text`, and `--space-1` through `--space-8`. Prefer high-contrast, low-ink surfaces and avoid relying on color alone. Use a readable sans-serif with Kiswahili diacritic support. Body text should target 16px minimum on mobile, line height 1.45–1.6, and touch targets of at least 44px.

## Component states

Buttons require default, hover, focus-visible, pressed, disabled, loading, and destructive-confirmation states. Inputs require empty, filled, focused, invalid, valid, disabled, read-only, and offline-draft states. Cards require loading skeleton, content, no-result, unavailable, and permission-limited states. Maps require loading, denied permission, stale location, no coverage, and manual-selection fallback. Chat requires sending, queued offline, delivered, read, failed, blocked, and attachment-scanning states.

## Responsive behavior

The product is mobile-first at 320px, 360px, and 390px widths, then tablet and desktop. Desktop sidebars collapse to a drawer; tables become stacked cards; multi-column forms become one column; maps offer list/map toggle; persistent emergency contact remains reachable without obscuring content. Use progressive enhancement for PWA and minimize JavaScript for public content.

## Accessibility checklist

Use semantic headings, landmarks, labeled controls, keyboard navigation, visible focus, screen-reader status announcements, error summaries, programmatic association of errors/help, reduced-motion preference, captions/transcripts for media, accessible charts, and a non-map text alternative. Test WCAG 2.2 AA with keyboard-only, screen reader, low vision, color-vision deficiency, and touch usability. Error messages must be available in English and Kiswahili.

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
