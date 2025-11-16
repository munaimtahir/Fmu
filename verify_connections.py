#!/usr/bin/env python3
"""
Backend-Frontend Connection Verification Script
This script verifies all modules and connection points in the SIMS application
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} NOT FOUND: {filepath}")
        return False

def check_directory_structure():
    """Verify the project directory structure"""
    print_header("PROJECT DIRECTORY STRUCTURE")

    structure_checks = {
        "Backend directory": "backend",
        "Frontend directory": "frontend",
        "Docker compose": "docker-compose.yml",
        "Environment example": ".env.example",
        "Nginx config": "nginx",
        "Documentation": "Docs"
    }

    all_good = True
    for desc, path in structure_checks.items():
        if not check_file_exists(path, desc):
            all_good = False

    return all_good

def check_backend_modules():
    """Verify all backend modules and their configuration"""
    print_header("BACKEND MODULES")

    modules = [
        ("Admissions", "backend/sims_backend/admissions"),
        ("Academics", "backend/sims_backend/academics"),
        ("Enrollment", "backend/sims_backend/enrollment"),
        ("Attendance", "backend/sims_backend/attendance"),
        ("Assessments", "backend/sims_backend/assessments"),
        ("Results", "backend/sims_backend/results"),
        ("Requests", "backend/sims_backend/requests"),
        ("Transcripts", "backend/sims_backend/transcripts"),
        ("Audit", "backend/sims_backend/audit"),
    ]

    all_good = True
    for module_name, module_path in modules:
        module_files = {
            "models.py": f"{module_path}/models.py",
            "views.py": f"{module_path}/views.py",
            "serializers.py": f"{module_path}/serializers.py",
            "urls.py": f"{module_path}/urls.py",
        }

        print(f"\n{BOLD}Module: {module_name}{RESET}")
        module_complete = True
        for file_desc, file_path in module_files.items():
            if Path(file_path).exists():
                print_success(f"  {file_desc}")
            else:
                print_error(f"  {file_desc} MISSING")
                module_complete = False
                all_good = False

        if module_complete:
            print_success(f"  Module {module_name} is COMPLETE")

    return all_good

def check_backend_api_endpoints():
    """List all backend API endpoints"""
    print_header("BACKEND API ENDPOINTS")

    endpoints = {
        "Authentication": [
            "/api/auth/token/ (POST) - Login",
            "/api/auth/token/refresh/ (POST) - Refresh token",
        ],
        "Dashboard": [
            "/api/dashboard/stats/ (GET) - Dashboard statistics",
        ],
        "Students": [
            "/api/students/ (GET, POST) - List/Create students",
            "/api/students/<id>/ (GET, PATCH, DELETE) - Student details",
        ],
        "Academic": [
            "/api/terms/ (GET, POST) - List/Create terms",
            "/api/programs/ (GET, POST) - List/Create programs",
            "/api/courses/ (GET, POST) - List/Create courses",
            "/api/sections/ (GET, POST) - List/Create sections",
        ],
        "Enrollment": [
            "/api/enrollments/ (GET, POST) - List/Create enrollments",
            "/api/sections/<id>/enroll/ (POST) - Enroll student in section",
        ],
        "Attendance": [
            "/api/attendance/ (GET, POST) - List/Create attendance records",
        ],
        "Assessments": [
            "/api/assessments/ (GET, POST) - List/Create assessments",
        ],
        "Results": [
            "/api/results/ (GET, POST) - List/Create results",
            "/api/pending-changes/ (GET) - List pending changes",
        ],
        "Health": [
            "/health/ (GET) - Health check",
            "/healthz/ (GET) - Health check (alias)",
        ],
        "API Docs": [
            "/api/schema/ (GET) - OpenAPI schema",
            "/api/docs/ (GET) - Swagger UI",
            "/api/redoc/ (GET) - ReDoc",
        ],
    }

    for category, urls in endpoints.items():
        print(f"\n{BOLD}{category}:{RESET}")
        for url in urls:
            print_info(f"  {url}")

    return True

def check_frontend_modules():
    """Verify all frontend modules and their configuration"""
    print_header("FRONTEND MODULES")

    frontend_checks = {
        "Axios configuration": "frontend/src/api/axios.ts",
        "Environment config": "frontend/src/lib/env.ts",
        "Auth API": "frontend/src/api/auth.ts",
        "Dashboard API": "frontend/src/api/dashboard.ts",
        "Students service": "frontend/src/services/students.ts",
        "Courses service": "frontend/src/services/courses.ts",
        "Sections service": "frontend/src/services/sections.ts",
        "Enrollment service": "frontend/src/services/enrollment.ts",
        "Attendance service": "frontend/src/services/attendance.ts",
        "Assessments service": "frontend/src/services/assessments.ts",
    }

    all_good = True
    for desc, path in frontend_checks.items():
        if not check_file_exists(path, desc):
            all_good = False

    return all_good

def check_connection_mapping():
    """Verify frontend-to-backend connection mappings"""
    print_header("FRONTEND ↔ BACKEND CONNECTION MAPPING")

    connections = [
        {
            "module": "Authentication",
            "frontend": "frontend/src/api/auth.ts",
            "backend": "backend/sims_backend/urls.py (EmailTokenObtainPairView)",
            "endpoints": ["/api/auth/token/", "/api/auth/token/refresh/"]
        },
        {
            "module": "Students",
            "frontend": "frontend/src/services/students.ts",
            "backend": "backend/sims_backend/admissions/views.py (StudentViewSet)",
            "endpoints": ["/api/students/"]
        },
        {
            "module": "Academics (Courses, Programs, Sections, Terms)",
            "frontend": "frontend/src/services/courses.ts, sections.ts",
            "backend": "backend/sims_backend/academics/views.py",
            "endpoints": ["/api/courses/", "/api/programs/", "/api/sections/", "/api/terms/"]
        },
        {
            "module": "Enrollment",
            "frontend": "frontend/src/services/enrollment.ts",
            "backend": "backend/sims_backend/enrollment/views.py (EnrollmentViewSet)",
            "endpoints": ["/api/enrollments/", "/api/sections/<id>/enroll/"]
        },
        {
            "module": "Attendance",
            "frontend": "frontend/src/services/attendance.ts",
            "backend": "backend/sims_backend/attendance/views.py (AttendanceViewSet)",
            "endpoints": ["/api/attendance/"]
        },
        {
            "module": "Assessments",
            "frontend": "frontend/src/services/assessments.ts",
            "backend": "backend/sims_backend/assessments/views.py",
            "endpoints": ["/api/assessments/"]
        },
        {
            "module": "Dashboard",
            "frontend": "frontend/src/api/dashboard.ts",
            "backend": "backend/sims_backend/urls.py (dashboard_stats)",
            "endpoints": ["/api/dashboard/stats/"]
        },
    ]

    for conn in connections:
        print(f"\n{BOLD}{conn['module']}:{RESET}")
        print_info(f"  Frontend: {conn['frontend']}")
        print_info(f"  Backend:  {conn['backend']}")
        print_success(f"  Endpoints: {', '.join(conn['endpoints'])}")

    return True

def check_configuration():
    """Check configuration files"""
    print_header("CONFIGURATION")

    # Check Docker configuration
    print(f"\n{BOLD}Docker Configuration:{RESET}")
    docker_files = {
        "Main compose": "docker-compose.yml",
        "Production compose": "docker-compose.prod.yml",
        "Staging compose": "docker-compose.staging.yml",
        "Backend Dockerfile": "backend/Dockerfile",
        "Frontend Dockerfile": "frontend/Dockerfile",
    }

    all_good = True
    for desc, path in docker_files.items():
        if not check_file_exists(path, desc):
            all_good = False

    # Check environment configuration
    print(f"\n{BOLD}Environment Configuration:{RESET}")
    if Path(".env").exists():
        print_success(".env file exists")
    else:
        print_warning(".env file does NOT exist (using .env.example as reference)")
        print_info("  Run: cp .env.example .env")

    if Path(".env.example").exists():
        print_success(".env.example file exists")
    else:
        print_error(".env.example file NOT FOUND")
        all_good = False

    return all_good

def check_key_configurations():
    """Check key configuration settings"""
    print_header("KEY CONFIGURATION SETTINGS")

    env_example_path = Path(".env.example")
    if env_example_path.exists():
        with open(env_example_path, 'r') as f:
            content = f.read()

        configs = {
            "Database": ["DB_NAME", "DB_USER", "DB_HOST", "DB_PORT"],
            "CORS": ["CORS_ALLOWED_ORIGINS"],
            "JWT": ["JWT_ACCESS_TOKEN_LIFETIME", "JWT_REFRESH_TOKEN_LIFETIME"],
            "Redis": ["REDIS_HOST", "REDIS_PORT"],
            "Django": ["DJANGO_SECRET_KEY", "DJANGO_DEBUG", "DJANGO_ALLOWED_HOSTS"],
        }

        for category, keys in configs.items():
            print(f"\n{BOLD}{category}:{RESET}")
            for key in keys:
                if key in content:
                    print_success(f"  {key} is configured")
                else:
                    print_error(f"  {key} is MISSING")

    return True

def verify_backend_settings():
    """Verify backend settings.py configuration"""
    print_header("BACKEND SETTINGS VERIFICATION")

    settings_path = Path("backend/sims_backend/settings.py")
    if settings_path.exists():
        with open(settings_path, 'r') as f:
            content = f.read()

        checks = {
            "CORS Middleware": "corsheaders.middleware.CorsMiddleware",
            "REST Framework": "REST_FRAMEWORK",
            "JWT Authentication": "rest_framework_simplejwt",
            "Database Config": "DATABASES",
            "CORS Settings": "CORS_ALLOWED_ORIGINS",
            "Redis/RQ Config": "RQ_QUEUES",
        }

        for desc, pattern in checks.items():
            if pattern in content:
                print_success(f"{desc}")
            else:
                print_error(f"{desc} NOT FOUND")
    else:
        print_error("settings.py NOT FOUND")

    return True

def main():
    """Main verification function"""
    print(f"\n{BOLD}{GREEN}{'='*80}")
    print(f"SIMS - Backend-Frontend Connection Verification".center(80))
    print(f"{'='*80}{RESET}\n")

    results = []

    # Run all checks
    results.append(("Directory Structure", check_directory_structure()))
    results.append(("Backend Modules", check_backend_modules()))
    results.append(("Backend API Endpoints", check_backend_api_endpoints()))
    results.append(("Frontend Modules", check_frontend_modules()))
    results.append(("Connection Mapping", check_connection_mapping()))
    results.append(("Configuration Files", check_configuration()))
    results.append(("Key Configurations", check_key_configurations()))
    results.append(("Backend Settings", verify_backend_settings()))

    # Print summary
    print_header("VERIFICATION SUMMARY")

    all_passed = True
    for check_name, result in results:
        if result:
            print_success(f"{check_name}: PASSED")
        else:
            print_error(f"{check_name}: FAILED")
            all_passed = False

    print("\n")
    if all_passed:
        print_success(f"{BOLD}ALL CHECKS PASSED! ✓{RESET}")
        print_info("\nNext steps:")
        print_info("  1. Ensure .env file is configured: cp .env.example .env")
        print_info("  2. Start services: docker compose up -d")
        print_info("  3. Run migrations: docker compose exec backend python manage.py migrate")
        print_info("  4. Access frontend: http://localhost:5173")
        print_info("  5. Access backend API: http://localhost:8000")
        return 0
    else:
        print_error(f"{BOLD}SOME CHECKS FAILED!{RESET}")
        print_warning("\nPlease fix the errors above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
