# Environment Variables (Truth Table)

    | Name | Type | Default | Required | Scope | Notes |
    |------|------|---------|----------|-------|-------|
    | `DEBUG` | bool | `1` | yes (dev) | backend | `0` for production |
    | `SECRET_KEY` | string | _none_ | yes | backend | Use a strong secret in prod |
    | `ALLOWED_HOSTS` | csv | `localhost,127.0.0.1` | yes | backend | e.g. `app.fmu.edu.pk` |
    | `DATABASE_URL` | url | `postgres://...` | yes | backend | Use managed Postgres in prod |
    | `REDIS_URL` | url | `redis://redis:6379/0` | no | backend | For cache/queues |
    | `EMAIL_HOST` | string | _none_ | no | backend | SMTP host |
    | `EMAIL_USER` | string | _none_ | no | backend | SMTP user |
    | `EMAIL_PASS` | string | _none_ | no | backend | SMTP password |
    | `FRONTEND_URL` | url | `http://localhost:3000` | yes | both | CORS/links |
    | `DJANGO_ALLOWED_CIDR` | csv | _none_ | no | backend | Optional IP allow-list |
    | `SENTRY_DSN` | url | _none_ | no | both | Error tracking |

    - Keep secrets out of the repo. Use `.env` locally; use Docker/CI secrets in prod.
