# VetKonect Tanzania/Zanzibar Backend

This repository contains the versioned Django/DRF backend for VetKonect Tanzania and Zanzibar. It is being implemented in the ordered Prompt 01–15 sequence defined by the project specification package.

## Current phase

The infrastructure foundation is complete. Identity/RBAC is the next implementation phase. See `docs/architecture/IMPLEMENTATION-TODO.md` and `docs/architecture/COMPLETION-MEMORY.md` for the live ledger.

## Setup

```bash
cp .env.example .env
python -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
python manage.py migrate
python manage.py runserver
```

For PostgreSQL/PostGIS and Redis, use `docker compose up --build` after Docker is available. The current sandbox uses SQLite for foundation tests only.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `/health/` | Public liveness response |
| `/readiness/` | Database readiness response |
| `/api/v1/schema/` | OpenAPI schema |
| `/api/v1/docs/` | Swagger UI |
| `/admin/` | Django administration, restricted by Django permissions |

## Verification

```bash
pytest -q
python manage.py check
python manage.py spectacular --file schema.yaml --validate
python manage.py check --deploy
```

Production readiness is not declared until the real PostgreSQL/PostGIS and Redis topology is provisioned, all ordered domain phases are implemented, and the final release-certification report contains real test and coverage evidence.
