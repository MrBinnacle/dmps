#!/usr/bin/env python3
"""
Code formatting and quality check script
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run command and report results"""
    print(f"Running {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"FAILED {description}:")
        print(result.stdout)
        print(result.stderr)
        return False
    else:
        print(f"PASSED {description}")
        return True


def main():
    """Main formatting and quality check"""
    src_path = Path("src/dmps")

    if not src_path.exists():
        print("❌ Source directory not found")
        sys.exit(1)

    commands = [
        ("black src/", "Code formatting"),
        ("isort src/", "Import sorting"),
        ("flake8 src/ --count --statistics", "Linting"),
        ("mypy src/ --ignore-missing-imports", "Type checking"),
    ]

    all_passed = True
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            all_passed = False

    if all_passed:
        print("\nAll quality checks passed!")
    else:
        print("\nSome quality checks failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
