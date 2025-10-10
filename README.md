# FMU - Student Information Management System (SIMS)

A comprehensive Student Information Management System built with Django REST Framework and React.

## Overview

SIMS is a production-ready academic digitization system designed to manage:
- Universities, Colleges, Departments, Programs
- Student admissions, enrollments, and records
- Course management and term scheduling
- Attendance tracking and eligibility computation
- Assessment schemes and results management
- Transcript generation with QR code verification
- Document management and verification
- Request ticket system (bonafide certificates, transcripts, etc.)

## Tech Stack

### Backend
- Python 3.12
- Django 5.1.4 + Django REST Framework
- PostgreSQL 14+
- Redis (for background jobs)
- JWT Authentication

### Frontend
- React 18
- Vite (build tool)
- Modern ES6+ JavaScript

### Infrastructure
- Docker & Docker Compose
- Nginx (reverse proxy)
- GitHub Actions (CI/CD)

## Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)
- Node.js 20+ (for local development)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/munaimtahir/Fmu.git
cd Fmu
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration (optional for development)
```

3. Start all services:
```bash
docker compose up --build
```

4. Run initial migrations (in a new terminal):
```bash
docker exec -it sims_backend python manage.py migrate
```

5. Create a superuser:
```bash
docker exec -it sims_backend python manage.py createsuperuser
```

6. Access the application:
- Frontend UI: http://localhost:5173
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- Full stack via Nginx: http://localhost

## Local Development Setup

### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

## Project Structure

```
Fmu/
├── backend/                    # Django backend
│   ├── sims_backend/          # Django project settings
│   ├── core/                  # Core app
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend Docker config
│   └── pytest.ini             # Test configuration
├── frontend/                   # React frontend
│   ├── src/                   # Source files
│   ├── public/                # Static files
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   └── Dockerfile             # Frontend Docker config
├── nginx/                      # Nginx configuration
│   ├── nginx.conf             # Main config
│   └── conf.d/                # Site configs
├── Docs/                       # Documentation
│   ├── FINAL_AI_DEVELOPER_PROMPT.md
│   ├── ARCHITECTURE.md
│   ├── DATAMODEL.md
│   ├── API.md
│   ├── SETUP.md
│   └── ...
├── docker-compose.yml          # Docker services
├── .env.example               # Environment template
└── README.md                  # This file
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

With coverage:
```bash
pytest --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Code Quality

### Backend
```bash
cd backend

# Lint with ruff
ruff check .

# Type check with mypy
mypy .
```

### Frontend
```bash
cd frontend

# Lint with ESLint
npm run lint
```

## API Documentation

Once the backend is running, API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `DJANGO_SECRET_KEY`: Django secret key (change in production!)
- `DJANGO_DEBUG`: Debug mode (True/False)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database credentials
- `REDIS_HOST`: Redis server host
- `CORS_ALLOWED_ORIGINS`: Allowed frontend origins

## Deployment

See `Docs/CI-CD.md` for CI/CD and deployment instructions.

## Contributing

Please read `Docs/CONTRIBUTING.md` for contribution guidelines.

## License

See LICENSE file for details.

## Support

For issues and questions, please use the GitHub issue tracker.
