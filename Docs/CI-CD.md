# CI/CD

    ## Gates
    - Backend: ruff + black + isort + mypy + pytest (>=80%)
    - Frontend: eslint + prettier + typecheck + vitest (>=70%)
    - Build Docker images and run a smoke test.
    - Trivy scan images, CodeQL analysis.

    ## Release
    - Tag `vX.Y.Z` → build & push images; create GitHub Release.
    - Attach CHANGELOG excerpt.
