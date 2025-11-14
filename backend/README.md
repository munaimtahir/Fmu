# sims_backend (Django)

Student Information Management System - Backend API

## Tech Stack
- Python 3.12
- Django 5.1.4
- Django REST Framework 3.15.2
- PostgreSQL 14+
- Redis (for background jobs)

## Setup for Development

### Local Development (without Docker)

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (create a `.env` file in the root):
```bash
cp ../.env.example ../.env
# Edit the .env file with your local settings
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

### Docker Development

See the main README and docker-compose.yml in the root directory.

## Project Structure

```
backend/
├── sims_backend/       # Main Django project settings
├── core/               # Core app with base models and utilities
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── pytest.ini          # Pytest configuration
└── pyproject.toml      # Ruff and mypy configuration
```

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=. --cov-report=html
```

## Code Quality

Lint with ruff:
```bash
ruff check .
```

Type check with mypy:
```bash
mypy .
```

## API Documentation

API documentation will be available at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Admin Interface

Django admin is available at: http://localhost:8000/admin/

## Production Configuration

Set the `DJANGO_ENV` environment variable to `production` for deployments. In
this mode the application will:

- Require `DJANGO_SECRET_KEY` and fail fast if it is missing.
- Reject accidental `DEBUG=True` settings.
- Enforce a non-empty `DJANGO_ALLOWED_HOSTS` list.
- Enable HTTPS-only cookie and redirect behaviours.

When running behind a reverse proxy (for example nginx or a load balancer)
ensure that it forwards the `X-Forwarded-Proto` header so Django can honour the
`SECURE_PROXY_SSL_HEADER` setting.
