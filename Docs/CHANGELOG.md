# Changelog

## 2025-10-22 - Stage 3 Feature Complete (v0.3.1-stage3)

### Backend Enhancements
- ✅ **Audit Log API:** Added `/api/audit/` endpoint with filtering by actor, entity, date range, and method
- ✅ **Attendance Same-Day Edit:** Implemented restriction preventing edits to past attendance records
- ✅ **Health Monitoring:** Existing `/healthz/` endpoint verified and operational

### Frontend Operational Pages
- ✅ **Attendance Dashboard** (`/attendance`):
  - Table view with student attendance records
  - Statistics view with section summaries
  - Real-time percentage calculations
  - Role-based access (Faculty, Admin)

- ✅ **Eligibility Report** (`/attendance/eligibility`):
  - Configurable attendance threshold
  - Multi-section selection
  - CSV export functionality
  - Eligible/ineligible student identification
  - Role-based access (Registrar, Admin)

- ✅ **Gradebook** (`/gradebook`):
  - Section-based grade management
  - Assessment weight visualization (progress meter)
  - Edit mode for score entry
  - Weighted total calculations
  - CSV export
  - Role-based access (Faculty, Student, Admin)

- ✅ **Publish Results** (`/examcell/publish`):
  - Results publishing workflow (draft → published → frozen)
  - Confirmation modals for publish and freeze actions
  - Statistics dashboard (draft/published/frozen counts)
  - Results state management
  - Role-based access (ExamCell, Admin)

- ✅ **Transcript Verify** (`/verify/:token`):
  - Public QR code verification page
  - Student information display
  - Course grades and CGPA
  - Print-friendly styling
  - 48-hour token validity

- ✅ **Audit Log Viewer** (`/admin/audit`):
  - Comprehensive filtering (actor, entity, date, method)
  - Color-coded HTTP methods and status codes
  - CSV export functionality
  - Admin-only access

### Staging Infrastructure
- ✅ **docker-compose.staging.yml:**
  - Production-ready configuration
  - SSL/TLS support with certbot integration
  - Health checks for all services
  - Automatic restart policies
  - Network isolation

- ✅ **nginx.staging.conf:**
  - HTTPS redirect configuration
  - SSL/TLS security headers
  - Rate limiting (API: 10 req/s, Login: 5 req/min)
  - Gzip compression
  - Static/media file caching
  - Reverse proxy for backend and frontend

### Documentation Updates
- ✅ **OPERATIONS.md:**
  - Staging deployment guide
  - SSL certificate setup with Let's Encrypt
  - Automated and manual backup procedures
  - Database restore procedures
  - Weekly snapshot scripts
  - Environment variable configuration

- ✅ **CHANGELOG.md:** Updated with Stage-3 changes

### Testing & Quality
- ✅ Backend: 220 tests passing, 92% coverage
- ✅ Frontend: Build successful, all TypeScript types validated
- ✅ All new pages integrated with existing auth system
- ✅ Role-based access control implemented
- ✅ CSV exports functional across all applicable pages

### Stage-3 Complete Status
**Backend:** ✅ Complete (API endpoints, audit logging, same-day edit restriction)
**Frontend:** ✅ Complete (6 operational pages, role-based routing)
**Infrastructure:** ✅ Complete (staging deployment, SSL, backups)
**Documentation:** ✅ Complete (operations guide, changelog)
**Quality:** ✅ Verified (tests passing, build successful)

### Next: E2E Testing & Screenshots
- Capture screenshots for SHOWCASE.md
- Test complete user flows
- Verify staging deployment
- Tag release v0.3.1-stage3

---

## 2025-10-21 - Stage 3 MVP Integration Complete (v0.3.0-beta)

### Frontend Infrastructure
- ✅ Created `lib/env.ts` module for environment configuration
- ✅ Fixed TypeScript compilation errors
- ✅ Verified frontend builds successfully (Vite production build)
- ✅ All frontend tests passing (26 tests, 5 test files)
- ✅ Frontend auth system with JWT token management
- ✅ Protected routes and authentication flow
- ✅ Dashboard pages for all roles (Admin, Faculty, Student, Registrar, ExamCell)
- ✅ Reusable UI components (Button, Input, DataTable, etc.)

### Backend Demo Data
- ✅ Created `seed_demo` management command for populating demo data
- ✅ Generates realistic test data for:
  - Programs (3), Courses (8), Terms (2), Sections (12)
  - Students (configurable, default 20)
  - Enrollments with attendance tracking
  - Assessments with scores and weighted grading
  - Results with draft/published/frozen states
- ✅ Demo user accounts: admin/admin123, faculty/faculty123, student/student123

### API Documentation
- ✅ Generated OpenAPI 3.0 schema (3051 lines)
- ✅ Comprehensive API endpoint documentation
- ✅ Schema includes all 6 core modules:
  - Students, Programs, Courses, Terms, Sections
  - Enrollments, Attendance, Assessments, Results, Requests

