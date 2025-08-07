import os

from setuptools import find_packages, setup

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dmps",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for [brief description]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrBinnacle/dmps",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.7b0",
            "isort>=5.9.3",
            "mypy>=0.910",
            "ruff>=0.1.0",
            "sphinx>=4.1.2",
            "sphinx-rtd-theme>=0.5.2",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "dmps=dmps.main:main",
        ],
    },
)
