# AI Tooling and Technology Stack

## Overview

This document details the AI/ML tools, models, and technologies used in the RAG Company Policies system, including rationale for choices, alternatives considered, and implementation details.

## Core AI Components

### 1. Embedding Model

#### Selected: `all-MiniLM-L6-v2`

- **Provider**: Sentence Transformers (HuggingFace)
- **Architecture**: MiniLM (distilled BERT)
- **Dimensions**: 384
- **Model Size**: ~23MB
- **License**: Apache 2.0

#### Rationale

- **Performance**: Strong semantic similarity performance on STS benchmarks
- **Efficiency**: Fast inference (~10ms per query on CPU)
- **Size**: Compact model suitable for local deployment
- **Cost**: Free, no API costs
- **Multilingual**: Good English performance with some multilingual capability

#### Alternatives Considered

1. **OpenAI text-embedding-ada-002**
   - Pros: Higher quality embeddings, 1536 dimensions
   - Cons: API costs, external dependency, slower
   - Decision: Rejected due to cost and latency concerns

2. **all-mpnet-base-v2**
   - Pros: Higher quality than MiniLM, 768 dimensions
   - Cons: Larger model size, slower inference
   - Decision: Rejected for speed/size trade-off

3. **Cohere Embed (free tier)**
   - Pros: Commercial quality, good performance
   - Cons: API dependency, rate limits
   - Decision: Considered as fallback option

#### Implementation Details

```python
from sentence_transformers import SentenceTransformer

# Model initialization
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embedding generation
embeddings = model.encode(texts, show_progress_bar=True)
```

### 2. Large Language Model (LLM)

#### Primary: OpenRouter (Free Models)

- **Provider**: OpenRouter
- **Models**:
  - microsoft/phi-3-mini-128k-instruct:free
  - meta-llama/llama-3.1-8b-instruct:free
  - google/gemma-2-9b-it:free
- **Context Length**: 128k tokens (Phi-3), 8k tokens (others)
- **Cost**: Free tier with generous limits

#### Rationale

- **Cost**: Completely free for development and moderate production use
- **Quality**: High-quality open-source models with good instruction following
- **Variety**: Multiple model options for comparison and fallback
- **Speed**: Reasonable response times (2-5 seconds)
- **Integration**: OpenAI-compatible API for easy integration

#### Alternatives Considered

1. **OpenAI GPT-3.5-turbo**
   - Pros: Excellent quality, fast response times
   - Cons: API costs ($0.0015-0.002/1K tokens)
   - Decision: Rejected due to cost requirements

2. **Hugging Face Inference API**
   - Pros: Free tier available, many model options
   - Cons: Rate limits, variable performance
   - Decision: Considered as alternative option

3. **Local Models (Ollama)**
   - Pros: No API costs, full control, privacy
   - Cons: Hardware requirements, setup complexity
   - Decision: Rejected for simplicity requirements

#### Implementation Details

```python
import requests

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000"
}

data = {
    "model": "microsoft/phi-3-mini-128k-instruct:free",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ],
    "max_tokens": 500,
    "temperature": 0.1
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=data
)
```

### 3. Vector Database

#### Selected: Chroma

- **Type**: Vector database with embeddings
- **Storage**: Local persistent storage
- **Language**: Python native
- **License**: Apache 2.0

#### Rationale

- **Simplicity**: Easy setup and configuration
- **Local Deployment**: No external dependencies
- **Python Integration**: Native Python API
- **Performance**: Sufficient for document corpus size
- **Cost**: Free, no hosting costs

#### Alternatives Considered

1. **Pinecone**
   - Pros: Managed service, high performance, scalability
   - Cons: API costs, external dependency
   - Decision: Rejected due to cost and complexity

2. **Weaviate**
   - Pros: Open source, good performance, GraphQL API
   - Cons: More complex setup, resource intensive
   - Decision: Rejected for simplicity requirements

3. **FAISS**
   - Pros: High performance, Facebook-backed
   - Cons: Lower-level API, no built-in persistence
   - Decision: Rejected for ease of use

#### Implementation Details

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_collection(
    name="company_policies",
    metadata={"description": "Company policies and procedures"}
)
```

## Document Processing Pipeline

### Text Extraction Tools

#### Markdown: `markdown` + `BeautifulSoup4`

- **Purpose**: Parse markdown files and extract clean text
- **Rationale**: Handles formatting while preserving structure
- **Alternative**: Direct text parsing (loses structure)

#### PDF: `PyPDF2`

- **Purpose**: Extract text from PDF documents
- **Rationale**: Lightweight, pure Python implementation
- **Limitations**: May struggle with complex layouts
- **Alternative**: `pdfplumber` (more robust but heavier)

#### Word Documents: `python-docx`

- **Purpose**: Extract text from .docx files
- **Rationale**: Standard library for Word document processing
- **Limitations**: Only supports .docx, not legacy .doc

#### HTML: `BeautifulSoup4`

- **Purpose**: Parse HTML and extract clean text
- **Rationale**: Robust HTML parsing with text extraction

### Text Chunking Strategy

#### Approach: Sentence-Aware Chunking

```python
def chunk_document(self, document, chunk_size=1000, overlap=200):
    sentences = text.split('. ')
    # Build chunks respecting sentence boundaries
    # Add overlap from previous chunk