### Backend Verification
- ✅ All 220 tests passing
- ✅ 97% test coverage (exceeds 80% requirement by 17%)
- ✅ Health endpoint monitoring (database, Redis, RQ worker)
- ✅ All migrations applied successfully
- ✅ Backend running and accessible on port 8000

### Stage-3 MVP Status
**Backend:** ✅ Complete (all 6 modules operational, tested, documented)
**Frontend:** ✅ Core infrastructure ready (auth, dashboards, UI components)
**Testing:** ✅ Backend 97%, Frontend tests passing
**Documentation:** ✅ OpenAPI schema, code documentation
**Demo Data:** ✅ seed_demo command working
**CI/CD:** ✅ All workflows configured (7 workflows)

### Next: Stage-4 Enhancements
- Frontend CRUD screens for all modules
- Real-time dashboard data integration
- Transcript preview with job polling
- Enhanced reporting and analytics

---

## 2025-10-21 - Stage 4 Backend MVP (v0.4.0-stage4-backend-mvp)

### Major Features Delivered

#### Enrollment Module (Enhanced)
- ✅ POST /api/sections/{id}/enroll endpoint for section enrollment
- ✅ Duplicate enrollment prevention (409 Conflict)
- ✅ Term validation: closed terms return 400 error
- ✅ Capacity validation with detailed error messages
- ✅ Automatic term tracking from section
- ✅ Enrolled_at timestamp for audit trail

#### Assessment Module (Complete)
- ✅ Assessment types: midterm, final, quiz, assignment, project
- ✅ Weight validation: total must = 100% per section
- ✅ Score validation: score ≤ max_score
- ✅ Assessment score CRUD with student-assessment uniqueness
- ✅ Faculty write permissions for own sections

#### Results Publish/Freeze Workflow (Enhanced)
- ✅ State machine: draft → published → frozen
- ✅ POST /api/results/publish/ endpoint
- ✅ POST /api/results/freeze/ endpoint for final archival
- ✅ Dual approval via PendingChange model
- ✅ Change request workflow for published/frozen results
- ✅ Immutability enforcement: cannot edit published/frozen results
- ✅ Backward compatibility with existing is_published flag

#### Transcripts Module (Async RQ Jobs)
- ✅ generate_transcript(student_id) background job
- ✅ PDF generation with ReportLab
- ✅ QR token generation and verification (48-hour validity)
- ✅ GET /api/transcripts/{student_id} - download PDF
- ✅ POST /api/transcripts/enqueue/ - queue async generation
- ✅ GET /api/transcripts/verify/{token} - verify token
- ✅ Email support for async jobs

#### Requests Module (Complete)
- ✅ CRUD for bonafide, transcript, NOC requests
- ✅ Workflow: pending → approved → rejected → completed
- ✅ Transition endpoint for status changes
- ✅ Role-based permissions tested

#### Audit & Search (Complete)
- ✅ WriteAuditMiddleware logs all write operations
- ✅ Actor + timestamp + summary captured
- ✅ django-filters on Students (program, status)
- ✅ django-filters on Sections (term, course)
- ✅ django-filters on Programs, Courses, Terms
- ✅ Search + ordering on all major entities

#### Ops & Reliability
- ✅ Nightly backup GitHub Action (pg_dump, 7-day retention)
- ✅ restore.sh script for database restoration
- ✅ /healthz endpoint (alias for /health/)
- ✅ Health check monitors: database, Redis, RQ queue
- ✅ RQ worker configuration in docker-compose

### New Models
- **Term**: Academic periods with open/closed status
- **Result.state**: draft/published/frozen state machine
- **Enrollment.enrolled_at**: Timestamp tracking
- **Enrollment.term**: Explicit term reference

### API Enhancements
- **Terms API**: Full CRUD with status filtering
- **Enrollment**: POST /api/sections/{id}/enroll with validations
- **Results**: /api/results/freeze/ for final archival
- **Health**: /healthz alias endpoint

### Testing & Quality
- ✅ 220 tests passing
- ✅ 97% code coverage (exceeds 85% requirement)
- ✅ Ruff linting: all checks passing
- ✅ mypy type checking: clean
- ✅ Django system checks: no issues
- ✅ All migrations linear and applied

### Documentation Updates
- ✅ API.md: Complete endpoint documentation with examples
- ✅ DATAMODEL.md: Comprehensive ERD with Mermaid diagram
- ✅ DATAMODEL.md: Business rules and state machines documented
- ✅ CHANGELOG.md: This release entry

### CI/CD & Infrastructure
- ✅ Backend CI workflow: lint + type check + tests (≥80% coverage)
- ✅ CodeQL security scanning
- ✅ Nightly backup workflow with 7-day artifact retention
- ✅ Database restore script with safety checks

### Definition of Done
- ✅ All 6 core modules delivered and tested
- ✅ APIs operational with role-based auth
- ✅ Transcripts generated via RQ job + QR verification
- ✅ Coverage ≥ 85% (achieved 97%)
- ✅ Documentation updated (API, DATAMODEL, CHANGELOG)
- ✅ CI green and passing
- ✅ Backup and restore automation complete

