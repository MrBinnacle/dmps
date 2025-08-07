# DMPS Release Guide

This guide explains how to release DMPS to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
2. **API Tokens**: Generate API tokens for both PyPI and TestPyPI
3. **GitHub Secrets**: Add tokens as repository secrets:
   - `PYPI_API_TOKEN` - Your PyPI API token
   - `TEST_PYPI_API_TOKEN` - Your TestPyPI API token

## Release Process

### 1. Prepare Release

```bash
# Update version in pyproject.toml and setup.cfg
# Update CHANGELOG.md with new version
# Commit changes
git add .
git commit -m "Prepare release v0.1.0"
git push
```

### 2. Test Build Locally

```bash
# Clean previous builds
rm -rf build/ dist/ src/*.egg-info/

# Build package
python -m build

# Check package
python -m twine check dist/*

# Test installation
pip install dist/dmps-*.whl --force-reinstall
dmps --version
```

### 3. Test on TestPyPI

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ dmps
```

### 4. Create GitHub Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: `v0.1.0`
4. Title: `DMPS v0.1.0`
5. Description: Copy from CHANGELOG.md
6. Publish release

### 5. Automatic PyPI Upload

The GitHub Actions workflow will automatically:
- Run tests
- Build package
- Upload to PyPI

### 6. Manual PyPI Upload (if needed)

```bash
# Upload to PyPI
python -m twine upload dist/*
```

## Post-Release

1. **Verify Installation**:
   ```bash
   pip install dmps
   dmps --version
   ```

2. **Update Documentation**: Ensure README and docs reflect new version

3. **Announce Release**: Share on relevant platforms

## Version Bumping

Update version in these files:
- `pyproject.toml` - `version = "0.1.1"`
- `setup.cfg` - `version = 0.1.1`
- `src/dmps/__init__.py` - `__version__ = '0.1.1'`
- `src/dmps/cli.py` - version string in argparse

## Troubleshooting

### Build Issues
- Ensure `setup.py` exists and calls `setup()`
- Check `pyproject.toml` syntax
- Verify all files are included in `MANIFEST.in`

### Upload Issues
- Check API token permissions
- Verify package name availability
- Ensure version number is unique

### Installation Issues
- Test in clean virtual environment
- Check dependencies
- Verify entry points work

## Automated Release Workflow

The repository includes:
- `.github/workflows/publish.yml` - Automated PyPI publishing
- `build_package.py` - Local build script
- Comprehensive testing before release

## Security

- Never commit API tokens
- Use GitHub Secrets for sensitive data
- Regularly rotate API tokens
- Review package contents before upload