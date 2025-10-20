## v0.3.0-beta — Stage 3 (Feature-Complete MVP)

### Added
- Enrollment, Assessments, Results (publish/freeze), Transcripts (QR-PDF via RQ), Requests modules
- Audit logging on all write operations with actor, timestamp, change summary
- Frontend auth flow with guarded routes; CRUD screens for Students, Sections, Attendance, Assessments, Results
- Dashboard metrics, eligibility widgets, results state indicators
- Redis RQ worker service and demo async PDF job
- GitHub Actions CI: lint, type, test, coverage, Trivy scan, build; CodeQL security analysis
- Nginx prod config to serve built frontend over TLS; health checks; backup/restore docs

### Changed
- Documentation refreshed: `API.md`, `DATAMODEL.md`, `SETUP.md`, `SHOWCASE.md`
- ERD/schema regenerated and published alongside API docs

### Fixed
- Coverage floors enforced (BE ≥ 80%, FE ≥ 70%); CI failures on regressions

### Notes
- Demo workflow: `make demo` → loads fixtures and opens dashboard
- Release artifacts attached to GitHub Release `v0.3.0-beta`
