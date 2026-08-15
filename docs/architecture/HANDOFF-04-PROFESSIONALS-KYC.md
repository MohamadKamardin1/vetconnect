# HANDOFF-04 — Professionals, Clinics, Credentials, and KYC

## Result

The professional and clinic foundation is complete. It includes professional profiles, clinics, clinic staff membership, private credential documents, immutable KYC review decisions, verification states, location linkage, and administrator-only verification actions.

Public discovery returns only active, verified professionals. Credential object keys are never serialized, and credential listings are restricted to the owning authenticated user. Clinics are scoped to owners and active staff, while administrator access remains available for operations.

## Verification evidence

| Check | Result |
|---|---|
| Professionals migrations | Generated and applied, including deterministic-order migration |
| `pytest -q` | **16 passed** |
| `python manage.py check` | Passed |
| `python manage.py makemigrations --check --dry-run` | No changes detected |
| OpenAPI generation/validation | Passed with zero warnings/errors |

Tests cover hidden unverified professionals, administrator KYC verification and public discoverability, private owner-scoped credentials, and owner assignment for clinic creation.

## Known boundaries

The current credential upload endpoint persists metadata only; object-storage upload signing, malware scanning, retention policy, and production object-store integration remain later security/operations work. KYC verification is intentionally administrator-only and stores an auditable decision record.

## Next-phase contract

Prompt 05 must implement animals, ownership, protected veterinary records, record-level grants, and safe sharing. It must preserve the established owner/object permission boundary and prevent unauthorized clinical-record access.
