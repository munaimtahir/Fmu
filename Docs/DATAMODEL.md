# Data Model (ERD)

    ```mermaid
    erDiagram
      INSTITUTION ||--o{ PROGRAM : offers
      PROGRAM ||--o{ COURSE : contains
      COURSE ||--o{ SECTION : offered_as
      SECTION ||--o{ ENROLLMENT : has
      STUDENT ||--o{ ENROLLMENT : takes
      SECTION ||--o{ ATTENDANCE : records
      SECTION ||--o{ ASSESSMENT : has
      STUDENT ||--o{ RESULT : receives
      RESULT ||--o{ AUDIT_LOG : tracks
    ```

    ## Key Entities
    - **Student**: demographics, id, status
    - **Program/Course/Section**: structure of learning
    - **Enrollment**: student-course binding
    - **Attendance**: date, presence, reason, entered by
    - **Assessment**: type, weight, rubric
    - **Result**: component marks, final grade, published flag
    - **AuditLog**: who/what/when/why of changes
