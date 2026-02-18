# Quick Reference Card

## 🚀 Start Application

```bash
python app.py
```

Open: http://localhost:5000

## 🧪 Run Tests

```bash
python test_installation.py    # Verify setup
python test_full_system.py     # Test RAG system
python src/evaluate.py         # Run evaluation
```

## 📝 Sample Questions

```
How many vacation days do I get?
Can I work remotely?
What is the password policy?
What are the meal allowances?
What is the dress code?
```

## 🔗 Key Features

- ✅ Semantic search with citations
- ✅ **Clickable source links**
- ✅ Free LLM (OpenRouter)
- ✅ Real-time chat interface
- ✅ Performance metrics

## 📂 Important Files

- `.env` - API configuration
- `policies/` - Policy documents
- `src/rag.py` - RAG implementation
- `app.py` - Web application
- `requirements.txt` - Dependencies

## 🔧 Change LLM Model

Edit `.env`:

```
OPENROUTER_MODEL=upstage/solar-pro-3:free
```

## 📊 View Results

- Evaluation: `evaluation_results/`
- Charts: `evaluation_results/evaluation_charts.png`
- Report: `evaluation_results/evaluation_report.txt`

## 🆘 Troubleshooting

| Issue       | Solution                                      |
| ----------- | --------------------------------------------- |
| API Error   | Check `.env` API key                          |
| No Database | Run `python src/ingest.py --corpus policies/` |
| Slow Query  | Normal for first query (model loading)        |
| Port in Use | Change PORT in `.env`                         |

## 📚 Documentation

- `README.md` - Overview
- `SETUP.md` - Setup guide
- `FINAL_STATUS.md` - Complete status
- `FEATURES_SUMMARY.md` - All features

## 💡 Tips

- First query takes 5-10 seconds (model loading)
- Subsequent queries: 1-3 seconds
- Click source links to view full documents
- Check sidebar for system stats

## 🎯 Demo Points

1. Show chat interface
2. Ask sample questions
3. Click source links
4. Show citations
5. Display metrics
6. Explain free stack

## ✅ Status

- System: ✅ Working
- Tests: ✅ Passing
- Docs: ✅ Complete
- Links: ✅ Clickable
- Cost: ✅ $0

**Ready for demo!** 🎉
