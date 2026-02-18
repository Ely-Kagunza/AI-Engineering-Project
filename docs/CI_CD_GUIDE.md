# CI/CD Pipeline Guide

## Overview

The project uses GitHub Actions for continuous integration and deployment. Every push to `main` or `develop` branches triggers automated tests.

## Pipeline Stages

### 1. Test Stage

Runs on every push and pull request.

**Steps:**

- ✅ Set up Python 3.11
- ✅ Cache dependencies for faster builds
- ✅ Install requirements
- ✅ Lint with flake8 (syntax errors)
- ✅ Format check with black
- ✅ Run installation test
- ✅ Test document processing
- ✅ Test module imports
- ✅ Verify policy documents exist
- ✅ Test Flask app startup

### 2. Security Scan Stage

Runs after tests pass.

**Steps:**

- ✅ Scan code with bandit
- ✅ Check for secrets in code
- ✅ Generate security report

### 3. Build Summary Stage

Generates a summary of the build.

**Steps:**

- ✅ Create build summary
- ✅ Display test results
- ✅ Show project status

## What Gets Tested

### Installation Test

```bash
python tests/test_installation.py
```

- Verifies all packages import correctly
- Tests document processing
- Checks text chunking
- Validates environment setup

### Document Processing Test

- Processes actual policy files
- Creates text chunks
- Validates chunk creation
- Tests all document types

### Import Tests

- Tests `src.ingest` module
- Tests `src.rag` module
- Tests `app` module
- Ensures no import errors

### Flask App Test

- Verifies app can be imported
- Tests initialization
- Checks for startup errors

### Security Tests

- Scans for code vulnerabilities
- Checks for exposed secrets
- Validates secure coding practices

## Viewing Results

### On GitHub

1. Go to your repository
2. Click "Actions" tab
3. See all workflow runs
4. Click on a run to see details

### Build Status Badge

Add to README.md:

```markdown
![CI/CD](https://github.com/YOUR_USERNAME/rag-company-policies/workflows/CI%2FCD%20Pipeline/badge.svg)
```

## What Triggers the Pipeline

### Automatic Triggers

- Push to `main` branch
- Push to `develop` branch
- Pull request to `main` branch

### Manual Trigger

You can also run manually:

1. Go to Actions tab
2. Select "CI/CD Pipeline"
3. Click "Run workflow"

## Expected Results

### ✅ Successful Build

```
✓ Test stage passed
✓ Security scan passed
✓ Build summary generated
```

### ❌ Failed Build

If tests fail:

1. Check the error message
2. Fix the issue locally
3. Run tests: `python run_tests.py`
4. Commit and push again

## Local Testing Before Push

Always run tests locally first:

```bash
# Run all tests
python run_tests.py

# Run specific test
python tests/test_installation.py

# Check code style
black --check .
flake8 . --exclude=venv,chroma_db
```

## Pipeline Configuration

The pipeline is defined in:

```
.github/workflows/ci.yml
```

### Key Features

- **Caching**: Pip dependencies cached for speed
- **Parallel Jobs**: Tests and security run in parallel
- **Continue on Error**: Linting doesn't fail the build
- **Build Summary**: Nice summary in GitHub UI

## Troubleshooting

### Build Fails on Import

**Issue**: Module not found
**Solution**: Check `requirements.txt` is complete

### Build Fails on Flake8

**Issue**: Code style errors
**Solution**: Run `black .` locally

### Build Fails on Tests

**Issue**: Test failures
**Solution**: Run `python run_tests.py` locally

### Build is Slow

**Issue**: Long build times
**Solution**: Dependencies are cached, should be fast after first run

## Advanced Configuration

### Adding New Tests

1. Create test in `tests/` folder
2. Add step to `.github/workflows/ci.yml`
3. Push and verify

### Changing Python Version

Edit `.github/workflows/ci.yml`:

```yaml
- name: Set up Python 3.11
  uses: actions/setup-python@v4
  with:
    python-version: '3.11' # Change this
```

### Adding Deployment

Uncomment the deploy job in `ci.yml` and configure:

- Deployment target (Render, Railway, etc.)
- Environment variables
- Health checks

## Best Practices

### Before Pushing

1. ✅ Run tests locally
2. ✅ Check code style
3. ✅ Verify no secrets in code
4. ✅ Update documentation if needed

### Commit Messages

Use clear, descriptive messages:

```bash
git commit -m "Add feature: clickable source links"
git commit -m "Fix: Update CI/CD to run actual tests"
git commit -m "Docs: Update setup guide"
```

### Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch
- Feature branches - For new features

## Monitoring

### Check Build Status

```bash
# View recent builds
gh run list

# View specific run
gh run view RUN_ID
```

### Email Notifications

GitHub sends emails on:

- Build failures
- First successful build after failure

## Security

### What's Checked

- Code vulnerabilities (bandit)
- Exposed secrets (grep)
- Dependency vulnerabilities

### What's Protected

- `.env` file (not in repo)
- API keys (environment variables)
- Sensitive data (gitignored)

## Performance

### Build Time

- First build: ~3-5 minutes
- Cached builds: ~1-2 minutes

### Optimization

- Dependencies cached
- Parallel jobs
- Minimal test data

## Summary

The CI/CD pipeline ensures:

- ✅ Code quality
- ✅ Tests pass
- ✅ Security checks
- ✅ Ready for deployment

Every push is automatically tested, giving you confidence in your code! 🚀
