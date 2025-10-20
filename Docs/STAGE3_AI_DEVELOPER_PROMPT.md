# 🧭 FMU SIMS — Stage 3 Development Prompt (CSMAR)

## C — Context / Mission
The FMU SIMS repository sits on a solid Stage 2 foundation:
- Core app registered and migrations verified
- JWT auth and DRF Spectacular docs live (`/api/docs`, `/api/redoc`)
- Frontend dashboard functional with health endpoint
- `TimeStampedModel` implemented + unit tested
- Docs and CHANGELOG updated (`REMEDIATION_SUMMARY.md` added)

**Objective:** Advance from *stable skeleton* → *feature‑complete MVP*.
All academic modules, background jobs, and CI/CD gates must now operate end‑to‑end in an auditable, demo‑ready build.

## S — Standards & Constraints
| Area | Requirement |
|---|---|
| Frameworks | Django REST Framework + React (Vite) |
| Testing Targets | Backend ≥ 80% coverage; Frontend ≥ 70% |
| Lint & Style | `ruff + black + isort + mypy` (Python) / `eslint + prettier + vitest` (JS) |
| Security | No PII in logs; RBAC per `ROLES.md`; JWT short expiry + rotation |
| Docs Discipline | Auto‑update API schema, ERD, ENV, CHANGELOG per commit |
| Infra | Docker Compose (dev); Nginx reverse proxy (prod) |
| CI/CD Pipeline | Lint → Type → Test → Coverage → Trivy Scan → Build → Release |
| Data Governance | Retention + Audit per `DATA-GOVERNANCE.md` & `RULES.md` |
| Acceptance | All boxes in `ACCEPTANCE_CHECKLIST.md` checked ✔️ |

## M — Modules to Deliver
### 1) Backend — Feature Completion
- **Enrollment Module:** student–section binding + business rules + validation
- **Assessments Module:** schemes, components, marks entry APIs
- **Results Module:** publish/freeze workflow + dual‑approval audit
- **Transcripts Module:** QR‑verified PDF generation (via RQ tasks)
- **Requests Module:** bonafide / transcript requests tracking
- **Audit Logging:** actor + timestamp + change summary for all writes
- **Filtering & Search:** `django-filters` for Students / Sections

### 2) Frontend — Feature Integration
- JWT Auth Flow (login → refresh → logout → guarded routes)
- CRUD screens: Students, Sections, Attendance, Assessments, Results
- Dashboard with counts + eligibility alerts + recent activity
- Attendance UI: daily marking and eligibility % bar (from backend endpoints)
- Results view: publish/freeze indicator + audit trail popup
- Global error boundary + toast system for UX feedback

### 3) DevOps & Infrastructure
- Add **rqworker** service to `docker-compose.yml` for async tasks
- Demo job for PDF generation and email notification
- Nginx serving built frontend with SSL (Let’s Encrypt)
- Monitoring & Health checks (`/healthz`, Sentry optional)
- Backups & restore per `OPERATIONS.md`
- CI/CD enforcement + auto release tag (`v0.3.0-beta`)

### 4) Documentation & Quality Assurance
- Update `API.md`, `DATAMODEL.md`, `SETUP.md`, `CHANGELOG.md`, `SHOWCASE.md`
- Add screenshots (Login, Dashboard, Attendance, Results, Transcript)
- Verify `ROLES.md` permission matrix matches code
- Regenerate schema & ERD from models
- Expand tests to cover new endpoints and UI flows

## A — Action Plan / Execution Steps
### Phase 1 – Backend Expansion
1. Create/extend apps: Enrollment, Assessments, Results, Transcripts, Requests
2. Implement models from `DATAMODEL.md`; generate migrations
3. Add serializers, viewsets, routers with role‑based permissions
4. Implement **AuditLog** middleware + unit tests
5. Build `publish_results` command with freeze/unfreeze states + safeguards
6. Integrate Redis RQ for async tasks (PDF jobs)
7. Add `rqworker` to docker‑compose and validate connection
8. Run lint, mypy, pytest — coverage ≥ 80%

### Phase 2 – Frontend Expansion
1. Implement auth hooks and token refresh middleware
2. Build CRUD screens for all core modules
3. Connect API calls using axios interceptors (`VITE_API_BASE_URL`)
4. Add toast / loading / error UI states
5. Extend dashboard cards + eligibility visualizations
6. FE unit + component tests ≥ 70%

### Phase 3 – DevOps & QA
1. Configure GitHub Actions: lint → type → test → coverage → Trivy scan
2. Add CodeQL security analysis
3. Deploy Single‑VM demo (backend :8000 / frontend :3000 / nginx :443)
4. Validate API docs build and ReDoc schema
5. Verify backup and restore process
6. Update CHANGELOG and Docs; tag release `v0.3.0-beta`

## R — Results / Deliverables
1. **Functional MVP:** Full academic cycle (Student → Enroll → Attend → Assess → Result → Transcript)
2. **Demo Script:** `make demo` loads fixtures + opens dashboard
3. **CI Green:** Lint + type + test + coverage + security gates pass
4. **Docs Synced:** API schema + ERD auto‑regenerated and verified
5. **Showcase:** Screenshots and walkthrough added to `SHOWCASE.md`
6. **Release:** `v0.3.0-beta` with CHANGELOG excerpt + GitHub Release artifacts

## Optional Stage 4 Preview
- Student self‑service portal
- Faculty dashboard for mark entry & attendance
- Notification system (SMS/Email)
- Analytics reports & CSV/XLSX exports
- Supervisor approval workflows for postgraduate tracking
