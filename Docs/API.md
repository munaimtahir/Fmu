# API Documentation (SIMS Backend)

> **Live API Documentation**: See interactive ReDoc/Swagger at `/api/redoc` and `/api/docs`.

## Authentication

### JWT Authentication
- `POST /api/auth/token/` - Obtain JWT access and refresh tokens
- `POST /api/auth/token/refresh/` - Refresh access token

**Headers**: Include `Authorization: Bearer <access_token>` in all authenticated requests.

---

## Core Modules

### Students (Admissions)
- `GET /api/students/` - List all students (filterable by program, status)
- `POST /api/students/` - Create new student (Admin/Registrar only)
- `GET /api/students/{id}/` - Get student details
- `PUT/PATCH /api/students/{id}/` - Update student (Admin/Registrar only)
- `DELETE /api/students/{id}/` - Delete student (Admin only)

**Filters**: `?program=CS&status=active`

---

### Programs, Courses, Sections (Academics)

#### Terms
- `GET /api/terms/` - List academic terms
- `POST /api/terms/` - Create new term
- `GET /api/terms/{id}/` - Get term details
- `PUT/PATCH /api/terms/{id}/` - Update term (set status: open/closed)
- `DELETE /api/terms/{id}/` - Delete term

**Filters**: `?status=open`

#### Programs
- `GET /api/programs/` - List all programs
- `POST /api/programs/` - Create new program
- `GET /api/programs/{id}/` - Get program details
- `PUT/PATCH /api/programs/{id}/` - Update program
- `DELETE /api/programs/{id}/` - Delete program

#### Courses
- `GET /api/courses/` - List all courses (filterable by program, credits)
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}/` - Get course details
- `PUT/PATCH /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course

**Filters**: `?program=1&credits=3`

#### Sections
- `GET /api/sections/` - List all sections (filterable by term, course)
- `POST /api/sections/` - Create new section
- `GET /api/sections/{id}/` - Get section details
- `PUT/PATCH /api/sections/{id}/` - Update section
- `DELETE /api/sections/{id}/` - Delete section

**Filters**: `?term=Fall2024&course=1`

---

### Enrollment
- `GET /api/enrollments/` - List all enrollments
- `POST /api/enrollments/` - Create enrollment (with capacity & term validation)
- `GET /api/enrollments/{id}/` - Get enrollment details
- `PUT/PATCH /api/enrollments/{id}/` - Update enrollment
- `DELETE /api/enrollments/{id}/` - Delete enrollment
- `POST /api/sections/{id}/enroll/` - Enroll student in section (special endpoint)

