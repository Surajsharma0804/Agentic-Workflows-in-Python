#!/usr/bin/env python3
"""
Quick health check script for Agentic Workflows
Run this to verify all systems are operational
"""
import sys
import subprocess
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status"""
    print(f"🔍 {description}...", end=" ", flush=True)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print("✅")
            return True
        else:
            print(f"❌\n   Error: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"❌\n   Error: {str(e)[:100]}")
        return False


def main():
    """Run all health checks"""
    print("\n" + "="*60)
    print("🏥 AGENTIC WORKFLOWS - HEALTH CHECK")
    print("="*60 + "\n")
    
    checks = []
    
    # Backend checks
    print("📦 Backend Checks:")
    checks.append(run_command("pytest -q", "Running Python tests"))
    
    # Frontend checks
    print("\n🎨 Frontend Checks:")
    ui_path = Path("ui")
    if ui_path.exists():
        checks.append(run_command("cd ui && npm run lint", "ESLint check"))
        checks.append(run_command("cd ui && npm run type-check", "TypeScript check"))
    
    # Summary
    print("\n" + "="*60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("="*60)
        print("\n🎉 System is healthy and ready for deployment!\n")
        return 0
    else:
        print(f"❌ SOME CHECKS FAILED ({passed}/{total})")
        print("="*60)
        print("\n⚠️  Please fix the issues above before deploying.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
