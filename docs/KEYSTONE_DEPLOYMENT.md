# Keystone Deployment Guide

## Overview

This guide explains how to deploy the SIMS application on Keystone, which uses **path-based routing** with Traefik reverse proxy. In Keystone deployments, your app is accessible at `http://VPS_IP/{APP_SLUG}/` instead of the domain root.

## What is Keystone?

Keystone is a deployment system that:
- Hosts multiple GitHub repos on one VPS using Docker
- Uses Traefik reverse proxy with PATH-BASED routing
- Strips the `{APP_SLUG}` prefix before forwarding requests to containers
- Example: `http://1.2.3.4/sims/` → Container receives requests as if they start at `/`

## Architecture

```
Browser: http://VPS_IP/sims/dashboard
    ↓
Traefik: Strips /sims/, forwards /dashboard to container
    ↓
Container: Receives /dashboard (not /sims/dashboard)
    ↓
App must generate: /sims/dashboard for browser links
```

## Critical Concepts

### 1. Browser vs Container Paths

- **Browser path**: What appears in the URL bar → `http://VPS_IP/sims/...`
- **Container path**: What the app receives → `/...` (without `/sims`)
- **Challenge**: App must generate browser links with `/sims/` prefix, but receives requests without it

### 2. Django FORCE_SCRIPT_NAME

Django's `FORCE_SCRIPT_NAME` setting tells Django it's deployed under a subpath:
- Makes `reverse()` and all URL generation include the prefix
- Makes redirects respect the subpath
- Static/media URLs automatically include the prefix

### 3. React Router basename

React Router's `basename` tells the router to prepend all routes with the base path:
- Navigations stay within the subpath
- Links are generated with the prefix
- Browser URLs maintain `/sims/` prefix

## Configuration Steps

### Step 1: Choose Your APP_SLUG

Pick a URL-safe slug for your app (e.g., `sims`, `fmu`, `student-system`).
This will be your subpath: `http://VPS_IP/{APP_SLUG}/`

### Step 2: Backend Configuration (Django)

Update your `.env` file with Keystone settings:

```bash
# Django subpath configuration (NO trailing slash)
FORCE_SCRIPT_NAME=/sims

# Cookie paths (WITH trailing slash)
SESSION_COOKIE_PATH=/sims/
CSRF_COOKIE_PATH=/sims/

# Reverse proxy settings
USE_X_FORWARDED_HOST=True

# Add your VPS IP to allowed hosts
DJANGO_ALLOWED_HOSTS=your.vps.ip.address,localhost,127.0.0.1

# Add your full URLs to CORS and CSRF origins
CORS_ALLOWED_ORIGINS=http://your.vps.ip.address
CSRF_TRUSTED_ORIGINS=http://your.vps.ip.address
```

**Important**:
- `FORCE_SCRIPT_NAME`: Must start with `/`, NO trailing slash (e.g., `/sims`)
- Cookie paths: Must start and end with `/` (e.g., `/sims/`)
- Use your actual VPS IP or domain in origins

### Step 3: Frontend Configuration (React/Vite)

Update your frontend `.env` file:

```bash
# Frontend base path (WITH trailing slash)
VITE_BASE_PATH=/sims/

# API URL should be empty for production (use relative URLs)
VITE_API_URL=
```

**Important**:
- `VITE_BASE_PATH`: Must start and end with `/` (e.g., `/sims/`)
- Leave `VITE_API_URL` empty in production (backend is on same domain)

### Step 4: Build Frontend

Build the frontend with the base path:

```bash
cd frontend
npm run build
```

The built files will use relative paths and respect the base path.

### Step 5: Traefik Configuration

Keystone's Traefik needs these labels in your `docker-compose.yml`:

