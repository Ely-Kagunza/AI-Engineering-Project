# Git Quick Commands

## 🚀 Quick Submission (Copy & Paste)

```bash
# 1. Check what will be committed
git status

# 2. Add all files (respects .gitignore)
git add .

# 3. Commit with message
git commit -m "Complete RAG system with clickable citations and organized structure"

# 4. Push to GitHub
git push origin main
```

## ⚠️ Before You Commit - VERIFY

```bash
# Check status (should NOT see .env or venv/)
git status

# View what's ignored
git status --ignored

# Should see in "Ignored files":
# - venv/
# - .env
# - __pycache__/
# - chroma_db/
```

## 🔍 Verify .env is NOT Tracked

```bash
# This should return nothing (good!)
git ls-files | grep "\.env$"

# This should show .env.example (good!)
git ls-files | grep "\.env"
```

## 🛠️ Common Git Commands

### Check Status

```bash
git status                 # See what's changed
git status --ignored       # See ignored files too
git diff                   # See changes in detail
```

### Add Files

```bash
git add .                  # Add all files
git add filename.py        # Add specific file
git add docs/              # Add entire folder
```

### Commit

```bash
git commit -m "Your message here"
git commit -am "Add and commit in one step"
```

### Push

```bash
git push                   # Push to current branch
git push origin main       # Push to main branch
```

### View History

```bash
git log                    # See commit history
git log --oneline          # Compact view
```

## 🔧 Fix Common Issues

### Accidentally Staged .env

```bash
# Remove from staging (keeps local file)
git restore --staged .env
```

### Accidentally Committed .env

```bash
# Remove from git but keep local
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

### Update .gitignore After Commits

```bash
# Clear cache and re-add everything
git rm -r --cached .
git add .
git commit -m "Update .gitignore"
git push
```

### Undo Last Commit (Not Pushed)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes, undo commit
git reset --hard HEAD~1
```

## 📦 Initial Setup (If Not Done)

```bash
# Initialize git
git init

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/rag-company-policies.git

# Set main branch
git branch -M main

# First push
git push -u origin main
```

## ✅ Pre-Push Checklist

Run these commands before pushing:

```bash
# 1. Run tests
python run_tests.py

# 2. Check git status
git status

# 3. Verify .env is ignored
git status --ignored | grep ".env"

# 4. Check what will be committed
git diff --cached --name-only
```

## 🎯 What Should Be in Git

```bash
# These should be tracked:
git ls-files | grep -E "(\.py$|\.md$|\.txt$|\.yml$|\.css$|\.js$|\.html$)"
```

Should include:

- ✅ All .py files
- ✅ All .md files
- ✅ requirements.txt
- ✅ .env.example
- ✅ .gitignore
- ✅ All docs/
- ✅ All src/
- ✅ All tests/
- ✅ All policies/

## ❌ What Should NOT Be in Git

```bash
# These should be ignored:
git status --ignored
```

Should show:

- ❌ venv/
- ❌ .env
- ❌ **pycache**/
- ❌ chroma_db/
- ❌ .vscode/

## 🔒 Security Verification

```bash
# CRITICAL: Verify .env is NOT in git
git ls-files | grep "^\.env$"
# Should return NOTHING

# Verify .env.example IS in git
git ls-files | grep "\.env.example"
# Should return: .env.example

# Check for any API keys in committed files
git grep -i "sk-or-v1"
# Should return NOTHING (or only in .env.example as placeholder)
```

## 📊 Repository Stats

```bash
# Count files in git
git ls-files | wc -l

# List all tracked files
git ls-files

# Show repository size
git count-objects -vH
```

## 🎉 Final Push Command

```bash
# All-in-one submission command
git add . && \
git commit -m "Complete RAG Company Policies System

- RAG implementation with free LLM
- Clickable source citations
- Organized project structure
- Complete documentation
- All tests passing
- Ready for demo and submission" && \
git push origin main
```

## 📞 Need Help?

See detailed guide: `docs/GIT_SUBMISSION_GUIDE.md`

## ✅ Success Indicators

After pushing, verify on GitHub:

- ✅ Green checkmark on CI/CD
- ✅ README displays correctly
- ✅ All files visible
- ✅ .env is NOT visible
- ✅ Repository is public

You're ready to submit! 🚀
