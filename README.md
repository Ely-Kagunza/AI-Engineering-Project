# RAG Company Policies & Procedures

A Retrieval-Augmented Generation (RAG) application that answers questions about company policies and procedures using semantic search and AI-powered responses.

## Features

- Document ingestion and chunking pipeline
- Vector embeddings with Chroma database
- RAG-powered Q&A with citations
- **Clickable source links** - View full policy documents
- Web interface for interactive queries
- Evaluation metrics (groundedness, citation accuracy, latency)
- CI/CD pipeline with GitHub Actions
- 100% free technology stack

## Quick Start

1. **Setup Environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure API Keys**

   ```bash
   copy .env.example .env
   # Edit .env and add your OpenRouter API key (free)
   ```

3. **Ingest Documents**

   ```bash
   python src/ingest.py --corpus policies/
   ```

4. **Start Application**

   ```bash
   python app.py
   ```

5. **Access Web UI**
   - Open http://localhost:5000
   - Ask questions about company policies

## API Endpoints

- `GET /` - Web chat interface
- `POST /chat` - Submit questions (returns answer + citations)
- `GET /health` - Health check

## Evaluation

Run evaluation suite:

```bash
python src/evaluate.py
```

## Project Structure

```
├── app.py                    # Flask web application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── policies/                # Company policy documents
│   ├── employee-handbook.md
│   ├── pto-policy.md
│   ├── remote-work-policy.md
│   ├── expense-policy.md
│   └── security-policy.md
├── src/                     # Core application code
│   ├── ingest.py           # Document ingestion pipeline
│   ├── rag.py              # RAG implementation
│   └── evaluate.py         # Evaluation framework
├── static/                  # Web UI assets
│   ├── style.css
│   └── app.js
├── templates/              # HTML templates
│   └── index.html
├── tests/                  # Test scripts
│   ├── test_installation.py
│   ├── test_full_system.py
│   ├── test_openrouter.py
│   └── test_links.py
├── scripts/                # Utility scripts
│   └── list_free_models.py
├── docs/                   # Documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── SETUP.md
│   ├── QUICK_START.md
│   ├── design-and-evaluation.md
│   ├── ai-tooling.md
│   └── ... (more docs)
└── .github/workflows/      # CI/CD pipeline
    └── ci.yml
```

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Quick Start](docs/QUICK_START.md)
- [Design & Evaluation](docs/design-and-evaluation.md)
- [AI Tooling](docs/ai-tooling.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Features Summary](docs/FEATURES_SUMMARY.md)
- [Final Status](docs/FINAL_STATUS.md)
