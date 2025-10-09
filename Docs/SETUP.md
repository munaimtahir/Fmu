# Setup
## Prereqs
- Docker, Docker Compose, Python 3.12, Node 20
## Quick Start
1. `cp .env.example .env` (fill DB creds)
2. `docker compose up --build`
3. `docker exec -it sims_backend python manage.py migrate`
4. `docker exec -it sims_backend python manage.py createsuperuser`
5. Access API at http://localhost:8000 and UI at http://localhost:5173
