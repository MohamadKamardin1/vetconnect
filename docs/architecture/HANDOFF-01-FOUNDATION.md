# HANDOFF-01-FOUNDATION — Django Infrastructure

## Result

The Prompt 01 foundation is complete. The repository now contains a runnable Django/DRF/ASGI/Celery project skeleton with versioned API routing, OpenAPI/Swagger, health/readiness endpoints, standardized JSON API error handling, safe HTML error templates, environment-driven security settings, Compose infrastructure, and reproducible test configuration.

## Verification evidence

| Check | Result |
|---|---|
| `python manage.py migrate --plan` | Passed |
| `python manage.py check` | Passed |
| Production-like `python manage.py check --deploy` with secure overrides | Passed with zero issues |
| `python manage.py spectacular --file schema.yaml --validate` | Passed |
| `pytest -q` | **4 passed** |
| `pytest -q --cov=core --cov-report=term-missing` | **4 passed; core coverage 67%** |

The test suite covers public health, database readiness, API 404 envelope, and safe HTML 404 behavior. The global exception handler, deployment-like settings, and OpenAPI generation are in place for later domains to extend.

## Known exception

The current sandbox lacks Docker, PostgreSQL/PostGIS, and Redis command-line tools. The repository includes `docker-compose.yml` with PostGIS and Redis services, but real integration verification against those services remains pending. SQLite is used only for the initial foundation test configuration and must not be used as evidence of production geospatial readiness.

## Next-phase contract

Prompt 02 must create the custom user model before any domain app migration, use the shared API/error conventions, implement roles as multi-role assignments, add object-level permission primitives, and prove every role's authentication and authorization flows with tests.
