# Git Submission Guide

## Important Files to Ignore

The `.gitignore` file has been created to exclude:

### 🔒 Sensitive Files (MUST IGNORE)

- `.env` - Contains your API keys (NEVER commit this!)
- Any files with passwords or secrets

### 📦 Generated Files (Should Ignore)

- `venv/` - Virtual environment (users create their own)
- `__pycache__/` - Python cache files
- `chroma_db/` - Vector database (regenerated from policies)
- `evaluation_results/` - Test outputs (regenerated)

### 🛠️ IDE Files (Should Ignore)

- `.vscode/` - VS Code settings
- `.idea/` - PyCharm settings
- `*.swp`, `*~` - Editor temp files

## What TO Include in Git

### ✅ Essential Files

- `app.py` - Main application
- `requirements.txt` - Dependencies
- `.env.example` - Config template (without secrets)
- `README.md` - Main documentation

### ✅ Source Code

- `src/` - All Python modules
- `static/` - Web assets
- `templates/` - HTML templates

### ✅ Documentation

- `docs/` - All documentation files
- `README.md` - Project overview

### ✅ Tests & Scripts

- `tests/` - Test scripts
- `scripts/` - Utility scripts
- `run_tests.py` - Test runner

### ✅ Configuration

- `.gitignore` - Git ignore rules
- `.env.example` - Environment template
- `requirements.txt` - Dependencies
- `.github/workflows/` - CI/CD pipeline

### ✅ Data

- `policies/` - Sample policy documents

## Git Commands

### Initial Setup

```bash
git init
git add .
git commit -m "Initial commit: RAG Company Policies System"
```

### Create GitHub Repository

1. Go to GitHub.com
2. Click "New Repository"
3. Name: "rag-company-policies"
4. Description: "RAG system for company policy Q&A with citations"
5. Keep it Public (for grading)
6. Don't initialize with README (we have one)
7. Click "Create repository"

### Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/rag-company-policies.git
git branch -M main
git push -u origin main
```

### Share with Grader

```bash
# Add quantic-grader as collaborator
# Or share the public repository URL
```

## Pre-Submission Checklist

### 1. Verify .gitignore

```bash
# Check what will be committed
git status

# Should NOT see:
# - .env (your API key!)
# - venv/
# - __pycache__/
# - chroma_db/
```

### 2. Test .env.example

```bash
# Make sure .env.example has placeholder
cat .env.example
# Should see: OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Verify All Tests Pass

```bash
python run_tests.py
```

### 4. Check Documentation

```bash
# Ensure README is up to date
cat README.md
```

## Repository Structure on GitHub

```
your-repo/
├── .github/workflows/ci.yml
├── .gitignore
├── README.md
├── requirements.txt
├── .env.example
├── app.py
├── run_tests.py
├── docs/
├── tests/
├── scripts/
├── policies/
├── src/
├── static/
└── templates/
```

## Important Notes

### ⚠️ NEVER Commit

- `.env` file (has your API key!)
- `venv/` folder
- `chroma_db/` folder
- Personal credentials

### ✅ ALWAYS Include

- `.env.example` (template without secrets)
- `requirements.txt`
- All source code
- Documentation
- Sample policies

## After Pushing

### Verify on GitHub

1. Go to your repository URL
2. Check files are there
3. Verify `.env` is NOT visible
4. Check README displays correctly
5. Verify CI/CD runs (GitHub Actions tab)

### Share with Grader

```
Repository URL: https://github.com/YOUR_USERNAME/rag-company-policies
```

## Quick Commands Reference

```bash
# Check status
git status

# Add all files (respects .gitignore)
git add .

# Commit
git commit -m "Your message"

# Push
git push

# View ignored files
git status --ignored
```

## Troubleshooting

### If you accidentally committed .env

```bash
# Remove from git but keep local file
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

### If you need to update .gitignore

```bash
# After updating .gitignore
git rm -r --cached .
git add .
git commit -m "Update .gitignore"
git push
```

## Final Checklist

- [ ] `.gitignore` created
- [ ] `.env` is ignored (not in git)
- [ ] `.env.example` is included
- [ ] All tests pass
- [ ] Documentation complete
- [ ] Repository pushed to GitHub
- [ ] Repository is public
- [ ] Shared with `quantic-grader`
- [ ] CI/CD pipeline runs successfully

You're ready to submit! 🚀
