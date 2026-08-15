# HANDOFF-06 — Discovery, Services, Reviews, and Ratings

## Result

The discovery phase is complete. Public service search exposes active services only for active, verified clinics. Public review search exposes approved reviews only for verified clinics or professionals. Review creation accepts exactly one target, prevents self-review, validates ratings from 1 to 5, and preserves one-review-per-user constraints at the database layer.

Administrator moderation can approve, reject, or hide reviews with a reason. Moderated content does not become publicly visible unless approved.

## Verification evidence

| Check | Result |
|---|---|
| Discovery migrations | Generated and applied |
| Full test suite | **20 passed** |
| `python manage.py check` | Passed |
| `python manage.py makemigrations --check --dry-run` | No changes detected |
| OpenAPI generation/validation | Passed with zero warnings/errors |

Tests prove verified-only service exposure, self-review denial, and approved-review public visibility.

## Next-phase contract

Prompt 07 must implement vendor, product, inventory, and marketplace scope. It must preserve the existing verified-clinic/vendor boundary, separate catalog availability from sensitive stock operations, and avoid claiming payments or fulfillment before a payment provider is integrated.