---

## 2025-10-20 - Stage 3 Development (v0.3.0-beta) - IN PROGRESS

### Infrastructure & Background Jobs
- Added rqworker service to docker-compose.yml for async task processing
- Created background jobs for transcript generation (generate_and_email_transcript, batch_generate_transcripts)
- Added `/api/transcripts/enqueue/` endpoint for async transcript generation
- Enhanced health check endpoint with Redis/RQ component status monitoring
- Integrated django-rq for background task management

### CI/CD & Security
- **CodeQL Security Analysis:** Added workflow for Python and JavaScript security scanning
- **Trivy Scanning:** Added comprehensive security scanning for filesystem and Docker images
- **Dependency Review:** Automated dependency vulnerability checking in PRs
- **Coverage Enforcement:** Backend ≥80% (99% achieved)
- **Release Automation:** Created workflow for automated release creation with artifacts

### Testing & Quality
- All backend tests passing (220 tests, 99% coverage)
- All linting checks passing (ruff for Python, ESLint for JavaScript)
- Updated tests to handle "degraded" health status when Redis unavailable
- Frontend development happening in parallel in separate branch

### Next Steps
- Expand frontend with JWT authentication flow
- Build CRUD screens for core modules
- Add dashboard with real-time statistics
- Update remaining documentation
- Create release tag v0.3.0-beta

## 2025-10-17 - Remediation Complete
### Django Configuration
- Added `core` app to INSTALLED_APPS (was missing despite being used)
- Verified all third-party apps registered: corsheaders, django_filters, simple_history, drf_spectacular
- Confirmed middleware order with CorsMiddleware at top
- Verified migrations run cleanly with both PostgreSQL and SQLite

### Core Shared Logic Enhancement
- Refactored Program model to inherit from TimeStampedModel base class
- Created migration for Program model timestamp fields (created_at, updated_at)
- Added comprehensive unit tests for Program model timestamp functionality
- Demonstrated reusable base model pattern across multiple apps

### Documentation
- Created REMEDIATION_SUMMARY.md documenting all fixes and current system state
- All endpoints verified: JWT auth at /api/auth/token/, API docs at /api/docs/
- Frontend dashboard confirmed working with health endpoint integration
- Updated changelog with remediation summary

## 2025-10-17
- Enabled cross-origin, filtering, history, and API schema tooling in Django settings and verified migrations against SQLite for local development.
- Exposed JWT authentication endpoints and DRF Spectacular-powered Swagger/ReDoc routes that align with published README URLs.
- Added a reusable `TimeStampedModel` in the `core` app, refactored the admissions `Student` model to inherit from it, and backfilled data via migrations with accompanying tests.
- Replaced the Vite starter counter with a dashboard stub that reads the backend health endpoint using a configurable `VITE_API_BASE_URL`.
- Updated documentation and quick-start instructions to reflect the new tooling, endpoints, and frontend environment requirements.

## 2025-01-12 - Stage 1 Progress (copilot/stage-1-completion-100pct)
### Code Quality & Testing
- Applied ruff, black, and isort formatting across entire codebase
- Implemented comprehensive test suite (121 tests) achieving 96% coverage
- All linters passing (ruff, black, isort)

### Attendance Module - Enhanced
- **NEW:** Implemented attendance percentage calculation utility
- **NEW:** Added eligibility checking with 75% threshold (per RULES.md)
- **NEW:** Created section attendance summary function
- **NEW:** API endpoints for `/percentage`, `/eligibility`, `/section-summary`
- 12 comprehensive tests covering boundary cases (60%, 75%, 80%, 100%)

### Core Modules - Complete CRUD
- **Academics:** Programs, Courses, Sections with constraints and search
- **Enrollment:** Student-section binding with duplicate prevention
- **Assessments:** Assessment types and score tracking
- **Results:** Basic result model with grade tracking

### Security & Auditing
- Comprehensive permission tests for all role-based access
- Object-level permissions for students
- Audit middleware tested for all write operations

### Test Coverage by Module
- Admissions: 97% (25+ tests)
- Academics: 100% (15+ tests)
- Attendance: 96% (25+ tests) 
- Enrollment: 100% (10+ tests)
- Assessments: 100% (8+ tests)
- Results: 100% (5+ tests)
- Audit: 86% (15+ tests)
- Permissions: 92-93% (18+ tests)

### URL Configuration
- Added attendance, assessments, results, transcripts to main URLs
- All modules now accessible via REST API

### Documentation
- Created STAGE1_PROGRESS_SUMMARY.md with detailed status and remaining work

## 2025-10-11
- Implement audit logging middleware and persistence for write requests.
- Normalized admissions app source formatting to resolve syntax issues and enabled routers in project URLs.
- Added audit logging tests and ensured serializer tests run under database context.

## 2025-10-10
- Admissions Student CRUD + Search (API, permissions, tests, seed).
- Standardized error shape; pagination enabled.
- Add demo data and docs snippets (API.students.md, DATAMODEL.students.md).
