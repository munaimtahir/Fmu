# Environment Variables (Truth Table)

    | Name | Type | Default | Required | Scope | Notes |
    |------|------|---------|----------|-------|-------|
    | `DJANGO_DEBUG` | bool | `True` | yes (dev) | backend | `False` for production |
    | `DJANGO_SECRET_KEY` | string | _none_ | yes | backend | Use a strong secret in prod |
    | `DJANGO_ALLOWED_HOSTS` | csv | `localhost,127.0.0.1` | yes | backend | e.g. `app.fmu.edu.pk` |
    | `DB_ENGINE` | string | `django.db.backends.postgresql` | yes | backend | Database engine |
    | `DB_NAME` | string | `sims_db` | yes | backend | Database name |
    | `DB_USER` | string | `sims_user` | yes | backend | Database user |
    | `DB_PASSWORD` | string | `sims_password` | yes | backend | Database password |
    | `DB_HOST` | string | `localhost` | yes | backend | Database host |
    | `DB_PORT` | string | `5432` | yes | backend | Database port |
    | `REDIS_HOST` | string | `localhost` | yes | backend | Redis host for RQ |
    | `REDIS_PORT` | string | `6379` | yes | backend | Redis port |
    | `EMAIL_BACKEND` | string | `console` | no | backend | Email backend type |
    | `EMAIL_HOST` | string | `smtp.gmail.com` | no | backend | SMTP host |
    | `EMAIL_USER` | string | _none_ | no | backend | SMTP user |
    | `EMAIL_PASS` | string | _none_ | no | backend | SMTP password |
    | `CORS_ALLOWED_ORIGINS` | csv | `http://localhost:5173` | yes | backend | CORS allow-list |
    | `VITE_API_BASE_URL` | url | `http://localhost:8000` | yes | frontend | Backend API URL |

    - Keep secrets out of the repo. Use `.env` locally; use Docker/CI secrets in prod.
    - See `.env.example` for a complete template with all variables.
