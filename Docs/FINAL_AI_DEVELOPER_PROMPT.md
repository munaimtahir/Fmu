# Final AI Developer Prompt
You are an autonomous senior full‑stack engineer. Build SIMS (Django + DRF + Postgres + React).

## Mission
Deliver Phase 1 as production‑ready: core academic digitization with tests, seed data, Docker deploy, and CI.

## Constraints
- Python 3.12, Django 5.x, DRF
- Postgres 14+
- React 18 + Vite (or Next.js if SSR needed)
- 90%+ backend test coverage; 70%+ frontend
- Twelve‑factor configuration via .env
- Migrations, fixtures, admin
- API first; clean REST with pagination and filtering

## Tasks
1. Scaffold backend `sims_backend/` and frontend `sims_frontend/`; shared `.env.example` and `docker-compose.yml`.
2. Implement models: University, College, Department, Program, Cohort, Section, Term, Course, Student, Admission, Enrollment, Attendance, AssessmentScheme, AssessmentComponent, Mark, Result, Transcript, Document, Verification, RequestTicket.
3. RBAC with Django groups/permissions; superuser bootstrap command.
4. CRUD APIs with DRF viewsets, query filters. Pagination=50. Search for name/code.
5. Attendance import endpoint (CSV) and manual entry endpoint; eligibility computation service.
6. Assessment & Results service: apply weightages; transcript PDF generator w/ QR.
7. Reporting endpoints: attendance eligibility list, defaulters, result summary (grouped).
8. Audit log (django-simple-history or custom middleware); daily backups (cron/Job).
9. Admin plus seed script to create demo university, programs, cohorts, 500 students, 10 teachers.
10. Frontend: secure login (JWT), role dashboard, screens for students list, attendance capture, marks entry, reports download.
11. CI (GitHub Actions): lint, type-check (mypy), tests, build images.
12. Docker deploy: Nginx reverse proxy; static/media; healthchecks.

## Definition of Done
- End‑to‑end working on Docker locally and in staging
- Test coverage targets met
- Two sample reports exported (CSV/PDF)
- README & SETUP.md validated on a clean machine
