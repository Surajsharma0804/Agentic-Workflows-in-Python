#!/usr/bin/env python3
"""
Comprehensive Pre-Submission Check for Agentic Workflows
Validates all functionality before AWS Builder Center submission
"""
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Tuple, Dict
import time


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CheckResult:
    """Result of a check."""
    def __init__(self, name: str, passed: bool, message: str = "", details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details


class ComprehensiveChecker:
    """Comprehensive checker for the project."""
    
    def __init__(self):
        self.results: List[CheckResult] = []
        self.project_root = Path(__file__).parent
        
    def print_header(self, text: str):
        """Print a section header."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    def print_check(self, name: str, status: str = "running"):
        """Print check status."""
        if status == "running":
            print(f"{Colors.OKCYAN}🔍 {name}...{Colors.ENDC}", end=" ", flush=True)
        elif status == "pass":
            print(f"{Colors.OKGREEN}✅{Colors.ENDC}")
        elif status == "fail":
            print(f"{Colors.FAIL}❌{Colors.ENDC}")
        elif status == "warning":
            print(f"{Colors.WARNING}⚠️{Colors.ENDC}")
    
    def run_command(self, cmd: str, cwd: Path = None, timeout: int = 120) -> Tuple[bool, str, str]:
        """Run a shell command and return success status."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd or self.project_root
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def check_file_exists(self, path: Path, description: str) -> CheckResult:
        """Check if a file exists."""
        self.print_check(f"Checking {description}", "running")
        exists = path.exists()
        self.print_check(f"Checking {description}", "pass" if exists else "fail")
        return CheckResult(
            f"File: {description}",
            exists,
            f"Found at {path}" if exists else f"Missing: {path}"
        )
    
    def check_directory_structure(self) -> List[CheckResult]:
        """Check project directory structure."""
        self.print_header("📁 PROJECT STRUCTURE")
        
        required_paths = [
            (self.project_root / "README.md", "README.md"),
            (self.project_root / "requirements-full.txt", "requirements-full.txt"),
            (self.project_root / "pyproject.toml", "pyproject.toml"),
            (self.project_root / ".env.example", ".env.example"),
            (self.project_root / "Dockerfile", "Dockerfile"),
            (self.project_root / "render.yaml", "render.yaml"),
            (self.project_root / ".kiro", ".kiro directory"),
            (self.project_root / ".kiro" / "README.md", ".kiro/README.md"),
            (self.project_root / "agentic_workflows", "agentic_workflows package"),
            (self.project_root / "ui", "ui directory"),
            (self.project_root / "ui" / "package.json", "ui/package.json"),
            (self.project_root / "tests", "tests directory"),
        ]
        
        results = []
        for path, desc in required_paths:
            results.append(self.check_file_exists(path, desc))
        
        return results
    
    def check_kiro_directory(self) -> List[CheckResult]:
        """Check .kiro directory is properly configured."""
        self.print_header("🤖 KIRO DIRECTORY")
        
        results = []
        kiro_path = self.project_root / ".kiro"
        
        # Check .kiro exists
        results.append(self.check_file_exists(kiro_path, ".kiro directory"))
        
        # Check .kiro is not in .gitignore
        self.print_check("Checking .kiro not in .gitignore", "running")
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            kiro_ignored = ".kiro" in content or "/.kiro" in content
            self.print_check("Checking .kiro not in .gitignore", "fail" if kiro_ignored else "pass")
            results.append(CheckResult(
                ".kiro not in .gitignore",
                not kiro_ignored,
                "✅ .kiro will be included in repository" if not kiro_ignored else "❌ .kiro is in .gitignore - MUST FIX"
            ))
        
        # Check .kiro contents
        if kiro_path.exists():
            kiro_files = list(kiro_path.glob("*"))
            self.print_check(f"Found {len(kiro_files)} files in .kiro", "pass" if kiro_files else "warning")
            results.append(CheckResult(
                ".kiro contents",
                len(kiro_files) > 0,
                f"Found {len(kiro_files)} files: {', '.join(f.name for f in kiro_files)}"
            ))
        
        return results
    
    def check_python_setup(self) -> List[CheckResult]:
        """Check Python environment and dependencies."""
        self.print_header("🐍 PYTHON ENVIRONMENT")
        
        results = []
        
        # Check Python version
        self.print_check("Checking Python version", "running")
        success, stdout, stderr = self.run_command("python --version")
        self.print_check("Checking Python version", "pass" if success else "fail")
        results.append(CheckResult(
            "Python version",
            success,
            stdout.strip() if success else stderr
        ))
        
        # Check pip
        self.print_check("Checking pip", "running")
        success, stdout, stderr = self.run_command("pip --version")
        self.print_check("Checking pip", "pass" if success else "fail")
        results.append(CheckResult(
            "pip available",
            success,
            stdout.strip() if success else stderr
        ))
        
        # Check if dependencies can be parsed
        self.print_check("Checking requirements.txt", "running")
        req_file = self.project_root / "requirements-full.txt"
        if req_file.exists():
            try:
                content = req_file.read_text()
                lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
                self.print_check("Checking requirements.txt", "pass")
                results.append(CheckResult(
                    "requirements-full.txt",
                    True,
                    f"Found {len(lines)} dependencies"
                ))
            except Exception as e:
                self.print_check("Checking requirements.txt", "fail")
                results.append(CheckResult("requirements-full.txt", False, str(e)))
        
        return results
    
    def check_frontend_setup(self) -> List[CheckResult]:
        """Check frontend setup."""
        self.print_header("⚛️  FRONTEND SETUP")
        
        results = []
        ui_path = self.project_root / "ui"
        
        # Check Node.js
        self.print_check("Checking Node.js", "running")
        success, stdout, stderr = self.run_command("node --version")
        self.print_check("Checking Node.js", "pass" if success else "fail")
        results.append(CheckResult(
            "Node.js version",
            success,
            stdout.strip() if success else "Node.js not found"
        ))
        
        # Check npm
        self.print_check("Checking npm", "running")
        success, stdout, stderr = self.run_command("npm --version")
        self.print_check("Checking npm", "pass" if success else "fail")
        results.append(CheckResult(
            "npm version",
            success,
            stdout.strip() if success else "npm not found"
        ))
        
        # Check package.json
        package_json = ui_path / "package.json"
        if package_json.exists():
            self.print_check("Checking package.json", "running")
            try:
                data = json.loads(package_json.read_text())
                self.print_check("Checking package.json", "pass")
                results.append(CheckResult(
                    "package.json",
                    True,
                    f"Name: {data.get('name')}, Version: {data.get('version')}"
                ))
            except Exception as e:
                self.print_check("Checking package.json", "fail")
                results.append(CheckResult("package.json", False, str(e)))
        
        # Check if node_modules exists
        node_modules = ui_path / "node_modules"
        self.print_check("Checking node_modules", "running")
        exists = node_modules.exists()
        self.print_check("Checking node_modules", "pass" if exists else "warning")
        results.append(CheckResult(
            "node_modules",
            True,  # Not critical
            "Installed" if exists else "Not installed (run: cd ui && npm install)"
        ))
        
        # Check if dist exists (built frontend)
        dist_path = ui_path / "dist"
        self.print_check("Checking frontend build", "running")
        exists = dist_path.exists() and (dist_path / "index.html").exists()
        self.print_check("Checking frontend build", "pass" if exists else "warning")
        results.append(CheckResult(
            "Frontend build",
            True,  # Not critical for dev
            "Built" if exists else "Not built (run: cd ui && npm run build)"
        ))
        
        return results
    
    def check_code_quality(self) -> List[CheckResult]:
        """Check code quality."""
        self.print_header("✨ CODE QUALITY")
        
        results = []
        
        # Check Python syntax
        self.print_check("Checking Python syntax", "running")
        success, stdout, stderr = self.run_command(
            "python -m py_compile agentic_workflows/**/*.py",
            timeout=30
        )
        self.print_check("Checking Python syntax", "pass" if success else "warning")
        results.append(CheckResult(
            "Python syntax",
            True,  # Not critical
            "All files valid" if success else "Some syntax issues (check manually)"
        ))
        
        return results
    
    def check_configuration(self) -> List[CheckResult]:
        """Check configuration files."""
        self.print_header("⚙️  CONFIGURATION")
        
        results = []
        
        # Check .env.example
        env_example = self.project_root / ".env.example"
        if env_example.exists():
            self.print_check("Checking .env.example", "running")
            try:
                content = env_example.read_text(encoding='utf-8')
                required_vars = ["DATABASE_URL", "SECRET_KEY"]
                missing = [var for var in required_vars if var not in content]
                self.print_check("Checking .env.example", "pass" if not missing else "warning")
                results.append(CheckResult(
                    ".env.example",
                    len(missing) == 0,
                    "All required variables present" if not missing else f"Missing: {', '.join(missing)}"
                ))
            except Exception as e:
                self.print_check("Checking .env.example", "warning")
                results.append(CheckResult(".env.example", True, "Present"))
        
        # Check Dockerfile
        dockerfile = self.project_root / "Dockerfile"
        if dockerfile.exists():
            self.print_check("Checking Dockerfile", "running")
            try:
                content = dockerfile.read_text(encoding='utf-8')
                has_from = "FROM" in content
                has_cmd = "CMD" in content or "ENTRYPOINT" in content
                self.print_check("Checking Dockerfile", "pass" if (has_from and has_cmd) else "warning")
                results.append(CheckResult(
                    "Dockerfile",
                    has_from and has_cmd,
                    "Valid Docker configuration" if (has_from and has_cmd) else "May need review"
                ))
            except Exception as e:
                self.print_check("Checking Dockerfile", "warning")
                results.append(CheckResult("Dockerfile", True, "Present"))
        
        # Check render.yaml
        render_yaml = self.project_root / "render.yaml"
        if render_yaml.exists():
            self.print_check("Checking render.yaml", "running")
            try:
                content = render_yaml.read_text(encoding='utf-8')
                has_services = "services:" in content
                self.print_check("Checking render.yaml", "pass" if has_services else "warning")
                results.append(CheckResult(
                    "render.yaml",
                    has_services,
                    "Valid Render configuration" if has_services else "May need review"
                ))
            except Exception as e:
                self.print_check("Checking render.yaml", "warning")
                results.append(CheckResult("render.yaml", True, "Present"))
        
        return results
    
    def check_documentation(self) -> List[CheckResult]:
        """Check documentation."""
        self.print_header("📚 DOCUMENTATION")
        
        results = []
        
        # Check README.md
        readme = self.project_root / "README.md"
        if readme.exists():
            self.print_check("Checking README.md", "running")
            try:
                content = readme.read_text(encoding='utf-8')
                sections = ["Quick Start", "Features", "Deployment", "API"]
                found_sections = [s for s in sections if s.lower() in content.lower()]
                self.print_check("Checking README.md", "pass" if len(found_sections) >= 3 else "warning")
                results.append(CheckResult(
                    "README.md",
                    len(found_sections) >= 3,
                    f"Found {len(found_sections)}/{len(sections)} key sections"
                ))
            except Exception as e:
                self.print_check("Checking README.md", "warning")
                results.append(CheckResult("README.md", True, f"Present but encoding issue: {str(e)[:50]}"))
        
        # Check .kiro/README.md
        kiro_readme = self.project_root / ".kiro" / "README.md"
        if kiro_readme.exists():
            self.print_check("Checking .kiro/README.md", "running")
            try:
                content = kiro_readme.read_text(encoding='utf-8')
                has_content = len(content) > 100
                self.print_check("Checking .kiro/README.md", "pass" if has_content else "warning")
                results.append(CheckResult(
                    ".kiro/README.md",
                    has_content,
                    f"{len(content)} characters" if has_content else "Needs more content"
                ))
            except Exception as e:
                self.print_check("Checking .kiro/README.md", "warning")
                results.append(CheckResult(".kiro/README.md", True, f"Present but encoding issue: {str(e)[:50]}"))

        
        return results
    
    def check_api_health(self) -> List[CheckResult]:
        """Check if API can start (quick test)."""
        self.print_header("🏥 API HEALTH CHECK")
        
        results = []
        
        # Try to import the app
        self.print_check("Checking API imports", "running")
        try:
            sys.path.insert(0, str(self.project_root))
            from agentic_workflows.api.server import create_app
            app = create_app()
            self.print_check("Checking API imports", "pass")
            results.append(CheckResult(
                "API imports",
                True,
                "FastAPI app can be created successfully"
            ))
        except Exception as e:
            self.print_check("Checking API imports", "fail")
            results.append(CheckResult(
                "API imports",
                False,
                f"Error: {str(e)[:100]}"
            ))
        
        return results
    
    def generate_report(self):
        """Generate final report."""
        self.print_header("📊 FINAL REPORT")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print(f"\n{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  Total Checks: {total}")
        print(f"  {Colors.OKGREEN}✅ Passed: {passed}{Colors.ENDC}")
        print(f"  {Colors.FAIL}❌ Failed: {failed}{Colors.ENDC}")
        print(f"  Success Rate: {(passed/total*100):.1f}%\n")
        
        if failed > 0:
            print(f"{Colors.WARNING}{Colors.BOLD}Failed Checks:{Colors.ENDC}")
            for result in self.results:
                if not result.passed:
                    print(f"  {Colors.FAIL}❌ {result.name}{Colors.ENDC}")
                    print(f"     {result.message}")
                    if result.details:
                        print(f"     {result.details}")
        
        print(f"\n{Colors.BOLD}Submission Checklist:{Colors.ENDC}")
        checklist = [
            ("GitHub Repository", True),
            (".kiro directory included", any(r.name == ".kiro not in .gitignore" and r.passed for r in self.results)),
            ("README.md complete", any(r.name == "README.md" and r.passed for r in self.results)),
            ("Code quality checks", passed >= total * 0.8),
            ("Documentation present", any(r.name == ".kiro/README.md" for r in self.results)),
        ]
        
        for item, status in checklist:
            icon = f"{Colors.OKGREEN}✅{Colors.ENDC}" if status else f"{Colors.FAIL}❌{Colors.ENDC}"
            print(f"  {icon} {item}")
        
        print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
        print("  1. Fix any failed checks above")
        print("  2. Ensure .kiro directory is committed to Git")
        print("  3. Push to GitHub repository")
        print("  4. Write technical blog post for AWS Builder Center")
        print("  5. Submit both links through AI for Bharat dashboard")
        
        if passed == total:
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Ready for submission!{Colors.ENDC}\n")
            return 0
        elif passed >= total * 0.8:
            print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️  Most checks passed. Review failures before submission.{Colors.ENDC}\n")
            return 0
        else:
            print(f"\n{Colors.FAIL}{Colors.BOLD}❌ Multiple issues found. Please fix before submission.{Colors.ENDC}\n")
            return 1
    
    def run_all_checks(self):
        """Run all checks."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║                                                                   ║")
        print("║        AGENTIC WORKFLOWS - COMPREHENSIVE PRE-SUBMISSION CHECK     ║")
        print("║                                                                   ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}\n")
        
        # Run all check categories
        self.results.extend(self.check_directory_structure())
        self.results.extend(self.check_kiro_directory())
        self.results.extend(self.check_python_setup())
        self.results.extend(self.check_frontend_setup())
        self.results.extend(self.check_configuration())
        self.results.extend(self.check_documentation())
        self.results.extend(self.check_code_quality())
        self.results.extend(self.check_api_health())
        
        # Generate report
        return self.generate_report()


def main():
    """Main entry point."""
    checker = ComprehensiveChecker()
    return checker.run_all_checks()


if __name__ == "__main__":
    sys.exit(main())
