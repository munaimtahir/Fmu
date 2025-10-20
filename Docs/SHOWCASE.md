# FMU SIMS - Showcase & Demo Guide

## Overview

This document showcases the key features and capabilities of the FMU Student Information Management System (SIMS) as of Stage 3 development (v0.3.0-beta).

## System Architecture

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Frontend  │─────▶│   Backend    │─────▶│ PostgreSQL │
│   (React)   │      │   (Django)   │      │            │
└─────────────┘      └──────────────┘      └────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    Redis     │
                     │              │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  RQ Worker   │
                     │ (Background) │
                     └──────────────┘
```

## Key Features

### 1. Core Academic Management
- **Students:** Complete CRUD with search, filtering, and pagination
- **Programs:** Academic program management
- **Courses:** Course catalog with credit hours
- **Sections:** Course sections with enrollment capacity
- **Enrollment:** Student-section binding with business rules

### 2. Attendance Tracking
- Daily attendance marking
- Automatic eligibility calculation (75% threshold)
- Section-wide attendance summaries
- Missing/present status tracking

**API Endpoints:**
```bash
# Mark attendance
POST /api/attendance/
{
  "section": 1,
  "student": 1,
  "date": "2024-01-15",
  "is_present": true
}

# Check eligibility
GET /api/attendance/eligibility/?student_id=1&section_id=1
```

### 3. Assessment & Grading
- Multiple assessment types (quiz, assignment, midterm, final)
- Weighted score calculation
- Grade computation (A+, A, B+, etc.)
- Component tracking

**Example:**
```bash
# Create assessment
POST /api/assessments/
{
  "section": 1,
  "type": "midterm",
  "weight": 30,
  "max_score": 100
}

# Record score
POST /api/assessment-scores/
{
  "assessment": 1,
  "student": 1,
  "score": 85,
  "max_score": 100
}
```

### 4. Results Management
- Publish/freeze workflow
- Dual-approval audit trail
- Grade finalization
- Pending change requests

### 5. Transcript Generation
- PDF transcript generation with QR verification
- Background job processing for bulk generation
- Email delivery integration
- 48-hour token validity

**API Endpoints:**
```bash
# Synchronous generation
GET /api/transcripts/123/

# Asynchronous generation
POST /api/transcripts/enqueue/
{
  "student_id": 123,
  "email": "student@example.com"
}

# Verify transcript
GET /api/transcripts/verify/transcript_123:abc123...
```

### 6. Request Tickets
- Bonafide certificate requests
- Transcript requests
- NOC (No Objection Certificate) requests
- Status tracking (pending, approved, rejected, completed)

### 7. Audit Logging
- All write operations logged
- Actor tracking
- Timestamp recording
- Request details captured

### 8. Health Monitoring
- Component-level health checks
- Database connection status
- Redis/RQ queue status
- Degraded state detection

**Health Check Response:**
```json
{
  "status": "ok",
  "service": "SIMS Backend",
  "components": {
    "database": "ok",
    "redis": "ok",
    "rq_queue": "ok"
  }
}
```

## Demo Workflow

### Setup
1. Clone and start services:
   ```bash
   git clone https://github.com/munaimtahir/Fmu.git
   cd Fmu
   docker compose up -d
   ```

2. Run migrations and create superuser:
   ```bash
   docker exec -it sims_backend python manage.py migrate
   docker exec -it sims_backend python manage.py createsuperuser
   ```

3. Access the system:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - API Docs: http://localhost:8000/api/docs

### Demo Scenarios

#### Scenario 1: Student Enrollment
```bash
# 1. Create a student
POST /api/students/
{
  "reg_no": "STU-2024-001",
  "name": "Alice Johnson",
  "program": "BS Computer Science",
  "status": "active"
}

# 2. Enroll in section
POST /api/enrollments/
{
  "student": 1,
  "section": 1,
  "status": "enrolled"
}

# 3. Verify enrollment
GET /api/enrollments/?student=1
```

#### Scenario 2: Attendance & Eligibility
```bash
# 1. Mark attendance (10 days)
for i in {1..10}; do
  POST /api/attendance/ {
    "section": 1,
    "student": 1,
    "date": "2024-01-$i",
    "is_present": true
  }
done

# 2. Check eligibility
GET /api/attendance/eligibility/?student_id=1&section_id=1

