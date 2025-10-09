# CI/CD
- GitHub Actions:
  - backend: ruff + mypy + pytest + coverage upload
  - frontend: npm ci + lint + test + build
  - docker build & push on main
- Environments: dev (local Docker), staging (VPS), prod (VPS/cloud)
- Secrets via repository settings