**POST /api/sections/{id}/enroll/**
```json
{
  "student_id": 1
}
```
**Validations**:
- Returns 409 if student already enrolled
- Returns 400 if term is closed
- Returns 400 if section at full capacity

---

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/percentage/` - Get attendance percentage for student in section
- `GET /api/attendance/eligibility/` - Check exam eligibility (≥75% threshold)
- `GET /api/attendance/section-summary/` - Get attendance summary for entire section

---

### Assessments
- `GET /api/assessments/` - List all assessments
- `POST /api/assessments/` - Create assessment (validates total weight ≤100%)
- `GET /api/assessments/{id}/` - Get assessment details
- `PUT/PATCH /api/assessments/{id}/` - Update assessment
- `DELETE /api/assessments/{id}/` - Delete assessment

#### Assessment Scores
- `GET /api/assessment-scores/` - List all scores
- `POST /api/assessment-scores/` - Record score
- `GET /api/assessment-scores/{id}/` - Get score details
- `PUT/PATCH /api/assessment-scores/{id}/` - Update score
- `DELETE /api/assessment-scores/{id}/` - Delete score

---

### Results (Publish/Freeze Workflow)

**States**: `draft` → `published` → `frozen`

- `GET /api/results/` - List all results
- `POST /api/results/` - Create result (starts in 'draft' state)
- `GET /api/results/{id}/` - Get result details
- `PUT/PATCH /api/results/{id}/` - Update result (only in 'draft' state)
- `DELETE /api/results/{id}/` - Delete result

#### State Transitions
- `POST /api/results/publish/` - Publish result (draft → published)
```json
{
  "result_id": 1,
  "published_by": "registrar@university.edu"
}
```

- `POST /api/results/freeze/` - Freeze result (published → frozen, final state)
```json
{
  "result_id": 1,
  "frozen_by": "dean@university.edu"
}
```

#### Change Requests (for published/frozen results)
- `POST /api/results/change-request/` - Request grade change
```json
{
  "result_id": 1,
  "new_grade": "A",
  "requested_by": "faculty@university.edu",
  "reason": "Calculation error corrected"
}
```

- `POST /api/results/approve-change/` - Approve or reject change request
```json
{
  "change_id": 1,
  "approved": true,
  "approved_by": "registrar@university.edu"
}
```

---

### Transcripts (Async Jobs via RQ)

- `GET /api/transcripts/{student_id}/` - Generate and download transcript PDF
- `POST /api/transcripts/enqueue/` - Enqueue transcript generation as background job
```json
{
  "student_id": 1,
  "email": "student@example.com"  // optional
}
```
- `GET /api/transcripts/verify/{token}/` - Verify transcript QR token

**QR Token**: Valid for 48 hours, embedded in transcript PDFs

---

### Requests (Bonafide, Transcript Requests)

**Workflow**: `pending` → `approved` → `completed`

- `GET /api/requests/` - List all requests
- `POST /api/requests/` - Create new request
- `GET /api/requests/{id}/` - Get request details
- `PUT/PATCH /api/requests/{id}/` - Update request
- `DELETE /api/requests/{id}/` - Delete request
- `POST /api/requests/{id}/transition/` - Transition request status
```json
{
  "status": "approved",
  "processed_by": "registrar@university.edu"
}
```

---

### Audit Logs

- `GET /api/audit/` - View audit trail (all write operations logged)

**Automatic**: All create/update/delete operations are logged with:
- Actor (user)
- Timestamp
- Action summary
- Request details

---

## Health & Monitoring

- `GET /health/` - System health check
- `GET /healthz/` - Health check alias

**Response**:
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

---

## API Schema

- `GET /api/schema/` - OpenAPI 3.0 schema
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc UI

---

## Permissions

- **Admin**: Full access to all endpoints
- **Registrar**: Create/update most resources, read all
- **Faculty**: Read/write sections they teach, assessments, attendance
- **Student**: Read own data only

---

## Pagination

All list endpoints support pagination:
- `?page=1` - Page number (default: 1)
- `?page_size=50` - Results per page (default: 50, max: 100)

---

## Filtering & Search

Use django-filters for exact matches:
- `?program=CS&status=active`

Use search for partial text matches:
- `?search=john`

Use ordering:
- `?ordering=name` (ascending)
- `?ordering=-name` (descending)

---

### Audit Logs
- `GET /api/audit/` - List audit log entries (Admin only)

**Query Parameters**:
- `actor` - Filter by username (partial match)
- `entity` - Filter by model name (partial match)
- `date_from` - Filter by timestamp (ISO 8601 format, e.g., 2025-10-22T00:00:00)
- `date_to` - Filter by timestamp (ISO 8601 format)
- `method` - Filter by HTTP method (POST, PUT, PATCH, DELETE)

**Example:**
```
GET /api/audit/?actor=admin&entity=Student&date_from=2025-10-22T00:00:00&method=POST
```

**Response:**
```json
{
  "count": 42,
  "results": [
    {
      "id": "uuid-here",
      "timestamp": "2025-10-22T10:30:00Z",
      "actor": 1,
      "actor_username": "admin",
      "method": "POST",
      "path": "/api/students/",
      "status_code": 201,
      "model": "Student",
      "object_id": "123",
      "summary": "Created student: John Doe (REG001)"
    }
  ]
}
```

**Notes:**
- All write operations (POST, PUT, PATCH, DELETE) are automatically logged
- Logs are immutable and cannot be modified or deleted
- Only administrators can access audit logs
- Useful for compliance, troubleshooting, and security audits

---

## Error Handling

Standard error response format:
```json
{
  "error": {
    "code": 400,
    "message": "Validation error description"
  }
}
```

**HTTP Status Codes**:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `403` - Forbidden (permission denied)
- `404` - Not Found
- `409` - Conflict (e.g., duplicate enrollment)
- `500` - Server Error
