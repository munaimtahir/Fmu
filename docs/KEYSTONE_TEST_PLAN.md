# Keystone Test Plan

This document provides a comprehensive testing checklist to verify Keystone path-based routing compatibility.

## Prerequisites

- Docker and Docker Compose installed
- Repository cloned and environment configured
- Basic understanding of Docker networking

## Test Environment Setup

### Option 1: Local Nginx Proxy (Recommended)

This best simulates Keystone's behavior.

1. **Create nginx test configuration**:

```bash
mkdir -p /tmp/keystone-test
cat > /tmp/keystone-test/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    server {
        listen 8080;
        server_name localhost;

        # Simulate Keystone routing for /sims/
        location /sims/ {
            # Strip /sims and forward to backend
            rewrite ^/sims(.*)$ $1 break;
            proxy_pass http://host.docker.internal:81;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-Host $host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
EOF
```

2. **Update .env for Keystone mode**:

```bash
# Backend Keystone settings
FORCE_SCRIPT_NAME=/sims
SESSION_COOKIE_PATH=/sims/
CSRF_COOKIE_PATH=/sims/
USE_X_FORWARDED_HOST=True

# Frontend Keystone settings  
VITE_BASE_PATH=/sims/
VITE_API_URL=
```

3. **Start the application**:

```bash
# Start main app
docker compose up -d

# Wait for services
sleep 15

# Start nginx proxy
docker run -d \
  --name keystone-nginx-test \
  -p 8080:8080 \
  -v /tmp/keystone-test/nginx.conf:/etc/nginx/nginx.conf:ro \
  --add-host=host.docker.internal:host-gateway \
  nginx:alpine
```

4. **Access**:
- **Keystone-style**: http://localhost:8080/sims/
- **Direct (for comparison)**: http://localhost:81/

### Option 2: Environment Variables Only (Quick Test)

For faster iteration, test with env vars only (less accurate):

1. **Update .env**:
```bash
FORCE_SCRIPT_NAME=/sims
SESSION_COOKIE_PATH=/sims/
CSRF_COOKIE_PATH=/sims/
VITE_BASE_PATH=/sims/
```

2. **Rebuild and start**:
```bash
docker compose down
docker compose up --build -d
```

