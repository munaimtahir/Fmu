# Keystone Deployment - Quick Reference

## 🚀 Quick Start

### 1. Configure Environment

Edit `.env`:
```bash
# Backend (Django)
FORCE_SCRIPT_NAME=/sims
SESSION_COOKIE_PATH=/sims/
CSRF_COOKIE_PATH=/sims/
USE_X_FORWARDED_HOST=True
DJANGO_ALLOWED_HOSTS=your.vps.ip.address,localhost

# Add to existing origins
CORS_ALLOWED_ORIGINS=http://your.vps.ip.address,...
CSRF_TRUSTED_ORIGINS=http://your.vps.ip.address,...
```

Create `frontend/.env`:
```bash
# Frontend (React)
VITE_BASE_PATH=/sims/
VITE_API_URL=
```

### 2. Build and Deploy

```bash
# Build frontend with subpath
cd frontend
npm install
npm run build
cd ..

# Start containers
docker compose up -d

# Initialize database
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --noinput
docker compose exec backend python manage.py seed_demo
```

### 3. Configure Traefik

Add to your `docker-compose.yml`:
```yaml
services:
  nginx:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.sims.rule=PathPrefix(`/sims`)"
      - "traefik.http.routers.sims.entrypoints=web"
      - "traefik.http.middlewares.sims-stripprefix.stripprefix.prefixes=/sims"
      - "traefik.http.routers.sims.middlewares=sims-stripprefix"
      - "traefik.http.services.sims.loadbalancer.server.port=80"
    networks:
      - keystone_network
      - default

networks:
  keystone_network:
    external: true
```

### 4. Test

```bash
# Automated tests
./scripts/test-keystone.sh

# Manual test in browser
http://your.vps.ip/sims/
```

## 📋 Environment Variables Reference

| Variable | Backend | Frontend | Example | Required |
|----------|---------|----------|---------|----------|
| `FORCE_SCRIPT_NAME` | ✅ | - | `/sims` | Yes |
| `SESSION_COOKIE_PATH` | ✅ | - | `/sims/` | Yes |
| `CSRF_COOKIE_PATH` | ✅ | - | `/sims/` | Yes |
| `USE_X_FORWARDED_HOST` | ✅ | - | `True` | Yes |
| `VITE_BASE_PATH` | - | ✅ | `/sims/` | Yes |
| `VITE_API_URL` | - | ✅ | `` (empty) | Yes |
| `DJANGO_ALLOWED_HOSTS` | ✅ | - | `1.2.3.4` | Yes |
| `CORS_ALLOWED_ORIGINS` | ✅ | - | `http://1.2.3.4` | Yes |
| `CSRF_TRUSTED_ORIGINS` | ✅ | - | `http://1.2.3.4` | Yes |

## ⚠️ Important Notes

### Path Format Rules
- `FORCE_SCRIPT_NAME`: NO trailing slash (e.g., `/sims`)
- Cookie paths: WITH trailing slash (e.g., `/sims/`)
- `VITE_BASE_PATH`: WITH trailing slash (e.g., `/sims/`)

### Must Match
The slug must be consistent across all settings:
- Traefik `PathPrefix`
- Django `FORCE_SCRIPT_NAME`
- Frontend `VITE_BASE_PATH`
- Cookie paths

### Collectstatic
Always run `collectstatic` AFTER setting `FORCE_SCRIPT_NAME`:
```bash
docker compose exec backend python manage.py collectstatic --noinput
```

## 🧪 Testing Checklist

Quick verification after deployment:

- [ ] Health: `curl http://VPS_IP/sims/health/`
- [ ] Static: `curl -I http://VPS_IP/sims/static/admin/css/base.css`
- [ ] Login page loads: `http://VPS_IP/sims/login`
- [ ] CSS/JS assets load (no 404s)
- [ ] Can log in successfully
- [ ] After login, URL is `/sims/dashboard` (not `/dashboard`)
- [ ] Navigation stays in `/sims/...`
- [ ] Page refresh works
- [ ] Logout works

## 🔗 Full Documentation

- **Complete Guide**: [docs/KEYSTONE_DEPLOYMENT.md](KEYSTONE_DEPLOYMENT.md)
- **Test Plan**: [docs/KEYSTONE_TEST_PLAN.md](KEYSTONE_TEST_PLAN.md)
- **Compatibility Report**: [docs/KEYSTONE_COMPATIBILITY_REPORT.md](KEYSTONE_COMPATIBILITY_REPORT.md)
- **Main README**: [../README.md](../README.md)

## 🐛 Troubleshooting

### Static files 404
- Run `collectstatic` after setting `FORCE_SCRIPT_NAME`
- Verify `FORCE_SCRIPT_NAME=/sims` (no trailing slash)

### Login redirects to root `/`
- Check `SESSION_COOKIE_PATH=/sims/` (with trailing slash)
- Verify `CSRF_COOKIE_PATH=/sims/` (with trailing slash)

### Frontend loads but assets 404
- Rebuild frontend after setting `VITE_BASE_PATH`
- Check browser DevTools console for actual 404 URLs
- Verify Vite build used correct base path

### API calls go to wrong path
- Check `VITE_API_URL` is empty (for relative URLs)
- Verify frontend was rebuilt after env var change
- Check network tab: calls should go to `/sims/api/...`

### Traefik not routing
- Verify `PathPrefix` rule matches your slug
- Check `stripprefix` middleware is applied
- Ensure container is on `keystone_network`

## 💡 Quick Commands

```bash
# Check if services are healthy
docker compose ps

# View backend logs
docker compose logs -f backend

# View nginx logs
docker compose logs -f nginx

# Restart after env var changes
docker compose down
docker compose up -d

# Run automated tests
./scripts/test-keystone.sh

# Check Django configuration
docker compose exec backend python manage.py shell
>>> from django.conf import settings
>>> settings.FORCE_SCRIPT_NAME
'/sims'
```

## 🎯 Common Scenarios

### Local Development (Root Path)
```bash
# Don't set Keystone variables
FORCE_SCRIPT_NAME=
SESSION_COOKIE_PATH=/
CSRF_COOKIE_PATH=/
VITE_BASE_PATH=/
```

### Staging Environment
```bash
FORCE_SCRIPT_NAME=/sims-staging
SESSION_COOKIE_PATH=/sims-staging/
CSRF_COOKIE_PATH=/sims-staging/
VITE_BASE_PATH=/sims-staging/
```

### Production
```bash
FORCE_SCRIPT_NAME=/sims
SESSION_COOKIE_PATH=/sims/
CSRF_COOKIE_PATH=/sims/
VITE_BASE_PATH=/sims/

# Additional production settings
DJANGO_DEBUG=False
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 📞 Support

- GitHub Issues: https://github.com/munaimtahir/fmu/issues
- Label your issue with `Keystone` for faster response
- Include your environment variables (redact secrets!)
- Include error messages and logs