```yaml
services:
  nginx:  # or whatever serves your app
    labels:
      # Enable Traefik
      - "traefik.enable=true"
      
      # HTTP router
      - "traefik.http.routers.sims.rule=PathPrefix(`/sims`)"
      - "traefik.http.routers.sims.entrypoints=web"
      
      # Strip prefix middleware (CRITICAL)
      - "traefik.http.middlewares.sims-stripprefix.stripprefix.prefixes=/sims"
      - "traefik.http.routers.sims.middlewares=sims-stripprefix"
      
      # Service configuration
      - "traefik.http.services.sims.loadbalancer.server.port=80"
      
      # Network
      - "traefik.docker.network=keystone_network"
    networks:
      - keystone_network
      - default

networks:
  keystone_network:
    external: true
```

**Key points**:
- Replace `sims` with your APP_SLUG throughout
- `PathPrefix` rule matches your subpath
- `stripprefix` middleware removes the prefix before forwarding
- Expose the internal port your nginx/app listens on

### Step 6: Django Static Files

After deploying, collect static files:

```bash
docker compose exec backend python manage.py collectstatic --noinput
```

Django will automatically prepend `FORCE_SCRIPT_NAME` to all static URLs.

## Testing Keystone Deployment

### 1. Health Check

```bash
curl http://your.vps.ip/sims/health/
# Should return: {"status": "ok", ...}
```

### 2. Static Files

```bash
curl -I http://your.vps.ip/sims/static/admin/css/base.css
# Should return: 200 OK
```

### 3. API Endpoint

```bash
curl http://your.vps.ip/sims/api/auth/login/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
# Should return: {"access": "...", "refresh": "..."}
```

### 4. Frontend Access

Open in browser: `http://your.vps.ip/sims/`

**Verify**:
- ✅ Page loads (no 404)
- ✅ CSS/JS loaded (check browser dev tools, no 404s)
- ✅ Can log in (no redirect to `/login` instead of `/sims/login`)
- ✅ After login, URL stays within `/sims/...`
- ✅ Navigation works (clicking links maintains `/sims/` prefix)
- ✅ API calls succeed (check network tab, calls go to `/sims/api/...`)

## Common Issues & Solutions

### Issue 1: 404 on Root `/`

**Symptom**: `http://VPS_IP/sims/` returns 404

**Solution**: 
- Check Traefik rule uses `PathPrefix` not just `Path`
- Verify stripprefix middleware is applied
- Check app is actually listening on the specified port

### Issue 2: Static Files 404

**Symptom**: CSS/JS files return 404, `/static/...` instead of `/sims/static/...`

**Solution**:
- Ensure `FORCE_SCRIPT_NAME` is set in Django settings
- Run `collectstatic` after setting `FORCE_SCRIPT_NAME`
- Verify whitenoise middleware is enabled

### Issue 3: Login Redirects to Root

**Symptom**: After login, redirected to `/dashboard` instead of `/sims/dashboard`

**Solution**:
- Verify `FORCE_SCRIPT_NAME` is set correctly
- Check `SESSION_COOKIE_PATH` matches the subpath
- Ensure Django's `reverse()` is used for all redirects (not hardcoded strings)

### Issue 4: CSRF Token Mismatch

**Symptom**: "CSRF verification failed" on form submissions

**Solution**:
- Set `CSRF_COOKIE_PATH` to match subpath (e.g., `/sims/`)
- Add full URL to `CSRF_TRUSTED_ORIGINS` (e.g., `http://your.vps.ip`)
- Verify cookies are being set with correct path in browser dev tools

### Issue 5: API Calls to Wrong URL

**Symptom**: Frontend makes calls to `/api/...` instead of `/sims/api/...`

**Solution**:
- Frontend: Set `VITE_BASE_PATH=/sims/` before building
- Verify Vite's `base` config is using the env var
- Rebuild frontend after changing base path
- Clear browser cache

### Issue 6: React Router 404 on Refresh

**Symptom**: Refreshing a page like `/sims/dashboard` returns 404

**Solution**:
- Ensure nginx/Traefik fallback serves `index.html` for all routes
- React Router `basename` must be set correctly
- Check Traefik forwarding includes sub-routes

## Local Development with Subpath Simulation

To test subpath behavior locally:

### Option 1: Use Nginx Locally

Create `nginx-local.conf`:

