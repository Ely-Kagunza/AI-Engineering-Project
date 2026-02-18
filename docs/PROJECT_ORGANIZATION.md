# Project Organization

## Directory Structure

The project is organized into logical folders for better maintainability:

### Root Directory

```
AI Project/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example           # Environment template
├── run_tests.py           # Test runner script
└── README.md              # Main documentation
```

### `/policies/` - Policy Documents

Contains all company policy documents that are indexed and searchable:

```
policies/
├── employee-handbook.md
├── pto-policy.md
├── remote-work-policy.md
├── expense-policy.md
└── security-policy.md
```

**Purpose**: Source documents for the RAG system

### `/src/` - Core Application Code

Contains the main application logic:

```
src/
├── __init__.py           # Package initialization
├── ingest.py            # Document ingestion pipeline
├── rag.py               # RAG system implementation
└── evaluate.py          # Evaluation framework
```

**Purpose**: Core RAG functionality

### `/static/` - Web UI Assets

Frontend resources for the web interface:

```
static/
├── style.css            # UI styling
└── app.js               # Frontend JavaScript
```

**Purpose**: Web interface assets

### `/templates/` - HTML Templates

Flask templates for the web interface:

```
templates/
└── index.html           # Main chat interface
```

**Purpose**: Web page templates

### `/tests/` - Test Scripts

All testing and verification scripts:

```
tests/
├── test_installation.py  # Verify installation
├── test_openrouter.py   # Test API connection
├── test_links.py        # Verify file links
└── test_full_system.py  # End-to-end test
```

**Purpose**: Quality assurance and verification

**Run all tests**: `python run_tests.py`

### `/scripts/` - Utility Scripts

Helper scripts for development and maintenance:

```
scripts/
└── list_free_models.py  # List available free models
```

**Purpose**: Development utilities

### `/docs/` - Documentation

All project documentation:

```
docs/
├── PROJECT_OVERVIEW.md          # Original requirements
├── SETUP.md                     # Setup instructions
├── QUICK_START.md              # Quick start guide
├── QUICK_REFERENCE.md          # Quick reference card
├── START_APP.md                # App startup guide
├── design-and-evaluation.md    # Architecture & evaluation
├── ai-tooling.md               # Technology stack
├── FEATURES_SUMMARY.md         # Complete feature list
├── PROJECT_STATUS.md           # Development status
├── FINAL_STATUS.md             # Final completion status
├── FIXED_MODEL_ISSUE.md        # Model troubleshooting
├── CLICKABLE_LINKS_ADDED.md    # New features guide
└── PROJECT_ORGANIZATION.md     # This file
```

**Purpose**: Comprehensive project documentation

### `/.github/workflows/` - CI/CD

GitHub Actions workflows:

```
.github/workflows/
└── ci.yml               # Continuous integration pipeline
```

**Purpose**: Automated testing and deployment

### `/chroma_db/` - Vector Database

Chroma database storage (created after ingestion):

```
chroma_db/
└── [database files]     # Vector embeddings and metadata
```

**Purpose**: Persistent vector storage

**Note**: Created by running `python src/ingest.py --corpus policies/`

### `/venv/` - Virtual Environment

Python virtual environment (not in git):

```
venv/
└── [Python packages]
```

**Purpose**: Isolated Python environment

## File Categories

### Configuration Files

- `.env` - Environment variables (API keys, settings)
- `.env.example` - Template for environment setup
- `requirements.txt` - Python package dependencies

### Application Files

- `app.py` - Flask web server
- `src/ingest.py` - Document processing
- `src/rag.py` - RAG implementation
- `src/evaluate.py` - Evaluation system

### Frontend Files

- `templates/index.html` - Web interface
- `static/style.css` - Styling
- `static/app.js` - Client-side logic

### Testing Files

- `tests/test_*.py` - Test scripts
- `run_tests.py` - Test runner

### Documentation Files

- `README.md` - Main readme
- `docs/*.md` - Detailed documentation

### Data Files

- `policies/*.md` - Policy documents
- `chroma_db/` - Vector database

## Quick Navigation

### Getting Started

1. Read: `README.md`
2. Setup: `docs/SETUP.md`
3. Quick Start: `docs/QUICK_START.md`

### Development

1. Architecture: `docs/design-and-evaluation.md`
2. Technology: `docs/ai-tooling.md`
3. Features: `docs/FEATURES_SUMMARY.md`

### Testing

1. Run tests: `python run_tests.py`
2. Individual test: `python tests/test_installation.py`

### Deployment

1. CI/CD: `.github/workflows/ci.yml`
2. Status: `docs/FINAL_STATUS.md`

## Best Practices

### Adding New Files

**Policy Documents**

- Add to: `policies/`
- Format: Markdown (.md) preferred
- Re-run: `python src/ingest.py --corpus policies/`

**Test Scripts**

- Add to: `tests/`
- Name: `test_*.py`
- Update: `run_tests.py` if needed

**Documentation**

- Add to: `docs/`
- Format: Markdown (.md)
- Update: `README.md` links

**Utility Scripts**

- Add to: `scripts/`
- Purpose: Development helpers

### File Naming Conventions

- **Python files**: `lowercase_with_underscores.py`
- **Documentation**: `UPPERCASE_WITH_UNDERSCORES.md` or `lowercase-with-dashes.md`
- **Test files**: `test_*.py`
- **Config files**: `.lowercase` or `lowercase.ext`

## Maintenance

### Regular Tasks

1. **Update Dependencies**

   ```bash
   pip install --upgrade -r requirements.txt
   pip freeze > requirements.txt
   ```

2. **Run Tests**

   ```bash
   python run_tests.py
   ```

3. **Update Documentation**
   - Keep `docs/` files current
   - Update `README.md` for major changes

4. **Clean Up**

   ```bash
   # Remove Python cache
   find . -type d -name __pycache__ -exec rm -rf {} +

   # Remove test artifacts
   rm -rf evaluation_results/
   ```

## Git Ignore

Files/folders not tracked in git:

- `.env` (contains secrets)
- `venv/` (virtual environment)
- `chroma_db/` (generated database)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `evaluation_results/` (test outputs)

## Summary

This organization provides:

- ✅ Clear separation of concerns
- ✅ Easy navigation
- ✅ Logical grouping
- ✅ Scalable structure
- ✅ Professional layout

All files are now properly organized for development, testing, and deployment!
