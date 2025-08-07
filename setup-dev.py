#!/usr/bin/env python3
"""
Development environment setup script
"""
import subprocess
import sys


def install_tools():
    """Install development tools"""
    tools = [
        "black",
        "ruff",
        "isort",
        "mypy",
        "pre-commit",
        "pytest",
        "bandit",
        "safety",
    ]

    print("Installing development tools...")
    for tool in tools:
        subprocess.run([sys.executable, "-m", "pip", "install", tool])

    print("Setting up pre-commit hooks...")
    subprocess.run(["pre-commit", "install"])

    print("Development environment ready!")
    print("\nUsage:")
    print("  python scripts/format.py  - Run quality checks")
    print("  pre-commit run --all-files - Run all hooks")


if __name__ == "__main__":
    install_tools()
