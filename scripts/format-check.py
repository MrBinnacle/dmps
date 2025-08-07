#!/usr/bin/env python3
"""
Format checker script to run before commits
"""
import subprocess
import sys


def run_command(cmd, description):
    """Run command and return success status"""
    print(f"Running {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED: {description}")
        print(result.stdout)
        print(result.stderr)
        return False
    print(f"PASSED: {description}")
    return True


def main():
    """Run all formatting checks"""
    checks = [
        ("python -m black --check src/", "Black formatting check"),
        ("python -m isort --check-only src/", "Import sorting check"),
        (
            "python -m ruff check src/",
            "Ruff linting",
        ),
        ("python -m mypy src/ --ignore-missing-imports", "Type checking"),
    ]

    all_passed = True
    for cmd, desc in checks:
        if not run_command(cmd, desc):
            all_passed = False

    if not all_passed:
        print("\nSome checks failed. Run 'python scripts/format.py' to fix.")
        sys.exit(1)

    print("\nAll checks passed!")


if __name__ == "__main__":
    main()
