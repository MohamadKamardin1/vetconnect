# DOCUMENT 12 — Next.js Architecture

Use the App Router with route groups for `(marketing)`, `(auth)`, `(public-discovery)`, `(app)`, `(workspace)`, and `(admin)`. Server Components should render public SEO pages, profile summaries, blog content, and initial discovery results. Client Components should handle maps, chat, calculators, form interactivity, optimistic queues, and accessible modals.

Use middleware only for coarse session gating and locale routing; enforce authorization in Django. Use a typed API client generated or hand-maintained from an OpenAPI contract. Add React Hook Form or equivalent with Zod-compatible schemas shared conceptually with backend validation, but always reconcile server errors. Use route-level `loading.tsx`, `error.tsx`, and `not-found.tsx`; provide domain-specific empty states.

Cache public blog and verified-profile projections with explicit revalidation. Do not cache private health, messaging, or verification data in shared caches. Implement i18n with stable keys and English/Kiswahili dictionaries; preserve language preference server-side and offline. Implement PWA manifest, service worker, background sync for safe drafts, image compression, and a visible offline indicator. Use structured metadata, canonical URLs, sitemap, robots, Open Graph, and JSON-LD for public professionals, clinics, blog posts, and locations only when consented.

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
