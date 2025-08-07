#!/usr/bin/env python3
"""
Build script for creating DMPS distribution packages.
"""

import subprocess
import sys
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def clean_build_dirs():
    """Clean previous build artifacts"""
    dirs_to_clean = ["build", "dist", "src/dmps.egg-info"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"🧹 Cleaning {dir_name}...")
            shutil.rmtree(dir_path)


def main():
    """Main build process"""
    print("🚀 Building DMPS package for PyPI distribution")
    print("=" * 50)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Install build dependencies
    run_command(
        f"{sys.executable} -m pip install --upgrade build twine",
        "Installing build dependencies"
    )
    
    # Run tests
    run_command(
        f"{sys.executable} -m pytest tests/ -v",
        "Running test suite"
    )
    
    # Build package
    run_command(
        f"{sys.executable} -m build",
        "Building distribution packages"
    )
    
    # Check package
    run_command(
        f"{sys.executable} -m twine check dist/*",
        "Checking package integrity"
    )
    
    print("\n🎉 Package build completed successfully!")
    print("\nNext steps:")
    print("1. Test installation: pip install dist/dmps-0.1.0-py3-none-any.whl")
    print("2. Upload to TestPyPI: python -m twine upload --repository testpypi dist/*")
    print("3. Upload to PyPI: python -m twine upload dist/*")
    
    # Show package contents
    dist_files = list(Path("dist").glob("*"))
    if dist_files:
        print(f"\n📦 Generated packages:")
        for file in dist_files:
            print(f"  - {file.name}")


if __name__ == "__main__":
    main()