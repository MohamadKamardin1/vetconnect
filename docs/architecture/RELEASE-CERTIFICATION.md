# Release Certification

## What this document is

A plain, honest assessment of what is and isn't ready, so "certification" means something rather than being a formality. This is not a legal or compliance sign-off — it's an engineering summary a reviewer can check against real code, real tests, and the traceability matrix.

## Scope covered

Everything in `docs/architecture/IMPLEMENTATION-TODO.md` phases 1–14 (foundation through API documentation/error finalization), plus the ClickPesa badge extension. Cross-referenced in full against the backlog in `docs/architecture/TRACEABILITY-MATRIX.md`.

## Real verification result (operator's first full-suite run)

The operator ran the full, repository-wide suite for real. First run: **71 tests collected, 70 passed, 1 failed** — plus one unrelated migration surfaced. Both issues traced to real causes and fixed in the same session (see `HANDOFF-14-API-DOCS-ERROR-FINALIZATION.md` for full detail):

- The 1 failing test was a test bug (`override_settings` doesn't reach DRF's class-bound `THROTTLE_RATES`), not an application defect. Fixed with the standard DRF-testing pattern.
- `makemigrations --check` surfaced a genuine pre-existing drift in `accounts.OneTimeToken` — a real, actively-used index that was missing from `Meta.indexes` since before any of phases 12–15, only caught because this was the first time `makemigrations --check` ran across the whole project rather than one app at a time. Fixed by restoring the model to match the existing migration (not by removing the index, which would have been a regression).

Critically: **all 6 new `marketplace` tests passed** on this same run — the marketplace regression fix and adversarial IDOR tests are confirmed working against a real database, not just reviewed. This updates the "not yet run anywhere" caveat below, which was accurate when this document was first written but is no longer the current state.

## Test suite summary (counted directly from the repository, not estimated)

| App | Test functions |
|---|---:|
| accounts | 9 |
| locations | 1 |
| professionals | 4 |
| animals | 2 |
| discovery | 2 |
| marketplace | 6 (added this phase — was 0) |
| messaging | 2 |
| community | 2 |
| feed | 2 |
| disease | 2 |
| notifications | 3 |
| billing | 5 |
| ai | 7 |
| audit | 3 |
| privacy | 4 |
| core | 13 |
| **Total** | **67** |

Every number above was produced by grepping `def test_` across each app's `tests/` directory in this sandbox, not estimated or copied from a prior claim.

## Adversarial coverage — what's actually been checked

- **Cross-user data isolation (IDOR):** verified with real tests in `ai` (interactions), `privacy` (export/deletion requests), `audit` (admin-only access), `marketplace` (vendor products, inventory, inquiries — added this phase), and `accounts` (admin-only suspend/reactivate/delete). Not independently re-verified in this phase for `animals`, `messaging`, `community`, `discovery`, `professionals`, `notifications` — their existing test files were read to confirm they exist and exercise real endpoints, not re-audited line by line for new IDOR gaps.
- **Privacy/redaction:** verified in `ai` (allowlist-only fields ever leave the process boundary; free-text/location excluded) and `privacy` (export payload scoped to the requesting user only).
- **Destructive-action safety:** verified in `privacy` (deletion is two-step, nothing destroys data on the first call) and `accounts` (anonymization, not hard deletion, preserving referential integrity).
- **Error handling / no internal leakage:** verified in `core` — every HTML and JSON error handler (400/401/403/404/405/429/500) tested directly, confirmed to never leak a traceback, file path, or secret.
- **Fallback/degradation safety:** verified in `ai` — provider failure, timeout, or missing configuration all degrade to the unchanged deterministic result rather than failing the request or silently fabricating an answer.

## Known gaps (see `TRACEABILITY-MATRIX.md` for full detail)

1. `locations` has 1 test for an entire geography app — thin, not expanded in this phase.
2. `animals`, `messaging`, `community`, `discovery`, `professionals`, `notifications` were not re-audited for new adversarial findings in this phase, only confirmed to have existing, passing test coverage.
3. Several Phase 2/3 backlog items are not implemented at all: blog CMS, appointments, saved profiles, analytics, disease surveillance, AI scribe/clinical guidance, advanced marketplace settlement, interoperability, model evaluation harness.
4. Module-specific admin consoles (verification queue UI, geography import, moderation console, content CMS, payments reconciliation, analytics dashboards) are not implemented — only their shared primitives (`audit`, `privacy`) are.
5. The frontend (`frontend/`) was not reviewed as part of this backend-focused certification. Its own `todo.md` shows its checklist essentially complete, but that's a self-report from a separate development track, not something this audit verified independently.

## Production readiness — infrastructure boundary

Every phase's handoff has flagged this consistently, and it remains true here: all verification in every phase (1–15) has run against SQLite, in-memory Channels, and — where relevant — mocked or offline-stub external providers (email console backend, `NoopProvider`/`ConsoleProvider` for AI, mocked ClickPesa webhook payloads). None of the phases have been verified against real PostgreSQL/PostGIS, real Redis, a real Celery worker/Beat process, real TLS termination, or real ClickPesa merchant credentials. This is the single largest gap between "the code is correct" (which this audit has real evidence for) and "the system is deployed and operating correctly" (which it does not).

## This sandbox's own limitation, stated plainly

Every phase from 12 onward, including this one, was built in a sandbox with no Django installation and no network access to install one. All code in this phase was reviewed and reasoned through carefully before being handed off, but not executed here. The operator has since run the full suite for real (see "Real verification result" above) and confirmed the `marketplace` tests specifically — added in this phase, previously unexecuted anywhere — pass against a real database.

## Recommendation

**Conditional pass.** The code, migrations, and test suite added across phases 12–15 are ready for the operator to run for real (commands below). Nothing in this phase's findings indicates a blocking defect — the one real bug found (`marketplace` serializer missing `id`) was fixed in the same phase it was found, not merely logged. The gaps listed above are scope gaps (features not built), not correctness gaps in what has been built. This is **not** a certification that the system is ready for production traffic — that requires the infrastructure boundary above to be closed first, which is explicitly outside a backend code audit's ability to certify.

## Verification the operator should run before treating this phase as certified

```
python manage.py makemigrations --check
python -m pytest -q
python manage.py check
python manage.py spectacular --file schema.yaml --validate
```

The full, repository-wide `pytest -q` (not scoped to one app) is the right command here — this phase's claims span every app's existing test suite, not just the new `marketplace` tests.
