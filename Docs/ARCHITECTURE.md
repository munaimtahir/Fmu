# Architecture Overview

    - **Backend:** Django REST Framework (DRF), Postgres, Redis (optional).
    - **Frontend:** React (Vite/Next), REST API client, component tests.
    - **Infra:** Docker Compose (dev), Nginx reverse proxy, SSL (Let's Encrypt).

    ## High-Level Diagram (ASCII)
    ```
    [React FE] <--> [DRF API] <--> [Postgres]
                       |
                     [Redis]*
                       |
                    [Celery]*
    [Nginx/SSL] sits in front of FE+API in production.
    ```

    ## Error Handling
    - Consistent error shape: `{ "error": { "code": "...", "message": "..." } }`.
    - No PII in logs.
