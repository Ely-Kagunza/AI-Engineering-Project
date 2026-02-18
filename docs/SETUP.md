# Setup Guide

## Prerequisites

- Python 3.11 or higher
- Virtual environment activated
- OpenRouter API key (free)

## Step 1: Get Free OpenRouter API Key

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Click "Sign In" or "Sign Up"
3. After signing in, go to "Keys" section
4. Click "Create Key"
5. Copy your API key

## Step 2: Configure Environment

1. Copy the example environment file:

   ```bash
   copy .env.example .env
   ```

2. Open `.env` file and add your OpenRouter API key:

   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

3. (Optional) Change the model if desired:
   ```
   OPENROUTER_MODEL=microsoft/phi-3-mini-128k-instruct:free
   ```

## Step 3: Ingest Documents

Run the ingestion pipeline to process the policy documents:

```bash
python src/ingest.py --corpus policies/
```

This will:

- Parse all documents in the `policies/` folder
- Create text chunks with overlap
- Generate embeddings
- Store everything in Chroma database

Expected output:

```
INFO:__main__:Processing: policies\employee-handbook.md
INFO:__main__:Created 15 chunks from policies\employee-handbook.md
...
INFO:__main__:Ingestion complete!
INFO:__main__:Processed files: 5
INFO:__main__:Total chunks: 75
```

## Step 4: Start the Application

```bash
python app.py
```

The application will start on http://localhost:5000

## Step 5: Test the System

Open your browser and go to:

```
http://localhost:5000
```

Try asking questions like:

- "How many vacation days do I get?"
- "What is the remote work policy?"
- "What are the expense reimbursement limits?"
- "What is the password policy?"

## Troubleshooting

### Issue: "OPENROUTER_API_KEY not found"

**Solution**: Make sure you created the `.env` file and added your API key

### Issue: "Failed to connect to Chroma collection"

**Solution**: Run the ingestion script first: `python src/ingest.py --corpus policies/`

### Issue: Slow first query

**Solution**: The first query downloads the embedding model (~23MB). Subsequent queries will be faster.

### Issue: API rate limits

**Solution**: OpenRouter free tier has generous limits. If you hit them, wait a few minutes or upgrade to paid tier.

## Running Evaluation

To evaluate the system performance:

```bash
python src/evaluate.py
```

This will:

- Run 25 test queries
- Measure groundedness, citation accuracy, and latency
- Generate visualizations in `evaluation_results/` folder

## Development Commands

### Format code:

```bash
black .
```

### Lint code:

```bash
flake8 .
```

### Run tests:

```bash
pytest
```

## Free Models Available

You can switch between these free models in your `.env` file:

1. **microsoft/phi-3-mini-128k-instruct:free** (Recommended)
   - 128k context window
   - Fast and efficient
   - Good for policy Q&A

2. **meta-llama/llama-3.1-8b-instruct:free**
   - Excellent reasoning
   - Good general performance

3. **google/gemma-2-9b-it:free**
   - Strong instruction following
   - Good for structured tasks

4. **qwen/qwen-2-7b-instruct:free**
   - Fast inference
   - Good multilingual support

## Next Steps

1. Add more policy documents to `policies/` folder
2. Re-run ingestion to update the database
3. Customize the system prompt in `src/rag.py`
4. Deploy to Render or Railway (see deployment guide)
5. Set up CI/CD with GitHub Actions
