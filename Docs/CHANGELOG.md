# Changelog

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
- **Coverage Enforcement:** Backend ≥80% (99% achieved), Frontend ≥50% (92.5% achieved)
- **Release Automation:** Created workflow for automated release creation with artifacts

### Frontend Development
- Expanded test coverage from 1 to 7 tests (92.5% coverage achieved)
- Added comprehensive App component tests (loading, error, success states)
- Configured coverage thresholds and reporting (v8 provider)
- Installed testing utilities (@testing-library/react, @testing-library/user-event)
- Enhanced ESLint configuration for test files
- Added test:coverage script to package.json

### Testing & Quality
- All backend tests passing (220 tests, 99% coverage)
- All frontend tests passing (7 tests, 92.5% coverage)
- All linting checks passing (ruff for Python, ESLint for JavaScript)
- Updated tests to handle "degraded" health status when Redis unavailable

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
