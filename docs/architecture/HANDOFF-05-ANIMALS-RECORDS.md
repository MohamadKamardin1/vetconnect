# HANDOFF-05 — Animals and Protected Veterinary Records

## Result

The animal and clinical-record foundation is complete. Owners can create and manage their own animals. Authenticated users can create records only for animals they own, while record reads are restricted to the owner, author, administrator, or an active explicit record grant.

Record grants support READ/WRITE permissions, expiration, revocation, owner issuance, and access logs. Expired grants and revoked grants are denied at the queryset boundary, not merely hidden in the serializer.

## Verification evidence

| Check | Result |
|---|---|
| Animals migration | Generated and applied |
| Adversarial animal/record tests | **18 total suite tests passed** |
| `python manage.py check` | Passed |
| `python manage.py makemigrations --check --dry-run` | No changes detected |
| OpenAPI generation/validation | Passed with zero warnings/errors |

The tests cover owner isolation, protected record grants, expiry, revocation, and authenticated record access. A failing expiry test was found and fixed by adding the grant-expiry predicate to both list and detail querysets.

## Security boundaries

The API does not rely on client-supplied owner identity. Animal creation binds the owner to the authenticated user, record creation verifies ownership of the animal, grant creation verifies ownership of the record, and read access requires an active grant or a privileged relationship. Record reads generate access-log entries.

## Next-phase contract

Prompt 06 must implement search/discovery, clinic/professional services, reviews, and ratings. It must search only public verified entities, enforce one-review-per-user semantics, prevent self-review, and moderate or hide rejected content.
