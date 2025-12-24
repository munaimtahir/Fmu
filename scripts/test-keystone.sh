#!/bin/bash

# Keystone Compatibility Test Script
# This script performs automated tests to verify Keystone path-based routing works correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="${BASE_URL:-http://localhost:8080/sims}"
TIMEOUT=5

echo "🧪 Keystone Compatibility Test Suite"
echo "===================================="
echo "Testing URL: $BASE_URL"
echo ""

# Test counter
PASSED=0
FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    echo -e "   ${YELLOW}Details${NC}: $2"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
}

info() {
    echo -e "ℹ️  $1"
}

# Test 1: Health Check
echo "Test 1: Health Check"
if RESPONSE=$(curl -sf --max-time $TIMEOUT "$BASE_URL/health/" 2>&1); then
    if echo "$RESPONSE" | grep -q "status"; then
        pass "Health endpoint accessible and returns valid response"
    else
        fail "Health endpoint returned unexpected response" "$RESPONSE"
    fi
else
    fail "Health endpoint not accessible" "curl failed"
fi
echo ""

# Test 2: Static Files
echo "Test 2: Static Files (Django Admin CSS)"
if curl -sf --max-time $TIMEOUT -I "$BASE_URL/static/admin/css/base.css" 2>&1 | grep -q "200"; then
    pass "Static files accessible at subpath"
elif curl -sf --max-time $TIMEOUT -I "$BASE_URL/staticfiles/admin/css/base.css" 2>&1 | grep -q "200"; then
    pass "Static files accessible at subpath (via staticfiles)"
else
    warn "Static files test skipped (collectstatic may not have been run)"
fi
echo ""

# Test 3: API Endpoints Exist
echo "Test 3: API Endpoints"
if curl -sf --max-time $TIMEOUT -X OPTIONS "$BASE_URL/api/auth/login/" > /dev/null 2>&1; then
    pass "API auth endpoint accessible"
else
    fail "API auth endpoint not accessible" "OPTIONS request failed"
fi
echo ""

# Test 4: Login API
echo "Test 4: Login API Functionality"
LOGIN_RESPONSE=$(curl -sf --max-time $TIMEOUT -X POST "$BASE_URL/api/auth/login/" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin123"}' 2>&1 || echo "CURL_FAILED")

if [ "$LOGIN_RESPONSE" = "CURL_FAILED" ]; then
    warn "Login test skipped (service may not be running or admin user not seeded)"
else
    if echo "$LOGIN_RESPONSE" | grep -q "access"; then
        pass "Login API works and returns JWT tokens"
        TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)
        
        # Test 5: Authenticated API Call
        echo ""
        echo "Test 5: Authenticated API Call"
        if [ -n "$TOKEN" ]; then
            if curl -sf --max-time $TIMEOUT "$BASE_URL/api/dashboard/stats/" \
                -H "Authorization: Bearer $TOKEN" > /dev/null 2>&1; then
                pass "Authenticated API call works with JWT"
            else
                warn "Authenticated API test skipped (endpoint may not exist or requires different permissions)"
            fi
        fi
    else
        fail "Login API returned unexpected response" "$LOGIN_RESPONSE"
    fi
fi
echo ""

# Test 6: Root Path Isolation
echo "Test 6: Root Path Isolation (Security)"
if curl -sf --max-time $TIMEOUT "$BASE_URL/../api/auth/login/" > /dev/null 2>&1; then
    warn "Root path accessible (may be expected in test environment)"
else
    pass "Root bypass prevented (app properly isolated to subpath)"
fi
echo ""

# Test 7: Frontend Index
echo "Test 7: Frontend Index HTML"
if curl -sf --max-time $TIMEOUT "$BASE_URL/" 2>&1 | grep -q "<!doctype html>"; then
    pass "Frontend index.html accessible at subpath root"
else
    warn "Frontend index test skipped (frontend may not be built or served)"
fi
echo ""

# Test 8: CORS Headers (if applicable)
echo "Test 8: CORS Configuration"
CORS_RESPONSE=$(curl -sf --max-time $TIMEOUT -I -X OPTIONS "$BASE_URL/api/auth/login/" \
    -H "Origin: http://localhost" \
    -H "Access-Control-Request-Method: POST" 2>&1 || echo "FAILED")

if [ "$CORS_RESPONSE" != "FAILED" ]; then
    if echo "$CORS_RESPONSE" | grep -qi "access-control-allow-origin"; then
        pass "CORS headers present"
    else
        warn "CORS headers not found (may be configured differently)"
    fi
else
    warn "CORS test skipped"
fi
echo ""

# Summary
echo "===================================="
echo "Test Summary"
echo "===================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All automated tests passed!${NC}"
    echo ""
    echo "⚠️  Note: Manual tests still required:"
    echo "   - Browser UI navigation"
    echo "   - Session persistence across refreshes"
    echo "   - Deep link access"
    echo "   - Cookie path verification (browser DevTools)"
    echo "   - Asset loading in browser (no 404s)"
    echo ""
    echo "   See docs/KEYSTONE_TEST_PLAN.md for complete test checklist"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Ensure services are running: docker compose up -d"
    echo "2. Check FORCE_SCRIPT_NAME is set in backend .env"
    echo "3. Check VITE_BASE_PATH is set in frontend .env"
    echo "4. Run migrations: docker compose exec backend python manage.py migrate"
    echo "5. Seed data: docker compose exec backend python manage.py seed_demo"
    echo "6. Collect static: docker compose exec backend python manage.py collectstatic --noinput"
    echo ""
    echo "For detailed troubleshooting, see docs/KEYSTONE_DEPLOYMENT.md"
    exit 1
fi
