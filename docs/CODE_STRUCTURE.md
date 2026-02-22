# Code Structure and Architecture

## Project Overview

This document provides a comprehensive guide to the codebase structure, module organization, and key components of the RAG Company Policies system.

## Directory Structure

```
project-root/
├── app.py                          # Flask web application (main entry point)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git ignore rules
│
├── src/                            # Core application modules
│   ├── __init__.py                # Package initialization
│   ├── rag.py                     # RAG system implementation
│   ├── ingest.py                  # Document ingestion pipeline
│   ├── evaluate.py                # Evaluation framework
│   └── __pycache__/               # Python cache (auto-generated)
│
├── static/                         # Frontend assets
│   ├── app.js                     # Client-side JavaScript
│   └── style.css                  # CSS styling
│
├── templates/                      # HTML templates
│   └── index.html                 # Main chat interface
│
├── policies/                       # Company policy documents (corpus)
│   ├── employee-handbook.md
│   ├── pto-policy.md
│   ├── remote-work-policy.md
│   ├── expense-policy.md
│   └── security-policy.md
│
├── tests/                          # Test suite
│   ├── test_installation.py       # Dependency verification
│   ├── test_full_system.py        # End-to-end tests
│   ├── test_openrouter.py         # API connectivity tests
│   └── test_links.py              # Citation link validation
│
├── chroma_db/                      # Vector database storage
│   ├── chroma.sqlite3             # Chroma database file
│   └── [collection-id]/           # Collection data
│
├── evaluation_results/             # Evaluation output
│   ├── detailed_results.csv       # Per-query results
│   ├── summary.json               # Aggregate metrics
│   ├── evaluation_charts.png      # Visualizations
│   └── evaluation_report.txt      # Text summary
│
├── scripts/                        # Utility scripts
│   └── list_free_models.py        # Free model discovery
│
├── docs/                           # Documentation
│   ├── PROJECT_OVERVIEW.md        # Project requirements
│   ├── SETUP.md                   # Setup instructions
│   ├── QUICK_START.md             # Quick start guide
│   ├── QUICK_REFERENCE.md         # Command reference
│   ├── FEATURES_SUMMARY.md        # Feature list
│   ├── design-and-evaluation.md   # Architecture & evaluation
│   ├── ai-tooling.md              # Technology stack
│   ├── CI_CD_GUIDE.md             # CI/CD documentation
│   └── CODE_STRUCTURE.md          # This file
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD
│
├── venv/                           # Python virtual environment
│
└── README.md                       # Project README

```

## Core Modules

### 1. app.py - Flask Web Application

**Purpose**: Main web server and API endpoints

**Key Components**:

```python
# Flask app initialization
app = Flask(__name__)

# RAG system initialization
rag_system = RAGSystem()
```

**Routes**:

| Route                | Method | Purpose                          |
| -------------------- | ------ | -------------------------------- |
| `/`                  | GET    | Web chat interface               |
| `/chat`              | POST   | Submit questions, return answers |
| `/health`            | GET    | Health check endpoint            |
| `/api/stats`         | GET    | System statistics                |
| `/policy/<filename>` | GET    | Serve policy documents           |

**Key Functions**:

- `index()` - Renders main chat interface
- `chat()` - Processes user questions and returns RAG responses
- `health()` - Returns system health status
- `stats()` - Returns system statistics
- `serve_policy()` - Serves policy documents with security checks

**Error Handling**:

- 404 handler for missing endpoints
- 500 handler for internal errors
- Graceful error messages for API failures

### 2. src/rag.py - RAG System Implementation

**Purpose**: Core RAG logic for retrieval and generation

**Classes**:

#### RAGSystem

Main class for RAG operations.

**Initialization**:

```python
RAGSystem(
    chroma_persist_dir="./chroma_db",
    embedding_model="all-MiniLM-L6-v2",
    llm_model="liquid/lfm-2.5-1.2b-instruct:free",
    top_k=5
)
```

**Key Methods**:

| Method                               | Purpose                                 |
| ------------------------------------ | --------------------------------------- |
| `query(question)`                    | Process user question and return answer |
| `_retrieve_documents(question)`      | Semantic search for relevant chunks     |
| `_generate_response(question, docs)` | Generate answer using LLM               |
| `_extract_citations(docs)`           | Extract citation information            |
| `_extract_sources(docs)`             | Extract unique source files             |
| `health_check()`                     | Check system health                     |

**Data Flow**:

```
User Question
    ↓
query()
    ├─ _retrieve_documents()  → Semantic search
    ├─ _generate_response()   → LLM generation
    ├─ _extract_citations()   → Citation extraction
    └─ _extract_sources()     → Source extraction
    ↓
Response with Citations
```

#### QueryValidator

Utility class for query validation and preprocessing.

**Methods**:

- `is_policy_related(question)` - Check if question is about policies
- `preprocess_question(question)` - Clean and normalize question

**Key Features**:

- Keyword-based policy detection
- Question normalization (whitespace, punctuation)
- Guardrails for off-topic questions

