# Setup

    This document shows how to run the project in three modes:
    - Local (bare Python/Node)
    - Docker (recommended for dev)
    - Production (Docker + Nginx + SSL)

    ## Prerequisites
    - Python 3.11+
    - Node 18+
    - Docker & Docker Compose v2
    - GNU Make (optional but recommended)

    ## Quick Start (Docker, Dev)
    ```bash
    cp .env.example .env  # update values
    docker compose up --build -d
    docker compose exec backend python manage.py migrate
    docker compose exec backend python manage.py createsuperuser
    ```

    Backend: http://localhost:8000  
    Frontend: http://localhost:3000  
    Admin: http://localhost:8000/admin  
    API Docs: http://localhost:8000/api/docs and /api/redoc

    ## Local (no Docker)
    ```bash
    # Backend
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env && python manage.py migrate && python manage.py runserver

    # Frontend
    cd frontend
    npm install
    npm run dev
    ```

    ## Production (single VM)
    - Set `DEBUG=0` and proper `ALLOWED_HOSTS`
    - Configure Nginx reverse proxy (see DEPLOYMENT_TARGETS.md)
    - Use systemd or docker compose to keep services running
    - Add backups and monitoring (see OPERATIONS.md)
