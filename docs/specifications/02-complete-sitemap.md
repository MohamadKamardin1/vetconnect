# DOCUMENT 02 — Complete Sitemap

## Evidence-labeled route tree

```text
PUBLIC
├── /                                  Homepage [CONFIRMED]
├── /about                             About, mission, team, map, contact form [CONFIRMED]
├── /privacy                           Privacy policy [CONFIRMED]
├── /terms-condition                   Terms and user policy [CONFIRMED]
├── /vetifypro                         AI clinical assistant marketing page [CONFIRMED]
├── /blog                              Blog listing, 10 articles, load more [CONFIRMED]
├── /blog/{slug}                       Article detail [INFERRED from listing; route NOT VERIFIED]
├── /feed-calculator                   Footer-linked tool [NOT VERIFIED]
├── /disease-predictor                 Footer-linked tool [NOT VERIFIED]
├── /dashboard/vet-vendor              Professional/clinic/vendor CTA target [PARTIALLY CONFIRMED]
└── /dashboard/chat-forum              Forum CTA target [PARTIALLY CONFIRMED]

AUTHENTICATION [RECOMMENDED, PRIVATE ROUTES NOT VERIFIED]
├── /auth/register
│   ├── /owner-farmer
│   ├── /veterinarian
│   ├── /paraprofessional
│   ├── /clinic
│   └── /vendor
├── /auth/login
├── /auth/verify-phone
├── /auth/verify-email
├── /auth/forgot-password
├── /auth/reset-password/{token}
└── /auth/logout

DISCOVERY [RECOMMENDED / SOME HOMEPAGE CONCEPTS CONFIRMED]
├── /professionals
├── /professionals/{id}
├── /clinics
├── /clinics/{id}
├── /vendors
├── /vendors/{id}
├── /products
├── /products/{id}
├── /search
└── /emergency

AUTHENTICATED PRODUCT
├── /app
├── /app/profile
├── /app/animals
│   ├── /new
│   └── /{id}
├── /app/messages
├── /app/notifications
├── /app/saved
├── /app/history
├── /app/forum
├── /app/calculations/feed
├── /app/predictions/disease
└── /app/settings

PROFESSIONAL / CLINIC / VENDOR WORKSPACES [RECOMMENDED]
├── /workspace/professional
│   ├── /profile
│   ├── /availability
│   ├── /requests
│   ├── /cases
│   ├── /reviews
│   ├── /verification
│   └── /settings
├── /workspace/clinic
│   ├── /profile
│   ├── /staff
│   ├── /services
│   ├── /hours
│   ├── /appointments
│   ├── /reviews
│   └── /settings
└── /workspace/vendor
    ├── /profile
    ├── /catalog
    ├── /inventory
    ├── /orders
    ├── /inquiries
    ├── /reviews
    └── /settings

ADMIN [RECOMMENDED / NOT VERIFIED]
└── /admin
    ├── /users
    ├── /roles
    ├── /verifications
    ├── /locations
    ├── /species-breeds
    ├── /diseases-symptoms
    ├── /feed-rules
    ├── /forum
    ├── /reviews-reports
    ├── /blog
    ├── /notifications
    ├── /payments
    ├── /analytics
    ├── /audit-log
    └── /system
```

## Route contract

Each route must declare `visibility`, `auth_required`, `role_required`, `canonical_url`, `entry_points`, `exit_points`, `data_dependencies`, `empty_state`, `error_state`, `mobile_behavior`, and `SEO policy`. Public discovery pages should be indexable only when profiles are verified and consent to public listing. Private workspaces must be `noindex` and protected by server-side authorization, not just client navigation.

## Public page findings

The homepage has a location marker, country selector/list, nearby-veterinarian section, CTA cards, calculator/predictor cards, forum CTA, testimonials, metrics, footer legal links, social links, and newsletter/contact affordances [1]. About adds a 500-character contact message, terms acceptance, map, team, partnership/support sections, and geographic coverage content [2]. Blog has article cards with author/date, excerpt, engagement counters, and “Load More Articles” [7].

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
