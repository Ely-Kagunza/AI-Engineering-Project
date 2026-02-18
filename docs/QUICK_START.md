# Quick Start Guide

## 🚀 Start the Application (3 Steps)

### Step 1: Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Step 2: Start the Server

```bash
python app.py
```

### Step 3: Open Browser

```
http://localhost:5000
```

That's it! 🎉

## 💬 Try These Questions

Copy and paste into the chat:

```
How many vacation days do I get?
```

```
Can I work remotely?
```

```
What is the password policy?
```

```
What are the meal allowances for business trips?
```

## 📊 Run Evaluation

```bash
python src/evaluate.py
```

Results will be in `evaluation_results/` folder.

## 🔄 Add More Documents

1. Add `.md`, `.pdf`, `.docx`, or `.txt` files to `policies/` folder
2. Run ingestion:
   ```bash
   python src/ingest.py --corpus policies/
   ```
3. Restart the app

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal

## 🆘 Troubleshooting

### "OPENROUTER_API_KEY not found"

→ Check your `.env` file has the API key

### "Failed to connect to Chroma"

→ Run: `python src/ingest.py --corpus policies/`

### Slow first query

→ Normal! The model is loading. Next queries will be fast.

## 📚 Full Documentation

- **Setup**: See `SETUP.md`
- **Architecture**: See `design-and-evaluation.md`
- **AI Tools**: See `ai-tooling.md`
- **Status**: See `PROJECT_STATUS.md`

## 🎯 Project Requirements

✅ RAG system with company policies  
✅ 5 policy documents created  
✅ Web interface with citations  
✅ Evaluation framework  
✅ CI/CD pipeline  
✅ 100% free technology stack  
✅ Complete documentation

Ready for demo and submission!