```

#### Parameters

- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters
- **Method**: Sentence boundary preservation

#### Rationale

- Maintains semantic coherence
- Prevents information loss at boundaries
- Balances context size with retrieval precision

## Retrieval and Generation Pipeline

### Retrieval Strategy

#### Semantic Search

- **Method**: Cosine similarity between query and document embeddings
- **Top-k**: 5 most similar chunks
- **No re-ranking**: Direct similarity-based selection

#### Query Processing

```python
def retrieve_documents(self, query):
    query_embedding = self.embedder.encode([query])
    results = self.collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )
    return results
```

### Prompt Engineering

#### System Prompt Design

```python
system_prompt = """You are a helpful assistant that answers questions about company policies.

GUIDELINES:
1. Only answer questions about company policies
2. Base answers on provided context
3. Always include citations [Source: filename]
4. If no relevant info, say so clearly
5. Keep responses concise but comprehensive

Context: {context}
Question: {question}
"""
```

#### Key Elements

- **Role Definition**: Clear assistant role
- **Scope Limitation**: Policy-only responses
- **Citation Requirements**: Mandatory source attribution
- **Fallback Behavior**: Explicit handling of missing information
- **Response Style**: Professional and concise

## Evaluation and Monitoring

### Evaluation Metrics Implementation

#### Groundedness Scoring

```python
def evaluate_groundedness(self, response, query_data):
    # Check if expected topics appear in both answer and citations
    grounded_score = 0.0
    for topic in query_data['expected_topics']:
        if topic in answer and any(topic in citation for citation in citations):
            grounded_score += 1.0
    return grounded_score / len(expected_topics)
```

#### Citation Accuracy

```python
def evaluate_citation_accuracy(self, response, query_data):
    # Measure relevance of citations to query
    accurate_citations = 0
    for citation in citations:
        relevance_score = calculate_word_overlap(query, citation)
        if relevance_score > threshold:
            accurate_citations += 1
    return accurate_citations / len(citations)
```

### Performance Monitoring

#### Latency Tracking

- **Measurement**: End-to-end response time
- **Granularity**: Per-query timing
- **Aggregation**: P50, P95 percentiles

#### System Health

- **Database Connection**: Chroma availability
- **API Status**: OpenAI API connectivity
- **Model Loading**: Embedding model status

## Development and Deployment Tools

### Development Environment

#### Python Environment Management

- **Tool**: `venv` (Python virtual environments)
- **Requirements**: `requirements.txt` with pinned versions
- **Python Version**: 3.11+ for optimal performance

#### Code Quality Tools

- **Formatter**: `black` (PEP 8 compliance)
- **Linter**: `flake8` (code quality checks)
- **Security**: `bandit` (security vulnerability scanning)

### Web Framework

#### Flask Application

- **Framework**: Flask 3.0
- **Rationale**: Lightweight, simple API requirements
- **Extensions**: Minimal dependencies for security
- **Alternative**: FastAPI (considered for async capabilities)

#### Frontend Technology

- **Framework**: Vanilla JavaScript + Bootstrap 5
- **Rationale**: Simple requirements, no complex state management
- **Features**: Real-time chat interface, responsive design
- **Alternative**: React (rejected for complexity)

### CI/CD Pipeline

#### GitHub Actions Workflow

```yaml
- Python setup and dependency installation
- Code quality checks (black, flake8)
- Security scanning (bandit)
- Import and basic functionality tests
- Deployment to staging environment
```

#### Testing Strategy

- **Unit Tests**: Core functionality testing
- **Integration Tests**: End-to-end pipeline testing
- **Performance Tests**: Latency and throughput validation

## Cost Analysis

### Development Costs

- **Embedding Model**: Free (local deployment)
- **Vector Database**: Free (local Chroma)
- **LLM API**: Free (OpenRouter free tier)
- **Development Tools**: Free (open source)
- **Total Development Cost**: $0

### Production Costs (Estimated)

- **OpenRouter API**: Free (generous limits for moderate usage)
- **Hosting**: $0-20/month (Render/Railway free tier available)
- **Total**: $0-20/month for moderate usage

### Cost Optimization Strategies

1. **Caching**: Store responses for common queries to reduce API calls
2. **Batch Processing**: Group similar queries when possible
3. **Model Selection**: Use most efficient free model for the task
4. **Usage Monitoring**: Track API usage to stay within free limits
5. **Fallback Models**: Multiple free models for redundancy

## Future Enhancements

### Short-term Improvements

1. **Response Caching**: Redis for common queries
2. **Better Chunking**: Semantic chunking with sentence transformers
3. **Query Expansion**: Synonym and related term expansion
4. **A/B Testing**: Compare different models and parameters

### Long-term Roadmap

1. **Multi-modal Support**: Image and table processing
2. **Conversational Memory**: Multi-turn conversation support
3. **Advanced RAG**: Re-ranking, query decomposition
4. **Custom Fine-tuning**: Domain-specific model adaptation

## Security and Privacy Considerations

### Data Handling

- **Query Logging**: Minimal logging, no persistent storage
- **API Keys**: Environment variable management
- **Data Encryption**: HTTPS for all communications

### Model Security

- **Input Sanitization**: Prevent prompt injection
- **Output Filtering**: Content safety checks
- **Rate Limiting**: Prevent abuse and excessive usage

### Compliance

- **Data Residency**: Local processing where possible
- **Audit Trail**: System access and usage logging
- **Privacy**: No personal data in policy documents