# Response:
{
  "eligible": true,
  "percentage": 100.0,
  "threshold": 75.0,
  "total_classes": 10,
  "present": 10,
  "absent": 0
}
```

#### Scenario 3: Assessment & Grading
```bash
# 1. Create assessments
POST /api/assessments/
[
  {"section": 1, "type": "quiz", "weight": 10},
  {"section": 1, "type": "assignment", "weight": 20},
  {"section": 1, "type": "midterm", "weight": 30},
  {"section": 1, "type": "final", "weight": 40}
]

# 2. Record scores
POST /api/assessment-scores/
{"assessment": 1, "student": 1, "score": 90, "max_score": 100}

# 3. Calculate final grade
GET /api/results/calculate/?student_id=1&section_id=1
```

#### Scenario 4: Transcript Generation
```bash
# 1. Enqueue transcript job
POST /api/transcripts/enqueue/
{
  "student_id": 1,
  "email": "student@example.com"
}

# Response:
{
  "message": "Transcript generation job enqueued",
  "job_id": "abc123...",
  "student_id": 1
}

# 2. Check worker logs
docker compose logs -f rqworker

# 3. Download transcript
GET /api/transcripts/1/
```

## API Documentation

### Authentication
All endpoints require JWT authentication except health check.

```bash
# Obtain token
POST /api/auth/token/
{
  "username": "admin",
  "password": "password"
}

# Use token
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/students/
```

### Endpoints Overview
- **Students:** `/api/students/` (CRUD, search, filter)
- **Programs:** `/api/programs/` (CRUD)
- **Courses:** `/api/courses/` (CRUD)
- **Sections:** `/api/sections/` (CRUD)
- **Enrollments:** `/api/enrollments/` (CRUD, filter by student/section)
- **Attendance:** `/api/attendance/` (CRUD, eligibility, summaries)
- **Assessments:** `/api/assessments/` (CRUD)
- **Assessment Scores:** `/api/assessment-scores/` (CRUD)
- **Results:** `/api/results/` (CRUD, publish, freeze)
- **Transcripts:** `/api/transcripts/` (generate, verify, enqueue)
- **Requests:** `/api/requests/` (CRUD, status tracking)

### Interactive Documentation
- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

## Testing & Quality

### Backend
- **220 tests** passing
- **99% coverage** achieved
- All linting checks passing (ruff, mypy)

### Frontend
- **7 tests** passing
- **92.5% coverage** achieved
- ESLint checks passing

### Security
- CodeQL analysis configured
- Trivy scanning enabled
- Dependency review automated

## CI/CD Pipeline

```
┌─────────────┐
│   Push/PR   │
└─────┬───────┘
      │
      ├──────▶ Backend CI
      │        ├── Lint (ruff)
      │        ├── Type Check (mypy)
      │        └── Test (pytest ≥80%)
      │
      ├──────▶ Frontend CI
      │        ├── Lint (ESLint)
      │        ├── Test (Vitest ≥50%)
      │        └── Build
      │
      ├──────▶ Security
      │        ├── CodeQL
      │        ├── Trivy
      │        └── Dependency Review
      │
      └──────▶ Release (on tag)
               ├── Build Artifacts
               ├── Create Release
               └── Upload Assets
```

## Demo Data

Seed data available in `backend/seed/`:
- Demo students
- Sample programs
- Test courses
- Example sections

**Load seed data:**
```bash
docker exec -it sims_backend python manage.py loaddata seed/demo_students.json
```

## Future Enhancements

### Stage 4 Preview
- Complete frontend with authentication
- CRUD screens for all modules
- Dashboard with real-time statistics
- Mobile-responsive design
- Advanced reporting
- Email notifications
- Bulk operations

## Support & Documentation

- **README:** Complete setup instructions
- **API Docs:** Auto-generated OpenAPI documentation
- **Data Model:** ERD and relationship diagrams
- **Operations:** Runbook for deployment and maintenance
- **CI/CD:** Automated pipeline documentation

## Conclusion

FMU SIMS v0.3.0-beta represents a solid foundation for academic management with:
- ✅ Complete backend API (99% tested)
- ✅ Basic frontend dashboard
- ✅ Background job processing
- ✅ Security scanning
- ✅ Automated CI/CD
- ✅ Comprehensive documentation

Ready for Stage 4 development focusing on frontend expansion and advanced features.