### 3. src/ingest.py - Document Ingestion Pipeline

**Purpose**: Parse, chunk, and embed documents

**Classes**:

#### DocumentProcessor

Handles document parsing and chunking.

**Key Methods**:

| Method                         | Purpose                 |
| ------------------------------ | ----------------------- |
| `process_file(file_path)`      | Process single document |
| `_process_markdown(file_path)` | Parse markdown files    |
| `_process_text(file_path)`     | Parse text files        |
| `_process_pdf(file_path)`      | Parse PDF files         |
| `_process_docx(file_path)`     | Parse Word documents    |
| `_process_html(file_path)`     | Parse HTML files        |

**Chunking Strategy**:

- **Chunk Size**: 800 characters
- **Overlap**: 150 characters
- **Method**: Character-based splitting with metadata

**Output**:

Each chunk includes:

```python
{
    'text': 'chunk content...',
    'metadata': {
        'title': 'Document Title',
        'source_id': 'policies/document.md',
        'chunk_id': 'chunk_0'
    }
}
```

**Supported Formats**:

- Markdown (.md)
- Plain text (.txt)
- PDF (.pdf)
- Word documents (.docx)
- HTML (.html)

### 4. src/evaluate.py - Evaluation Framework

**Purpose**: Measure system performance and quality

**Classes**:

#### RAGEvaluator

Evaluates RAG system performance.

**Key Methods**:

| Method                          | Purpose                       |
| ------------------------------- | ----------------------------- |
| `run_full_evaluation()`         | Run complete evaluation suite |
| `_load_evaluation_queries()`    | Load test queries             |
| `_evaluate_groundedness()`      | Calculate groundedness score  |
| `_evaluate_citation_accuracy()` | Calculate citation accuracy   |
| `_calculate_latency_metrics()`  | Calculate latency statistics  |

**Metrics**:

1. **Groundedness**: % of answers supported by evidence
2. **Citation Accuracy**: % of relevant citations
3. **Latency**: P50, P95, mean, min, max response times

**Test Queries**: 25 queries across 5 categories

- PTO Policies (6 queries)
- Remote Work (4 queries)
- Expenses (5 queries)
- Security (6 queries)
- Employee Handbook (4 queries)

**Output**:

- `evaluation_results/detailed_results.csv` - Per-query results
- `evaluation_results/summary.json` - Aggregate metrics
- `evaluation_results/evaluation_charts.png` - Visualizations
- `evaluation_results/evaluation_report.txt` - Text summary

## Frontend Components

### templates/index.html

**Purpose**: Main chat interface

**Key Elements**:

- Chat message display area
- User input form
- Source citations display
- Sidebar with system info
- Bootstrap 5 styling

**Features**:

- Real-time message display
- Clickable source links
- Responsive design
- Mobile-friendly layout

### static/app.js

**Purpose**: Client-side JavaScript logic

**Key Functions**:

- `sendMessage()` - Send question to API
- `displayMessage()` - Display message in chat
- `displaySources()` - Show source citations
- `formatResponse()` - Format API response
- `handleError()` - Handle API errors

**API Integration**:

```javascript
POST /chat
{
    "question": "user question"
}

Response:
{
    "answer": "response text",
    "citations": [...],
    "sources": [...],
    "latency_ms": 2410
}
```

### static/style.css

**Purpose**: Styling and layout

**Key Styles**:

- Chat interface layout
- Message styling
- Citation formatting
- Responsive breakpoints
- Dark/light theme support

## Data Flow Architecture

### Document Ingestion Flow

```
Policy Documents (MD, PDF, DOCX, TXT, HTML)
    ↓
DocumentProcessor.process_file()
    ├─ Parse document content
    ├─ Clean and normalize text
    └─ Split into chunks (800 chars, 150 overlap)
    ↓
Chunk with Metadata
    ├─ text: chunk content
    ├─ title: document title
    ├─ source_id: file path
    └─ chunk_id: chunk identifier
    ↓
SentenceTransformer.encode()
    ├─ Generate embeddings (384 dimensions)
    └─ Create vector representation
    ↓
Chroma Vector Database
    ├─ Store embeddings
    ├─ Store metadata
    └─ Index for similarity search
```

### Query Processing Flow

```
User Question
    ↓
QueryValidator.preprocess_question()
    ├─ Remove extra whitespace
    ├─ Add punctuation
    └─ Normalize text
    ↓
RAGSystem.query()
    ├─ _retrieve_documents()
    │   ├─ Encode question (SentenceTransformer)
    │   ├─ Search Chroma (cosine similarity)
    │   └─ Return top-5 chunks
    │
    ├─ _generate_response()
    │   ├─ Format context from chunks
    │   ├─ Create prompt with system instructions
    │   ├─ Call OpenRouter API
    │   └─ Return generated response
    │
    ├─ _extract_citations()
    │   ├─ Extract source information
    │   ├─ Create citation objects
    │   └─ Generate document links
    │
    └─ _extract_sources()
        ├─ Get unique source files
        └─ Return source list
    ↓
Response Object
    ├─ answer: generated response
    ├─ citations: source citations
    ├─ sources: source files
    └─ retrieved_chunks: count
    ↓
Flask API Response (JSON)
    ↓
Frontend Display
    ├─ Show answer
    ├─ Display citations with links
    └─ Show metadata
```