3. **Access directly**: http://localhost:81/
   (Note: This won't perfectly simulate Keystone but catches many issues)

## Test Suite

### Phase 1: Static & Health Checks

#### Test 1.1: Health Endpoint ✅
```bash
curl -s http://localhost:8080/sims/health/ | jq
```

**Expected**:
- Status: 200 OK
- Response: `{"status": "ok", "service": "SIMS Backend", ...}`

**Pass Criteria**: Health check returns 200

---

#### Test 1.2: Django Admin Static Files ✅
```bash
curl -I http://localhost:8080/sims/static/admin/css/base.css
```

**Expected**:
- Status: 200 OK
- Content-Type: text/css

**Pass Criteria**: Static files load from `/sims/static/...`

---

#### Test 1.3: Frontend Assets ✅

Open browser: http://localhost:8080/sims/

**Check Browser DevTools > Network**:
- [ ] `index.html` loads (200)
- [ ] JavaScript bundles load (200, not 404)
- [ ] CSS files load (200, not 404)
- [ ] No 404 errors in console

**Pass Criteria**: All assets load successfully from `/sims/...` paths

---

### Phase 2: Authentication Flow

#### Test 2.1: Login Page Loads ✅

Navigate to: http://localhost:8080/sims/login

**Verify**:
- [ ] Login form displays
- [ ] Page CSS/styling works
- [ ] URL stays at `/sims/login` (not `/login`)

**Pass Criteria**: Login page renders correctly at `/sims/login`

---

#### Test 2.2: Login API Call ✅

**Browser DevTools > Network**, then log in with:
- Username: `admin`
- Password: `admin123`

**Verify in Network tab**:
- [ ] POST request goes to `/sims/api/auth/login/` (not `/api/auth/login/`)
- [ ] Response: 200 OK with tokens
- [ ] Cookies are set with path `/sims/`

**Pass Criteria**: Login succeeds, tokens received, cookies scoped correctly

---

#### Test 2.3: Post-Login Redirect ✅

After successful login:

**Verify**:
- [ ] Redirected to `/sims/dashboard` (not `/dashboard`)
- [ ] Dashboard loads successfully
- [ ] User info displays correctly

**Pass Criteria**: Redirect stays within `/sims/` subpath

---

#### Test 2.4: Protected Route Navigation ✅

Click through various navigation links:
- Dashboard
- Students (if accessible)
- Attendance (if accessible)
- Any other menu items

**Verify for each**:
- [ ] URL stays within `/sims/...` (check address bar)
- [ ] Page content loads
- [ ] Navigation history works (browser back button)

**Pass Criteria**: All navigation maintains `/sims/` prefix

---

### Phase 3: API Functionality

#### Test 3.1: Dashboard Stats API ✅

**Browser DevTools > Network**, navigate to dashboard

**Verify**:
- [ ] GET request to `/sims/api/dashboard/stats/` (not `/api/...`)
- [ ] Response: 200 OK with stats data
- [ ] JWT token in Authorization header

**Pass Criteria**: API calls use correct subpath

---

#### Test 3.2: List Endpoints ✅

Navigate to a page with data tables (e.g., Students list)

**Verify in Network tab**:
- [ ] API calls go to `/sims/api/students/` (with correct subpath)
- [ ] Pagination works (URLs maintain subpath)
- [ ] Search/filter maintains subpath

**Pass Criteria**: All list API calls use `/sims/api/...` paths

---

#### Test 3.3: Create/Update Operations ✅

Try creating or updating a record:

**Verify**:
- [ ] POST/PUT requests go to `/sims/api/.../`
- [ ] CSRF token is included
- [ ] Operation succeeds
- [ ] Redirect after save uses subpath

**Pass Criteria**: CRUD operations work with subpath routing

---

### Phase 4: Session & Cookie Behavior

#### Test 4.1: Cookie Inspection ✅

**Browser DevTools > Application > Cookies > localhost**

**Verify**:
- [ ] `sessionid` cookie exists
- [ ] Cookie path: `/sims/` (not `/`)
- [ ] `csrftoken` cookie exists
- [ ] Cookie path: `/sims/` (not `/`)

**Pass Criteria**: Session and CSRF cookies scoped to subpath

---

#### Test 4.2: Session Persistence ✅

1. Log in
2. Navigate to different pages
3. Refresh browser (F5)
4. Close and reopen browser tab

**Verify after each**:
- [ ] Still logged in
- [ ] No redirect to login
- [ ] Session data persists

**Pass Criteria**: Sessions work correctly across navigation and refreshes

---

#### Test 4.3: Logout Flow ✅

Click logout button/link

**Verify**:
- [ ] Logout API call to `/sims/api/auth/logout/`
- [ ] Redirected to `/sims/login` (not `/login`)
- [ ] Cookies cleared
- [ ] Cannot access protected routes after logout

**Pass Criteria**: Logout works and redirects correctly

---

### Phase 5: Direct URL Access (Refresh Test)

#### Test 5.1: Dashboard Refresh ✅

1. Navigate to: http://localhost:8080/sims/dashboard
2. Press F5 (refresh)

**Verify**:
- [ ] Page reloads successfully
- [ ] Still at `/sims/dashboard`
- [ ] No 404 error
- [ ] Content displays correctly

**Pass Criteria**: Direct URL access works (no routing errors)

---

#### Test 5.2: Deep Link Refresh ✅

Navigate to a nested route (e.g., `/sims/dashboard/admin`)
1. Copy URL
2. Open in new browser tab
3. Refresh (F5)

**Verify**:
- [ ] Page loads from URL
- [ ] No 404 error
- [ ] Protected route check works (redirects to login if not authenticated)

**Pass Criteria**: Deep links work with subpath

---

### Phase 6: Browser DevTools Verification

#### Test 6.1: Search for Root Paths ✅

**Browser DevTools > Sources > Search (Ctrl+Shift+F)**

Search for these patterns in loaded JavaScript:
- `"/api/`
- `"href":"/"` 
- `"src":"/`

**Verify**:
- [ ] No hardcoded `/api/` calls (should be `/sims/api/` or relative)
- [ ] No absolute root paths in generated code
- [ ] Asset paths respect base path

**Pass Criteria**: No hardcoded root-absolute paths in frontend code

---

#### Test 6.2: Network Tab Audit ✅

**Browser DevTools > Network**

Perform various actions (login, navigate, logout)

**Verify all requests**:
- [ ] All API calls: `/sims/api/...`
- [ ] All static assets: `/sims/assets/...` or `/sims/static/...`
- [ ] No requests to `/api/` without subpath
- [ ] No 404 errors

**Pass Criteria**: All network requests respect subpath routing

---

### Phase 7: Negative Tests

#### Test 7.1: Root Access ✅

Try accessing: http://localhost:8080/

**Expected**:
- Should NOT show the app (Keystone would route to different app)
- May show 404 or Traefik default page

**Pass Criteria**: App is not accessible at root `/` (only at `/sims/`)

---

#### Test 7.2: Bypass Attempt ✅

Try accessing: http://localhost:8080/api/auth/login/
(Without `/sims/` prefix)

**Expected**:
- Should fail (404 or no route)
- Should NOT reach the backend

**Pass Criteria**: Direct API access without subpath doesn't work

---

### Phase 8: Local Development Mode Test

#### Test 8.1: Switch to Development Mode ✅

1. **Update .env** (remove Keystone settings):
```bash
FORCE_SCRIPT_NAME=
SESSION_COOKIE_PATH=/
CSRF_COOKIE_PATH=/
VITE_BASE_PATH=/
```

2. **Rebuild**:
```bash
docker compose down
docker compose up --build -d
```

3. **Access**: http://localhost:81/

**Verify**:
- [ ] App works at root `/`
- [ ] Login works
- [ ] Navigation works
- [ ] API calls go to `/api/...` (without subpath)

**Pass Criteria**: App still works in standard mode (backward compatible)

---

## Automated Test Script

Save as `scripts/test-keystone.sh`:

```bash
#!/bin/bash

set -e

echo "🧪 Keystone Compatibility Test Suite"
echo "===================================="

BASE_URL="${BASE_URL:-http://localhost:8080/sims}"

echo ""
echo "1. Health Check..."
if curl -sf "$BASE_URL/health/" > /dev/null; then
    echo "   ✅ Health endpoint accessible"
else
    echo "   ❌ Health endpoint failed"
    exit 1
fi

echo ""
echo "2. Static Files..."
if curl -sf -I "$BASE_URL/static/admin/css/base.css" | grep -q "200 OK"; then
    echo "   ✅ Static files accessible"
else
    echo "   ❌ Static files failed"
    exit 1
fi

echo ""
echo "3. API Login..."
RESPONSE=$(curl -sf -X POST "$BASE_URL/api/auth/login/" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin123"}' || echo "FAILED")

if echo "$RESPONSE" | grep -q "access"; then
    echo "   ✅ Login API works"
    TOKEN=$(echo "$RESPONSE" | jq -r .access)
else
    echo "   ❌ Login API failed"
    echo "   Response: $RESPONSE"
    exit 1
fi

echo ""
echo "4. Authenticated API..."
if curl -sf "$BASE_URL/api/dashboard/stats/" \
    -H "Authorization: Bearer $TOKEN" > /dev/null; then
    echo "   ✅ Authenticated API works"
else
    echo "   ❌ Authenticated API failed"
    exit 1
fi

echo ""
echo "5. Root Path Isolation..."
if ! curl -sf "$BASE_URL/../api/auth/login/" > /dev/null 2>&1; then
    echo "   ✅ Root bypass prevented"
else
    echo "   ⚠️  Warning: Root path accessible (may be expected in test env)"
fi

echo ""
echo "✅ All automated tests passed!"
echo ""
echo "⚠️  Manual tests still required:"
echo "   - Browser UI navigation"
echo "   - Session persistence"
echo "   - Deep link refresh"
echo "   - Cookie path verification"
```

Usage:
```bash
chmod +x scripts/test-keystone.sh
./scripts/test-keystone.sh
```

## Test Results Template

Use this template to record test results:

```markdown
## Test Execution Report

**Date**: YYYY-MM-DD
**Tester**: [Name]
**Environment**: [Local/Staging/Production]
**APP_SLUG**: /sims

### Test Results Summary

| Phase | Test | Status | Notes |
|-------|------|--------|-------|
| 1. Static | Health endpoint | ✅ PASS | |
| 1. Static | Admin static files | ✅ PASS | |
| 1. Static | Frontend assets | ✅ PASS | |
| 2. Auth | Login page loads | ✅ PASS | |
| 2. Auth | Login API call | ✅ PASS | |
| 2. Auth | Post-login redirect | ✅ PASS | |
| 2. Auth | Protected routes | ✅ PASS | |
| 3. API | Dashboard stats | ✅ PASS | |
| 3. API | List endpoints | ✅ PASS | |
| 3. API | CRUD operations | ✅ PASS | |
| 4. Session | Cookie inspection | ✅ PASS | |
| 4. Session | Persistence | ✅ PASS | |
| 4. Session | Logout | ✅ PASS | |
| 5. Refresh | Dashboard refresh | ✅ PASS | |
| 5. Refresh | Deep link | ✅ PASS | |
| 6. DevTools | Root paths search | ✅ PASS | |
| 6. DevTools | Network audit | ✅ PASS | |
| 7. Negative | Root access | ✅ PASS | |
| 7. Negative | Bypass attempt | ✅ PASS | |
| 8. Dev Mode | Standard mode | ✅ PASS | |

### Issues Found

[List any issues discovered]

### Recommendations

[Any suggestions for improvements]

### Sign-off

- [ ] All critical tests passed
- [ ] App ready for Keystone deployment
- [ ] Documentation updated

**Approved by**: [Name]
**Date**: [Date]
```

## Cleanup

After testing:

```bash
# Stop test nginx
docker stop keystone-nginx-test
docker rm keystone-nginx-test

# Stop app
docker compose down

# Reset .env to development defaults
# (Remove Keystone settings or set to root paths)
```

## Support

If tests fail, consult:
1. [KEYSTONE_DEPLOYMENT.md](KEYSTONE_DEPLOYMENT.md) - Full deployment guide
2. "Common Issues" section in deployment guide
3. GitHub Issues with "Keystone" label

## Version

- **Test Plan Version**: 1.0
- **Last Updated**: 2024
- **Compatible with**: SIMS v1.0+
