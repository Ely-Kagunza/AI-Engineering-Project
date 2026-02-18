# Design and Evaluation Document

## System Architecture

### Overview

This RAG (Retrieval-Augmented Generation) system is designed to answer questions about company policies and procedures using semantic search and AI-powered response generation.

### Architecture Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   Flask API     │    │   RAG Engine    │
│   (HTML/JS)     │◄──►│   (app.py)      │◄──►│   (rag.py)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐             │
                       │   Ingestion     │             │
                       │   Pipeline      │             │
                       │   (ingest.py)   │             │
                       └─────────────────┘             │
                                │                      │
                                ▼                      ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Document      │    │   Vector DB     │
                       │   Processing    │    │   (Chroma)      │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Embeddings    │
                                               │   (Sentence     │
                                               │   Transformers) │
                                               └─────────────────┘
```

### Data Flow

1. **Document Ingestion**:
   - Parse documents (MD, PDF, DOCX, TXT, HTML)
   - Clean and normalize text content
   - Split into overlapping chunks (1000 chars, 200 overlap)
   - Generate embeddings using sentence-transformers
   - Store in Chroma vector database

2. **Query Processing**:
   - User submits question via web interface
   - Question is embedded using same model
   - Semantic search retrieves top-k relevant chunks
   - Retrieved context is injected into LLM prompt
   - LLM generates response with citations
   - Response returned with metadata

3. **Response Generation**:
   - System prompt enforces policy-only responses
   - Retrieved chunks provide context
   - Citations extracted from source documents
   - Guardrails prevent off-topic responses

## Design Decisions

### Document Chunking Strategy

- **Chunk Size**: 1000 characters
  - Rationale: Balance between context preservation and retrieval precision
  - Large enough to maintain semantic coherence
  - Small enough for focused retrieval

- **Overlap**: 200 characters
  - Prevents information loss at chunk boundaries
  - Ensures important concepts aren't split

- **Chunking Method**: Sentence-aware splitting
  - Preserves sentence integrity
  - More natural language boundaries than fixed-size chunks

### Embedding Model Selection

- **Model**: `all-MiniLM-L6-v2`
  - Rationale: Good balance of performance and speed
  - 384-dimensional embeddings (efficient storage)
  - Strong performance on semantic similarity tasks
  - Fast inference for real-time queries

### Vector Database Choice

- **Database**: Chroma
  - Rationale: Lightweight, local deployment
  - No external dependencies for development
  - Good Python integration
  - Persistent storage with simple setup

### LLM Integration

- **Primary**: OpenRouter (Free Models)
  - Models: Microsoft Phi-3 Mini, Meta Llama 3.1 8B, Google Gemma 2 9B
  - Rationale: Free access to high-quality open-source models
  - No API costs for development and production
  - Multiple model options for comparison and fallback
  - Good instruction following and reasoning capabilities

- **Alternative Options**:
  - Hugging Face Inference API (free tier)
  - Local deployment with Ollama
  - Other free API providers

### Retrieval Strategy

- **Top-k**: 5 documents
  - Rationale: Provides sufficient context without overwhelming LLM
  - Balances relevance with response time
  - Allows for diverse source coverage

- **No Re-ranking**: Simplified pipeline
  - Reduces complexity and latency
  - Embedding similarity sufficient for policy documents
  - Can be added as future enhancement

## Evaluation Framework

### Metrics Definition

#### 1. Groundedness

- **Definition**: Percentage of answers fully supported by retrieved evidence
- **Measurement**: Keyword overlap between answer and citations
- **Target**: >70% groundedness score
- **Calculation**:
  ```
  groundedness = (supported_topics / total_expected_topics)
  ```

#### 2. Citation Accuracy

- **Definition**: Percentage of citations that correctly support the answer
- **Measurement**: Relevance of cited passages to query
- **Target**: >80% citation accuracy
- **Calculation**:
  ```
  citation_accuracy = (relevant_citations / total_citations)
  ```

#### 3. Latency

- **Definition**: Response time from query to answer
- **Measurements**:
  - P50 (median response time)
  - P95 (95th percentile response time)
- **Targets**:
  - P50 < 1500ms
  - P95 < 3000ms

### Test Query Design

#### Query Categories

1. **PTO Policies** (8 queries)
   - Vacation accrual, sick leave, holidays
   - Tests policy-specific numerical information

2. **Remote Work** (4 queries)
   - Eligibility, requirements, equipment
   - Tests procedural information

3. **Expense Policies** (5 queries)
   - Reimbursement limits, procedures
   - Tests financial policy details

4. **Security Policies** (5 queries)
   - Password requirements, incident reporting
   - Tests compliance information

5. **Employee Handbook** (3 queries)
   - General policies, conduct, probation
   - Tests broad policy coverage

#### Query Characteristics

- **Specificity**: Mix of specific and general questions
- **Complexity**: Single-topic focus for clear evaluation
- **Coverage**: All major policy areas represented
- **Difficulty**: Range from simple lookups to complex procedures

### Evaluation Process

1. **Automated Testing**:
   - Run all 25 test queries
   - Measure response times
   - Calculate groundedness and citation scores
   - Generate statistical summaries

2. **Manual Review**:
   - Spot-check answer quality
   - Verify citation relevance
   - Assess response appropriateness

3. **Performance Analysis**:
   - Category-wise performance breakdown
   - Latency distribution analysis
   - Correlation between metrics

4. **Reporting**:
   - Detailed CSV results
   - Summary statistics (JSON)
   - Visualization charts
   - Recommendations for improvement

## Quality Assurance

### Guardrails Implementation

1. **Topic Restriction**:
   - System prompt enforces policy-only responses
   - Rejection of non-policy questions
   - Clear messaging for out-of-scope queries

2. **Citation Requirements**:
   - All answers must include source references
   - Format: [Source: filename]
   - Snippet extraction for verification

3. **Response Length Control**:
   - Maximum token limits prevent excessive responses
   - Concise but comprehensive answers
   - Focus on directly answering the question

### Error Handling

1. **Graceful Degradation**:
   - Fallback responses for system errors
   - User-friendly error messages
   - Logging for debugging

2. **Input Validation**:
   - Question preprocessing and cleaning
   - Empty query handling
   - Rate limiting considerations

3. **System Monitoring**:
   - Health check endpoints
   - Performance metrics tracking
   - Error rate monitoring

## Scalability Considerations

### Current Limitations

- Single-threaded processing
- Local vector database
- No caching layer
- Limited concurrent users

### Future Enhancements

1. **Performance Optimization**:
   - Response caching for common queries
   - Batch processing for multiple queries
   - Async processing pipeline

2. **Scalability Improvements**:
   - Distributed vector database
   - Load balancing for multiple instances
   - CDN for static assets

3. **Feature Additions**:
   - Query suggestion/autocomplete
   - Conversation history
   - Advanced filtering options
   - Multi-language support

## Security and Privacy

### Data Protection

- No persistent storage of user queries
- Secure API key management
- HTTPS enforcement in production

### Access Control

- No authentication required (internal tool)
- Rate limiting to prevent abuse
- Input sanitization

### Compliance

- Company policy documents only
- No external data sources
- Audit trail for system access

## Deployment Strategy

### Development Environment

- Local development with sample data
- Environment variables for configuration
- Docker containerization option

### Production Deployment

- Cloud platform deployment (Render/Railway)
- Environment-specific configurations
- Automated deployment via GitHub Actions
- Health monitoring and alerting

### Monitoring and Maintenance

- Application performance monitoring
- Error tracking and alerting
- Regular evaluation runs
- Document corpus updates
