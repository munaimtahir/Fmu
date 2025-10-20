# CI/CD Overview

This repository includes two automated CI pipelines to validate code quality on every push and pull request.

## Backend CI (`.github/workflows/backend-ci.yml`)
- **Ruff** enforces formatting and linting on every push/pull request that touches the backend.
- **mypy** provides static type coverage for the Django project using the configured stubs.
- **pytest** runs against a temporary SQLite database and produces HTML and XML coverage reports that are published as workflow artifacts.

## Frontend CI (`.github/workflows/frontend-ci.yml`)
- Runs on pushes and pull requests that touch the frontend codebase.
- Uses Node 20 with cached dependencies to execute `npm ci`, `npm run lint`, `npm test`, and `npm run build` in sequence.
- Publishes the production build from `dist/` as a downloadable artifact for reviewers.

## Environment Deployment
- **Development**: Run locally via Docker Compose (`docker-compose.yml`).
- **Production**: Build Docker images locally and deploy to your VPS or cloud environment of choice.
  - Store environment-specific secrets (database credentials, Django secret key, JWT signing key, etc.) securely in your deployment environment.

## Secrets Management
- Configure secrets from **Repository Settings → Secrets and variables → Actions**.
- Suggested secrets include `DJANGO_SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, and any credentials needed for staging/production services.
- Use environment-specific secrets (e.g., `STAGING_DB_URL`, `PROD_DB_URL`) alongside protected workflow environments to control deployments.

These pipelines ensure that every commit and merge maintains application integrity while providing a clear promotion path from development to production.
