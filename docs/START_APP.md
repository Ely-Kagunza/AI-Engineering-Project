# Starting the Application

## Quick Start

Run the Flask application:

```bash
python app.py
```

The application will start on **http://localhost:5000**

## What You'll See

```
INFO:__main__:Loading embedding model: all-MiniLM-L6-v2
INFO:__main__:Connected to existing Chroma collection
INFO:__main__:Starting Flask app on port 5000
INFO:__main__:Debug mode: False
INFO:__main__:RAG system ready for queries
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
```

## Access the Application

Open your web browser and go to:

```
http://localhost:5000
```

## Try These Questions

1. **PTO Questions:**
   - "How many vacation days do I get?"
   - "What is the sick leave policy?"
   - "What holidays does the company observe?"

2. **Remote Work Questions:**
   - "Can I work remotely?"
   - "What equipment does the company provide for remote work?"
   - "What are the core collaboration hours?"

3. **Expense Questions:**
   - "What are the meal allowances for business trips?"
   - "How do I submit an expense report?"
   - "What expenses are not reimbursable?"

4. **Security Questions:**
   - "What is the password policy?"
   - "How should I handle confidential information?"
   - "What should I do if I lose my company laptop?"

5. **General Questions:**
   - "What is the probationary period?"
   - "What is the dress code?"
   - "What is the company's mission?"

## Features to Explore

- **Citations**: Each answer includes sources from policy documents
- **Snippets**: See the exact text that supports the answer
- **Response Time**: Check the latency for each query
- **System Stats**: View document count and model information in the sidebar

## Stopping the Application

Press `Ctrl+C` in the terminal to stop the Flask server.

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, you can change it in the `.env` file:

```
PORT=8000
```

### Slow First Query

The first query may take 5-10 seconds as the embedding model loads. Subsequent queries will be much faster (1-3 seconds).

### API Errors

If you see OpenRouter API errors:

1. Check your API key in `.env` file
2. Verify you have internet connection
3. Check OpenRouter status at https://status.openrouter.ai

## Next Steps

1. **Run Evaluation**: `python src/evaluate.py`
2. **Add More Documents**: Place new policy files in `policies/` folder
3. **Re-ingest**: Run `python src/ingest.py --corpus policies/` again
4. **Deploy**: Follow deployment guide for Render or Railway