```nginx
server {
    listen 8080;
    
    location /sims/ {
        proxy_pass http://localhost:81/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Run nginx:
```bash
nginx -c $(pwd)/nginx-local.conf -g 'daemon off;'
```

Set environment variables:
```bash
# Backend
FORCE_SCRIPT_NAME=/sims
SESSION_COOKIE_PATH=/sims/
CSRF_COOKIE_PATH=/sims/

# Frontend
VITE_BASE_PATH=/sims/
```

Access: `http://localhost:8080/sims/`

### Option 2: Use Environment Variables Only

Simplest approach for quick testing:

```bash
# Set Keystone env vars in your .env
FORCE_SCRIPT_NAME=/sims
SESSION_COOKIE_PATH=/sims/
CSRF_COOKIE_PATH=/sims/
VITE_BASE_PATH=/sims/

# Start normally
docker compose up

# Access at root (simulation only, not perfect)
# http://localhost:81/
```

Note: This doesn't perfectly simulate Keystone but helps catch many issues.

## Environment Variables Reference

### Required for Keystone

| Variable | Example | Description |
|----------|---------|-------------|
| `FORCE_SCRIPT_NAME` | `/sims` | Django subpath (NO trailing slash) |
| `SESSION_COOKIE_PATH` | `/sims/` | Session cookie scope (WITH trailing slash) |
| `CSRF_COOKIE_PATH` | `/sims/` | CSRF cookie scope (WITH trailing slash) |
| `VITE_BASE_PATH` | `/sims/` | Frontend base path (WITH trailing slash) |

### Optional but Recommended

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_X_FORWARDED_HOST` | `True` | Trust X-Forwarded-Host from Traefik |
| `DJANGO_ALLOWED_HOSTS` | - | Add your VPS IP/domain |
| `CORS_ALLOWED_ORIGINS` | - | Add full URL with VPS IP |
| `CSRF_TRUSTED_ORIGINS` | - | Add full URL with VPS IP |

### Local Development

For local dev at root (`/`), either:
1. Don't set Keystone variables (use defaults)
2. Or set them to root:
   ```bash
   FORCE_SCRIPT_NAME=
   SESSION_COOKIE_PATH=/
   CSRF_COOKIE_PATH=/
   VITE_BASE_PATH=/
   ```

## Deployment Checklist

Before deploying to Keystone:

- [ ] Choose APP_SLUG (e.g., `sims`)
- [ ] Update `.env` with Keystone variables
- [ ] Set `FORCE_SCRIPT_NAME=/your-slug`
- [ ] Set cookie paths `/your-slug/`
- [ ] Set `VITE_BASE_PATH=/your-slug/`
- [ ] Build frontend with `npm run build`
- [ ] Add Traefik labels to docker-compose
- [ ] Deploy containers
- [ ] Run `collectstatic`
- [ ] Test health endpoint: `/your-slug/health/`
- [ ] Test static files load
- [ ] Test login flow
- [ ] Test navigation stays in subpath
- [ ] Test API calls go to correct path
- [ ] Test refresh on sub-routes

## Production Security

When deploying to production:

1. **HTTPS Setup**: Traefik should terminate SSL
   ```python
   # settings.py
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   ```

2. **Secure Cookies**: Enable secure flags
   ```python
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   CSRF_COOKIE_HTTPONLY = True
   ```

3. **Strong Secret**: Generate new `DJANGO_SECRET_KEY`
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

4. **Disable Debug**: Always set `DJANGO_DEBUG=False`

5. **Restrict Hosts**: Set specific IPs/domains in `DJANGO_ALLOWED_HOSTS`

## Support

For issues or questions:
- Check "Common Issues" section above
- Review GitHub Issues: https://github.com/munaimtahir/fmu/issues
- Create new issue with "Keystone" label

## Additional Resources

- Django SCRIPT_NAME documentation: https://docs.djangoproject.com/en/stable/ref/settings/#force-script-name
- Traefik PathPrefix: https://doc.traefik.io/traefik/routing/routers/#rule
- React Router basename: https://reactrouter.com/en/main/router-components/browser-router
- Vite base config: https://vitejs.dev/config/shared-options.html#base
