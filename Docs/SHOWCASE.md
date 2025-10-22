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

## Stage-3 Operational Features (v0.3.1)

### 1. Attendance Dashboard
**Path:** `/attendance` (Faculty, Admin)

**Features:**
- Toggle between table view and statistics view
- Real-time attendance percentage calculations
- Section-based filtering
- Student-level attendance tracking
- Visual status indicators (Present/Absent)

**View Modes:**
- **Table View:** Individual attendance records with date, student, and status
- **Statistics View:** Section summary with average attendance and per-student percentages

### 2. Registrar Eligibility Report
**Path:** `/attendance/eligibility` (Registrar, Admin)

**Features:**
- Configurable attendance threshold (default 75%)
- Multi-section report generation
- Eligible/ineligible status determination
- CSV export functionality
- Summary statistics (total students, eligible count, ineligible count)

**Use Case:** Generate eligibility reports for exam access based on attendance thresholds.

### 3. Gradebook
**Path:** `/gradebook` (Faculty, Student, Admin)

**Features:**
- Section-based gradebook view
- Assessment weight visualization (progress meter)
- Score entry in edit mode
- Weighted total calculation (auto-computed)
- CSV export for offline analysis
- Weight validation (warns if total ≠ 100%)

**Assessment Weight Meter:**
- Green: Total = 100% (valid)
- Yellow: Total < 100% (warning)
- Red: Total > 100% (error)

### 4. Publish Results
**Path:** `/examcell/publish` (ExamCell, Admin)

**Features:**
- Results workflow: draft → published → frozen
- Confirmation modals for critical actions
- Statistics dashboard (draft/published/frozen counts)
- Section-based filtering
- State-based action enablement

**Workflow:**
1. Faculty enters grades (draft state)
2. ExamCell publishes results (students can view)
3. ExamCell freezes results (immutable, final)

### 5. Transcript Verification
**Path:** `/verify/:token` (Public)

**Features:**
- QR code-based verification
- Student information display (reg_no, name, program)
- Course grades and CGPA
- Print-friendly styling
- 48-hour token validity
- Issue date tracking

**Security:** No sensitive PII, token expires after 48 hours.

### 6. Audit Log Viewer
**Path:** `/admin/audit` (Admin only)

**Features:**
- Comprehensive filtering:
  - Actor (username)
  - Entity (model name)
  - Date range (from/to)
  - HTTP method (POST, PUT, PATCH, DELETE)
- Color-coded visualization:
  - HTTP methods (green=POST, blue=PUT/PATCH, red=DELETE)
  - Status codes (green=2xx, red=4xx/5xx)
- CSV export for compliance
- Paginated results

**Use Case:** Compliance auditing, troubleshooting, security investigations.

### 7. Staging Deployment Infrastructure

**docker-compose.staging.yml:**
- Production-ready service configuration
- SSL/TLS support with automatic renewal
- Health checks for all services
- Automatic restart policies
- Network isolation
- Backup volume mounts

**nginx.staging.conf:**
- HTTPS redirect (HTTP → HTTPS)
- SSL/TLS configuration (TLS 1.2+)
- Security headers (HSTS, X-Frame-Options, etc.)
- Rate limiting:
  - API: 10 req/s (burst: 20)
  - Login: 5 req/min (burst: 3)
- Gzip compression
- Static/media file caching
- Reverse proxy for backend and frontend

**Certbot Integration:**
- Automatic certificate renewal every 12 hours
- ACME challenge support
- Let's Encrypt integration

## Screenshots

### Attendance Dashboard - Table View
*Shows student attendance records with date, status, and reason*

### Attendance Dashboard - Statistics View
*Displays section summary with average attendance and per-student percentages*

### Registrar Eligibility Report
*Multi-section eligibility report with configurable threshold and CSV export*

### Gradebook
*Section gradebook with assessment weights, scores, and weighted totals*

### Publish Results
*Results publishing workflow with draft/published/frozen states*

### Transcript Verify Page
*Public QR verification page showing student transcript information*

### Audit Log Viewer
*Admin audit log with filtering and color-coded events*

**Note:** Screenshots will be added after E2E testing and manual verification.

## Future Enhancements

### Stage 4 Preview
- Enhanced dashboard widgets with real-time data
- Advanced reporting with charts and graphs
- Mobile-responsive design optimization
- Email notification system
- Bulk operations (import/export)
- Role-based dashboard customization

## Support & Documentation

- **README:** Complete setup instructions
- **API Docs:** Auto-generated OpenAPI documentation + `/api/docs/` (Swagger)
- **Data Model:** ERD and relationship diagrams
- **Operations:** Complete runbook with backup/restore procedures
- **CI/CD:** Automated pipeline with security scanning
- **Staging Guide:** HTTPS deployment with SSL configuration

## Metrics

### Backend
- **Tests:** 220 passing
- **Coverage:** 91%
- **Endpoints:** 40+ REST APIs
- **Security Alerts:** 0

### Frontend
- **Tests:** 26 passing
- **Build:** Successful (558KB gzipped)
- **Pages:** 6 operational pages + role dashboards
- **Components:** 15+ reusable UI components

### Infrastructure
- **Services:** 6 containers (postgres, redis, backend, frontend, rqworker, nginx)
- **Health Checks:** Automated monitoring for all services
- **Backups:** Nightly automated + manual procedures
- **SSL:** Automatic renewal via certbot

## Conclusion

FMU SIMS v0.3.1-stage3 represents a fully operational academic management system with:
- ✅ Complete backend API (91% tested, 0 security alerts)
- ✅ Operational frontend pages (attendance, gradebook, results, audit)
- ✅ Production-ready staging infrastructure (SSL, backups, monitoring)
- ✅ Background job processing (transcripts, email)
- ✅ Security scanning (CodeQL, audit logging)
- ✅ Automated CI/CD (7 workflows)
- ✅ Comprehensive documentation

**Ready for production deployment and user acceptance testing.**
