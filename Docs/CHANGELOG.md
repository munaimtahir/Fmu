# Changelog

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
