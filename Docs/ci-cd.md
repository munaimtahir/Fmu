# CI/CD Overview

This repository ships three automated pipelines designed to keep the application healthy from commit through deployment.

## Backend CI (`.github/workflows/backend-ci.yml`)
- **Ruff** enforces formatting and linting on every push/pull request that touches the backend.
- **mypy** provides static type coverage for the Django project using the configured stubs.
- **pytest** runs against a temporary SQLite database and produces HTML and XML coverage reports that are published as workflow artifacts.

## Frontend CI (`.github/workflows/frontend-ci.yml`)
- Runs on pushes and pull requests that touch the frontend codebase.
- Uses Node 20 with cached dependencies to execute `npm ci`, `npm run lint`, `npm test`, and `npm run build` in sequence.
- Publishes the production build from `dist/` as a downloadable artifact for reviewers.

## Docker Release (`.github/workflows/docker-release.yml`)
- Builds and pushes versioned images for the backend and frontend Dockerfiles whenever `main` is updated.
- Images are tagged for the branch, commit SHA, and `latest`, and are published to GitHub Container Registry (`ghcr.io`).
- Requires no additional credentials beyond the built-in `GITHUB_TOKEN`, but a custom token can be configured if registry policies require it.

## Environment Promotion
- **Development**: Run locally via Docker Compose (`docker-compose.yml`).
- **Staging/Production**: Deploy from the published container images to the VPS or cloud environment of choice.
  - Store environment-specific secrets (database credentials, Django secret key, JWT signing key, etc.) in GitHub repository secrets or organization secrets.
  - Reference those secrets in deployment workflows or infrastructure tooling when promoting the latest container images.

## Secrets Management
- Configure secrets from **Repository Settings → Secrets and variables → Actions**.
- Suggested secrets include `DJANGO_SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, and any credentials needed for staging/production services.
- Use environment-specific secrets (e.g., `STAGING_DB_URL`, `PROD_DB_URL`) alongside protected workflow environments to control deployments.

These pipelines ensure that every commit and merge maintains application integrity while providing a clear promotion path from development to production.
