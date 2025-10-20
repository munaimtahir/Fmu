# Operations Runbook

## System Architecture

The SIMS system consists of the following services:

### Core Services
- **Backend (Django):** REST API on port 8000
- **Frontend (React/Vite):** UI on port 5173 (dev) / served by Nginx (prod)
- **PostgreSQL:** Database on port 5432
- **Redis:** Cache and message broker on port 6379
- **RQ Worker:** Background task processor
- **Nginx:** Reverse proxy on ports 80/443

### Service Dependencies
```
Frontend → Backend → PostgreSQL
              ↓
            Redis → RQ Worker
```

## Service Management

### Starting Services
```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d backend
docker compose up -d rqworker

# View logs
docker compose logs -f backend
docker compose logs -f rqworker
```

### Stopping Services
```bash
# Stop all services
docker compose down

# Stop specific service
docker compose stop rqworker
```

### Service Health Checks

**Health Endpoint:** `GET /health/`

Returns:
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

**Status Values:**
- `ok` - All components healthy
- `degraded` - One or more components unhealthy

### Background Jobs (RQ Worker)

The RQ worker processes asynchronous tasks like transcript generation and email notifications.

**Monitor Worker:**
```bash
# Check worker logs
docker compose logs -f rqworker

# Check queue status (inside backend container)
docker exec -it sims_backend python manage.py rqstats
```

**Common Background Jobs:**
- `generate_and_email_transcript` - Generate PDF transcript and email
- `batch_generate_transcripts` - Bulk transcript generation

**Enqueue Job Example:**
```bash
POST /api/transcripts/enqueue/
{
  "student_id": 123,
  "email": "student@example.com"
}
```

## Backups

### Database Backup
```bash
# Manual backup
docker exec sims_postgres pg_dump -U sims_user sims_db > backup_$(date +%Y%m%d).sql

# Automated backup (cron)
# Daily at 2 AM
0 2 * * * docker exec sims_postgres pg_dump -U sims_user sims_db > /backups/sims_$(date +\%Y\%m\%d).sql
```

### Database Restore
```bash
# Stop backend and worker
docker compose stop backend rqworker

# Restore from backup
docker exec -i sims_postgres psql -U sims_user sims_db < backup_20251020.sql

# Restart services
docker compose start backend rqworker

# Verify health
curl http://localhost:8000/health/
```

### Media Files Backup
```bash
# Backup uploaded files
tar -czf media_backup_$(date +%Y%m%d).tar.gz ./media/

# Restore
tar -xzf media_backup_20251020.tar.gz -C ./
```

## Monitoring

### Health Endpoints
- **API Health:** `GET /health/` - Overall system health
- **Database:** Checked via health endpoint
- **Redis/RQ:** Checked via health endpoint
- **Frontend:** Static file availability

### Log Management
```bash
# View logs
docker compose logs -f [service_name]

# Backend logs
docker compose logs -f backend

# Worker logs
docker compose logs -f rqworker

# All logs
docker compose logs -f

# Save logs to file
docker compose logs > logs_$(date +%Y%m%d).txt
```

**Log Rotation:**
- Rotate daily
- Keep 14 days hot
- Archive monthly backups

### Error Tracking
- **Sentry (optional):** Configure `SENTRY_DSN` environment variable
- **Health Check Monitoring:** Monitor `/health/` endpoint every 30 seconds

### Metrics to Monitor
- API response times
- Background job queue length
- Database connections
- Memory usage
- Disk space
- Failed background jobs

## Incidents

### Incident Response Process
1. **Triage:** Assess severity and impact
2. **Communication:** Notify stakeholders via #ops-fmu
3. **Investigation:** Check logs, health endpoints, metrics
4. **Mitigation:** Apply temporary fix
5. **Resolution:** Implement permanent fix
6. **Postmortem:** Document incident and learnings

### Severity Levels
- **P1 (Critical):** System down, data loss risk
- **P2 (High):** Major feature broken, degraded performance
- **P3 (Medium):** Minor feature broken, workaround available
- **P4 (Low):** Cosmetic issue, enhancement request

### Common Issues

#### Backend Service Not Starting
```bash
# Check logs
docker compose logs backend

# Check database connection
docker exec sims_backend python manage.py check --database default

# Run migrations
docker exec sims_backend python manage.py migrate
```

#### RQ Worker Not Processing Jobs
```bash
# Check worker logs
docker compose logs rqworker

# Check Redis connection
docker exec sims_backend python manage.py rqstats

# Restart worker
docker compose restart rqworker
```

#### High Memory Usage
```bash
# Check container stats
docker stats

# Restart services
docker compose restart backend rqworker

# Scale workers
docker compose up -d --scale rqworker=3
```

## Restore Procedures

### Complete System Restore
1. **Stop all services:**
   ```bash
   docker compose down
   ```

2. **Restore database:**
   ```bash
   docker compose up -d postgres
   docker exec -i sims_postgres psql -U sims_user sims_db < backup.sql
   ```

3. **Restore media files:**
   ```bash
   tar -xzf media_backup.tar.gz -C ./
   ```

4. **Start services:**
   ```bash
   docker compose up -d
   ```

5. **Verify health:**
   ```bash
   curl http://localhost:8000/health/
   docker compose ps
   ```

6. **Run smoke tests:**
   ```bash
   # Test API
   curl http://localhost:8000/api/students/
   
   # Test frontend
   curl http://localhost:5173/
   ```

## Maintenance

### Database Maintenance
```bash
# Vacuum database
docker exec sims_postgres vacuumdb -U sims_user -d sims_db -v

# Reindex
docker exec sims_postgres reindexdb -U sims_user -d sims_db

# Check statistics
docker exec sims_postgres psql -U sims_user -d sims_db -c "SELECT * FROM pg_stat_activity;"
```

### Cleanup
```bash
# Remove old logs
docker compose logs > /dev/null

# Clean Docker system
docker system prune -a --volumes

# Clear old backups (keep last 30 days)
find /backups -type f -mtime +30 -delete
```

## Security

### SSL Certificate Renewal
```bash
# Renew Let's Encrypt certificate
docker exec sims_nginx certbot renew

# Reload Nginx
docker exec sims_nginx nginx -s reload
```

### Security Scanning
- **Trivy:** Automated in CI/CD pipeline
- **CodeQL:** Automated in CI/CD pipeline
- **Manual scan:**
  ```bash
  # Scan Docker image
  trivy image sims-backend:latest
  ```

## Contact

- **Triage channel:** #ops-fmu
- **On-call rota:** See internal wiki
- **Postmortem template:** See internal wiki
