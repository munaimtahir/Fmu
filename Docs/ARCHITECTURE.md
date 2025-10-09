# Architecture
- Django REST API (sims_backend)
- React SPA (sims_frontend)
- Postgres DB
- Nginx reverse proxy
- Object storage for documents (local in dev; S3/minio later)
- Background jobs (Django-Q or RQ) for PDFs, backups, notifications
