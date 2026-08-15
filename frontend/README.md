# VetKonnect frontend

This is the responsive web experience for **VetKonnect Tanzania & Zanzibar**. It is a React 19, TypeScript, Vite, Tailwind 4 application that consumes the Django REST API under `/api/v1/`.

## What is included

The application contains a premium mobile-first public website, professional discovery, marketplace and community entry points, authentication surfaces, and a role-aware protected workspace. The workspace presents UI paths for animal records, clinician credentials, ClickPesa verification badge subscriptions, marketplace, conversations, community, notifications, feed planning, and disease-support context.

> The interface preserves clinical safety boundaries. It presents disease-support and feed-planning tools as structured decision support, never diagnosis or emergency triage.

## Local development

```bash
pnpm install
VITE_API_BASE_URL=http://localhost:8000 pnpm dev
```

Set `VITE_API_BASE_URL` to the Django backend origin, for example `http://localhost:8000`. The client expects the backend route contract to be mounted beneath `/api/v1/`.

## Quality checks

```bash
pnpm check
pnpm build
```

## Authentication and authorization

The browser client stores the SimpleJWT access token in session storage and sends it only through the `Authorization: Bearer` header. The backend remains the authority for RBAC, KYC, protected animal records, ClickPesa subscriptions, payment webhooks, and all data-level authorization decisions. The UI never grants an access right solely from a route or visual state.

## Deployment

Build with `pnpm build` and serve `dist/public` from a CDN or static web server. Configure the Django backend CORS/CSRF origins for the deployed frontend and set `VITE_API_BASE_URL` during the build. Do not place credentials, ClickPesa checksum keys, private keys, or Django secrets in a `VITE_` variable.

## Asset licensing and storage

The branded hero, verification, livestock, marketplace, and seal visuals are referenced through stable managed storage paths. They are not stored in this repository to keep source control and deployments lightweight.
