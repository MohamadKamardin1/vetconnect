# HANDOFF-03 — Tanzania and Zanzibar Location Foundation

## Result

The location foundation is complete. The backend now models Territory, Region, District, Ward, Locality, and ServiceArea with normalized codes, parent-child constraints, active flags, territory separation, service-area relationships, and PostGIS-ready latitude/longitude storage boundaries.

Public read-only APIs are available under `/api/v1/locations/` for regions, districts, wards, localities, and service areas. Public locality responses round coordinates to two decimal places and include a radius instead of exposing exact sensitive coordinates.

## Verification evidence

| Check | Result |
|---|---|
| Location migrations | Generated and applied, including deterministic ordering migration |
| `pytest -q` | **12 passed** |
| `python manage.py check` | Passed |
| `python manage.py makemigrations --check --dry-run` | No changes detected |
| OpenAPI generation/validation | Passed with zero warnings/errors |

Tests prove Mainland/Zanzibar filtering, hierarchy relations, and privacy-safe rounded coordinates. Real PostGIS distance/index verification remains pending because the current sandbox does not provide the PostGIS service; Compose contains the production topology.

## Next-phase contract

Prompt 04 must build professional, clinic, staff, credential, and KYC workflows. It must link every professional/clinic to the location hierarchy, enforce document access restrictions, preserve immutable verification history, and deny public discovery of unverified professionals.
