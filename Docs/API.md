# API Summary (Critical Endpoints)

    > See live ReDoc/Swagger at `/api/redoc` and `/api/docs`.

    ## Auth
    - `POST /api/auth/login`
    - `POST /api/auth/logout`
    - `POST /api/auth/refresh`

    ## Students
    - `GET /api/students` (Admin/Registrar)
    - `POST /api/students` (Admin/Registrar)
    - `GET /api/students/{id}` (Owner or Staff)
    - `PATCH /api/students/{id}` (Admin/Registrar)

    ## Enrollment
    - `POST /api/sections/{id}/enroll`
    - `GET /api/enrollments?student=...`

    ## Attendance
    - `POST /api/sections/{id}/attendance`
    - `GET /api/attendance?section=...&date=...`

    ## Assessments & Results
    - `POST /api/sections/{id}/assessments`
    - `POST /api/assessments/{id}/scores`
    - `POST /api/results/publish`
    - `GET /api/results?student=...`

    ## Transcripts
    - `GET /api/transcripts/{student_id}` - Generate and download transcript PDF
    - `POST /api/transcripts/enqueue/` - Enqueue transcript generation as background job
    - `GET /api/transcripts/verify/{token}` - Verify transcript QR token

    ## Health & Monitoring
    - `GET /health/` - System health check (database, Redis, RQ queue status)
