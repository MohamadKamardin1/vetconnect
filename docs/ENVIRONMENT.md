# Environment and Deployment Variables

The service reads configuration from environment variables. `.env.example` is a non-secret template; production secrets must be injected by the deployment platform and must never be committed.

| Variable group | Required values |
|---|---|
| Django | `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_TIME_ZONE` |
| Database | `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_CONN_MAX_AGE` |
| Redis/Celery/Channels | `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `CHANNELS_BACKEND` |
| Browser security | `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `SECURE_SSL_REDIRECT`, cookie flags, HSTS |
| API controls | `API_PAGE_SIZE`, `API_ANON_RATE`, `API_USER_RATE` |

Production requires PostgreSQL with PostGIS and Redis. The default local settings use SQLite and eager Celery only for early development. Those defaults are not a production certification. The supplied Compose file provisions the intended integration topology when Docker is available.

## Foundation commands

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
python manage.py migrate
python manage.py check
python manage.py check --deploy
python manage.py spectacular --file schema.yaml --validate
pytest -q
```

The current sandbox does not have Docker, PostgreSQL, PostGIS, or Redis command-line tools installed. This is recorded in `HANDOFF-01.md` and remains a release-readiness dependency until a real integration environment is used.
