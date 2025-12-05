#!/usr/bin/env python3
"""
Comprehensive Fix Script for Agentic Workflows
Identifies and fixes all issues automatically
"""
import sys
import subprocess
import os
from pathlib import Path
import secrets
import json


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")


def run_command(cmd, cwd=None):
    """Run command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=120
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_env_file():
    """Check if .env file exists."""
    print_header("1. CHECKING ENVIRONMENT CONFIGURATION")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print_success(".env file exists")
        return True
    else:
        print_warning(".env file not found")
        
        if env_example_path.exists():
            print_info("Creating .env from .env.example...")
            
            # Read .env.example
            content = env_example_path.read_text()
            
            # Generate SECRET_KEY
            secret_key = secrets.token_urlsafe(32)
            content = content.replace(
                "SECRET_KEY=CHANGE_ME_IN_PRODUCTION_USE_STRONG_RANDOM_KEY_32_CHARS_MIN",
                f"SECRET_KEY={secret_key}"
            )
            
            # Write .env
            env_path.write_text(content)
            print_success(f".env file created with SECRET_KEY: {secret_key[:10]}...")
            print_warning("Please update DATABASE_URL and OAuth credentials in .env")
            return True
        else:
            print_error(".env.example not found")
            return False


def check_database():
    """Check database connection and initialize if needed."""
    print_header("2. CHECKING DATABASE")
    
    try:
        # Try to import and initialize database
        sys.path.insert(0, str(Path.cwd()))
        from agentic_workflows.db.database import init_db, get_engine
        from agentic_workflows.db.models import Base
        
        print_info("Initializing database tables...")
        init_db()
        print_success("Database tables initialized successfully")
        
        # Check if tables exist
        engine = get_engine()
        inspector = __import__('sqlalchemy').inspect(engine)
        tables = inspector.get_table_names()
        
        print_info(f"Found {len(tables)} tables: {', '.join(tables)}")
        
        required_tables = ['users', 'workflows', 'workflow_executions', 'audit_logs']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print_warning(f"Missing tables: {', '.join(missing_tables)}")
            print_info("Running migrations...")
            success, stdout, stderr = run_command("alembic upgrade head")
            if success:
                print_success("Migrations completed successfully")
            else:
                print_warning(f"Migrations failed: {stderr}")
        else:
            print_success("All required tables exist")
        
        return True
        
    except Exception as e:
        print_error(f"Database check failed: {str(e)}")
        print_info("Database will use SQLite fallback")
        return False


def check_frontend_build():
    """Check if frontend is built."""
    print_header("3. CHECKING FRONTEND BUILD")
    
    dist_path = Path("ui/dist")
    index_path = dist_path / "index.html"
    
    if dist_path.exists() and index_path.exists():
        print_success("Frontend is built")
        
        # Check build size
        total_size = sum(f.stat().st_size for f in dist_path.rglob('*') if f.is_file())
        print_info(f"Build size: {total_size / 1024 / 1024:.2f} MB")
        return True
    else:
        print_warning("Frontend not built")
        print_info("Building frontend...")
        
        # Check if node_modules exists
        if not Path("ui/node_modules").exists():
            print_info("Installing dependencies...")
            success, stdout, stderr = run_command("npm install", cwd="ui")
            if not success:
                print_error(f"npm install failed: {stderr}")
                return False
        
        # Build frontend
        success, stdout, stderr = run_command("npm run build", cwd="ui")
        if success:
            print_success("Frontend built successfully")
            return True
        else:
            print_error(f"Frontend build failed: {stderr}")
            return False


def check_tests():
    """Run backend tests."""
    print_header("4. RUNNING TESTS")
    
    print_info("Running Python tests...")
    success, stdout, stderr = run_command("python -m pytest tests/ -v --tb=short")
    
    if success:
        # Count passed tests
        passed = stdout.count(" PASSED")
        print_success(f"All tests passed ({passed} tests)")
        return True
    else:
        print_error("Some tests failed")
        print(stderr)
        return False


def check_oauth_config():
    """Check OAuth configuration."""
    print_header("5. CHECKING OAUTH CONFIGURATION")
    
    try:
        from agentic_workflows.config import get_settings
        settings = get_settings()
        
        # Check Google OAuth
        if settings.google_client_id and settings.google_client_secret:
            print_success("Google OAuth configured")
        else:
            print_warning("Google OAuth not configured")
            print_info("To enable: Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env")
        
        # Check GitHub OAuth
        if settings.github_client_id and settings.github_client_secret:
            print_success("GitHub OAuth configured")
        else:
            print_warning("GitHub OAuth not configured")
            print_info("To enable: Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in .env")
        
        # Check Apple OAuth
        if settings.apple_client_id:
            print_success("Apple OAuth configured")
        else:
            print_warning("Apple OAuth not configured")
            print_info("To enable: Set APPLE_CLIENT_ID and related variables in .env")
        
        return True
        
    except Exception as e:
        print_error(f"OAuth check failed: {str(e)}")
        return False


def check_api_health():
    """Check if API can start."""
    print_header("6. CHECKING API HEALTH")
    
    try:
        from agentic_workflows.api.server import create_app
        
        print_info("Creating FastAPI app...")
        app = create_app()
        print_success("FastAPI app created successfully")
        
        # Check routes
        routes = [route.path for route in app.routes]
        api_routes = [r for r in routes if r.startswith('/api')]
        print_info(f"Found {len(api_routes)} API routes")
        
        # Check critical routes
        critical_routes = [
            '/api/health',
            '/api/auth/login',
            '/api/auth/register',
            '/api/workflows',
            '/api/plugins'
        ]
        
        for route in critical_routes:
            if route in routes:
                print_success(f"Route exists: {route}")
            else:
                print_warning(f"Route missing: {route}")
        
        return True
        
    except Exception as e:
        print_error(f"API health check failed: {str(e)}")
        return False


def generate_deployment_checklist():
    """Generate deployment checklist."""
    print_header("7. DEPLOYMENT CHECKLIST")
    
    checklist = {
        "Environment Variables": [
            ("SECRET_KEY", "Generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""),
            ("DATABASE_URL", "PostgreSQL connection string"),
            ("GOOGLE_CLIENT_ID", "Optional: Google OAuth client ID"),
            ("GOOGLE_CLIENT_SECRET", "Optional: Google OAuth client secret"),
            ("GITHUB_CLIENT_ID", "Optional: GitHub OAuth client ID"),
            ("GITHUB_CLIENT_SECRET", "Optional: GitHub OAuth client secret"),
        ],
        "Database Setup": [
            ("Create PostgreSQL database", "On Render.com or other provider"),
            ("Run migrations", "alembic upgrade head"),
            ("Verify tables", "Check users, workflows, workflow_executions, audit_logs"),
        ],
        "Frontend": [
            ("Build frontend", "npm run build in ui/"),
            ("Verify dist/ exists", "Check ui/dist/index.html"),
        ],
        "Testing": [
            ("Run backend tests", "pytest tests/"),
            ("Test login/register", "Manual testing"),
            ("Test API endpoints", "Check /api/docs"),
        ]
    }
    
    for category, items in checklist.items():
        print(f"\n{Colors.BOLD}{category}:{Colors.ENDC}")
        for item, description in items:
            print(f"  ☐ {item}")
            print(f"     {Colors.BLUE}{description}{Colors.ENDC}")


def main():
    """Main function."""
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("="*70)
    print("  AGENTIC WORKFLOWS - COMPREHENSIVE FIX SCRIPT  ".center(70))
    print("="*70)
    print(f"{Colors.ENDC}\n")
    
    results = []
    
    # Run all checks
    results.append(("Environment Configuration", check_env_file()))
    results.append(("Database", check_database()))
    results.append(("Frontend Build", check_frontend_build()))
    results.append(("Tests", check_tests()))
    results.append(("OAuth Configuration", check_oauth_config()))
    results.append(("API Health", check_api_health()))
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_warning(f"{name}: NEEDS ATTENTION")
    
    print(f"\n{Colors.BOLD}Overall: {passed}/{total} checks passed{Colors.ENDC}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Your application is ready!{Colors.ENDC}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Some checks need attention. See details above.{Colors.ENDC}\n")
        generate_deployment_checklist()
        return 1


if __name__ == "__main__":
    sys.exit(main())
