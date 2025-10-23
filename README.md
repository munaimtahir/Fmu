# FMU - Student Information Management System (SIMS)

[![Backend CI](https://github.com/munaimtahir/Fmu/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/munaimtahir/Fmu/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/munaimtahir/Fmu/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/munaimtahir/Fmu/actions/workflows/frontend-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/react-19-61dafb.svg)](https://reactjs.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive, production-ready Student Information Management System built with Django REST Framework and React.

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# Clone and start
git clone https://github.com/munaimtahir/Fmu.git
cd Fmu
cp .env.example .env

# Start all services
docker compose up -d

# Run migrations and seed demo data
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo --students 30

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# Admin Panel: http://localhost:8000/admin
```

### Using Makefile
```bash
make demo        # Setup and seed demo data
make test        # Run all tests
make lint        # Run all linters
make docker-up   # Start Docker services
```

## 📊 Status & Metrics

### Current Version
- **Production:** v1.0.0-prod ✅
- **Stable:** v1.1.0-stable ✅
- **Status:** ✅ Production-ready
- **Last Verified:** October 23, 2025

### Test Coverage
| Component | Tests | Coverage | Status |
|-----------|-------|----------|--------|
| Backend | 220 | 91% | ✅ PASS |
| Frontend | 26 | 100% | ✅ PASS |

### Quality Metrics
- ✅ All linters passing (ruff, mypy, eslint, tsc)
- ✅ All tests passing (220 backend, 26 frontend)
- ✅ CI/CD green
- ✅ Docker build successful
- ✅ Security scanning clean (CodeQL)
- ✅ Production deployment ready

## 📋 Overview

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
- API Authentication: http://localhost:8000/api/auth/token/
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

3. Configure environment variables (optional):
```bash
cp .env.example .env  # or create frontend/.env manually
```

4. Start development server:
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
- OpenAPI schema: http://localhost:8000/api/schema/
- JWT token obtain/refresh endpoints live under http://localhost:8000/api/auth/.

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `DJANGO_SECRET_KEY`: Django secret key (change in production!)
- `DJANGO_DEBUG`: Debug mode (True/False)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database credentials
- `REDIS_HOST`: Redis server host
- `CORS_ALLOWED_ORIGINS`: Allowed frontend origins

## Deployment

See [Docs/SETUP.md](Docs/SETUP.md) for detailed deployment instructions.
See [Docs/CI-CD.md](Docs/CI-CD.md) for CI/CD pipeline documentation.

## 📄 Documentation

Complete documentation is available in the [Docs/](Docs/) directory:

- **[Architecture](Docs/ARCHITECTURE.md)** - System design and components
- **[API Reference](Docs/API.md)** - Complete endpoint documentation  
- **[Data Model](Docs/DATAMODEL.md)** - Database schema and ERD
- **[Setup Guide](Docs/SETUP.md)** - Deployment and configuration
- **[Contributing](Docs/CONTRIBUTING.md)** - Contribution guidelines
- **[Changelog](Docs/CHANGELOG.md)** - Version history
- **[Tests](Docs/TESTS.md)** - Testing documentation
- **[CI/CD](Docs/CI-CD.md)** - Pipeline configuration

## 🎯 Demo Credentials

After running `make demo` or `python manage.py seed_demo`:

- **Admin:** admin / admin123
- **Faculty:** faculty / faculty123  
- **Student:** student / student123

## Contributing

Please read [Docs/CONTRIBUTING.md](Docs/CONTRIBUTING.md) for contribution guidelines.

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues, questions, or contributions:

- 📖 [Complete Documentation](Docs/)
- 🐛 [Issue Tracker](https://github.com/munaimtahir/Fmu/issues)
- 📧 Contact: munaimtahir@users.noreply.github.com

## License

See LICENSE file for details.

## Support

For issues and questions, please use the GitHub issue tracker.