## Configuration and Environment

### Environment Variables

**Required**:

```bash
OPENROUTER_API_KEY=your_api_key_here
```

**Optional**:

```bash
FLASK_DEBUG=False              # Debug mode
PORT=5000                      # Server port
CHROMA_DB_PATH=./chroma_db    # Database path
```

### Configuration Files

- `.env` - Local environment (not committed)
- `.env.example` - Template for setup
- `requirements.txt` - Python dependencies

## Dependencies

### Core Dependencies

| Package               | Version  | Purpose            |
| --------------------- | -------- | ------------------ |
| flask                 | 3.0.0    | Web framework      |
| chromadb              | >=0.4.22 | Vector database    |
| sentence-transformers | >=2.2.2  | Embeddings         |
| requests              | 2.31.0   | HTTP client        |
| python-dotenv         | 1.0.1    | Environment config |

### Document Processing

| Package        | Version | Purpose          |
| -------------- | ------- | ---------------- |
| pypdf2         | 3.0.1   | PDF parsing      |
| python-docx    | 1.1.0   | Word documents   |
| beautifulsoup4 | 4.12.3  | HTML parsing     |
| markdown       | 3.5.2   | Markdown parsing |

### Data Processing

| Package | Version  | Purpose             |
| ------- | -------- | ------------------- |
| numpy   | >=1.24.0 | Numerical computing |
| pandas  | >=2.0.0  | Data manipulation   |

### Evaluation

| Package      | Version  | Purpose                   |
| ------------ | -------- | ------------------------- |
| scikit-learn | >=1.3.0  | ML utilities              |
| matplotlib   | >=3.7.0  | Plotting                  |
| seaborn      | >=0.12.0 | Statistical visualization |

### Development

| Package | Version  | Purpose           |
| ------- | -------- | ----------------- |
| pytest  | >=7.4.0  | Testing framework |
| black   | >=23.0.0 | Code formatter    |
| flake8  | >=6.0.0  | Linter            |

## Testing

### Test Files

**tests/test_installation.py**

- Verifies all dependencies are installed
- Checks Python version compatibility
- Validates environment setup

**tests/test_full_system.py**

- End-to-end system tests
- Tests document ingestion
- Tests query processing
- Tests response generation

**tests/test_openrouter.py**

- Tests OpenRouter API connectivity
- Validates API key configuration
- Tests model availability

**tests/test_links.py**

- Tests citation link generation
- Validates policy document serving
- Tests link accessibility

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_full_system.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

## CI/CD Pipeline

### GitHub Actions Workflow

**File**: `.github/workflows/ci.yml`

**Triggers**:

- Push to main branch
- Pull requests

**Steps**:

1. Setup Python environment
2. Install dependencies
3. Run code quality checks (black, flake8)
4. Run security scanning (bandit)
5. Run tests
6. Optional deployment

## Key Design Patterns

### 1. Separation of Concerns

- **app.py**: Web interface and API
- **src/rag.py**: RAG logic
- **src/ingest.py**: Document processing
- **src/evaluate.py**: Evaluation framework

### 2. Configuration Management

- Environment variables for sensitive data
- Configurable parameters (chunk size, top-k, etc.)
- Flexible model selection

### 3. Error Handling

- Try-catch blocks for API calls
- Graceful degradation
- Informative error messages
- Logging for debugging

### 4. Modularity

- Reusable components
- Clear interfaces between modules
- Easy to extend and modify

## Performance Considerations

### Optimization Points

1. **Embedding Generation**: ~10ms per query (local)
2. **Vector Search**: ~50-100ms (Chroma)
3. **LLM Inference**: ~2,300-3,600ms (bottleneck)
4. **Total Latency**: ~2,400-3,700ms

### Caching Opportunities

- Response caching for common queries
- Embedding caching
- Model caching

### Scalability

- Local deployment suitable for <100 queries/day
- Can scale to cloud deployment (Render, Railway)
- Horizontal scaling with load balancing

## Security Considerations

### Input Validation

- Query validation and sanitization
- File path validation for policy serving
- API key management

### Data Protection

- HTTPS for all communications
- Environment variable for API keys
- No persistent query logging

### Rate Limiting

- OpenRouter free tier: 50 requests/day
- Can implement custom rate limiting
- Fallback models for redundancy

## Extension Points

### Easy to Extend

1. **Add New Document Types**: Extend DocumentProcessor
2. **Add New Metrics**: Extend RAGEvaluator
3. **Add New Models**: Update RAGSystem initialization
4. **Add New Routes**: Add to app.py

### Future Enhancements

- Response caching layer
- Re-ranking for better citations
- Conversation memory
- Multi-modal support
- Knowledge graph integration

---

**Last Updated**: February 22, 2026
**Status**: Complete and Accurate
**Verification**: All information verified against source code
