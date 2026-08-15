# HANDOFF-10 — Feed Calculator and Disease Decision Support

## Result

The feed and disease phase is implemented as a configuration-driven decision-support boundary. Exact formulas and disease-confidence behavior were not present in the specification, so the backend does not invent hidden constants or claim diagnostic certainty. Feed rules are versioned and auditable. Disease rules are versioned, symptom-weighted, and auditable.

Feed requests validate required metric inputs, return explicit `INVALID` results for missing or malformed values, return `MISSING_CONFIGURATION` when no verified rule exists, and calculate only when an enabled configured formula is available. Disease requests validate the complete intake, return explicit missing-configuration states, rank possible conditions from configured symptom weights, mark high-risk or severe cases as `EMERGENCY`, require referral in those cases, and always include a non-diagnostic disclaimer.

## API surface

| Method | Route | Purpose |
|---|---|---|
| POST/GET | `/api/v1/feed/calculations/` | Create or list owner-scoped feed calculations |
| POST/GET | `/api/v1/disease/assessments/` | Create or list owner-scoped disease decision-support assessments |

## Verification evidence

| Check | Result |
|---|---|
| Feed/disease migrations | Generated and applied |
| Full test suite | **28 passed** |
| `python manage.py check` | Passed |
| Migration drift check | No changes detected |
| OpenAPI generation/validation | Passed with zero errors; one non-blocking status-enum naming warning remains from multiple unrelated model status sets |

## Safety and privacy evidence

Assessment history is authenticated and owner-scoped. The API uses “possible conditions,” urgency, referral, assumptions, provenance through rule/version identifiers, and a mandatory disclaimer instead of definitive diagnosis claims. Emergency escalation is deterministic from configured high-risk symptoms or severe/critical severity.

## Next-phase contract

Prompt 11 must implement in-app notifications, preferences, delivery logs, Celery task boundaries, retry/idempotency behavior, and provider adapters without exposing real credentials in the repository.
