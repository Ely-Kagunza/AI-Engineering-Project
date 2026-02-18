# RAG — Company Policies & Procedures (Project Documentation)

## Short goal ✅
Build a Retrieval-Augmented Generation (RAG) app that answers user questions about a small, legally includable corpus of company policies and procedures, evaluate its information quality and latency, and provide documentation + demo for grading.

---

## 1) Scope & deliverables 📦
- Corpus: 5–20 short files (md/html/pdf/txt), 30–120 pages total.
- Code repo including: `README.md`, `design-and-evaluation.md`, `ai-tooling.md` (and optional `deployed.md`).
- Recorded demo (5–10 minutes). Repo must be shared with `quantic-grader`.

---

## 2) Core requirements (high level) 🔧
- Environment & reproducibility: virtualenv, `requirements.txt`, setup instructions, fixed seeds where applicable.
- Ingestion & indexing: parse → clean → chunk (window/heading + overlap) → embed → store (e.g., `Chroma`).
- Retrieval & RAG: Top-k retrieval (+ optional re-rank), inject retrieved chunks + citations into LLM prompt, guardrails (refuse outside-corpus Qs, limit length, always cite sources).
- Web app/API: `/` (chat UI), `POST /chat` (returns answer + citations + snippet + source links), `GET /health`.
- Evaluation: 15–30 test queries; report groundedness, citation accuracy, latency (p50/p95).
- CI/CD: GitHub Actions to install deps and run build/tests; optional deploy to Render/Railway on success.

---

## 3) Required evaluation metrics 📋
- Groundedness — % answers fully supported by retrieved evidence.
- Citation accuracy — % answers whose citations correctly point to supporting passages.
- Latency — p50 / p95 response times (sample of 10–20 queries).

---

## 4) Minimal implementation checklist (priority) ✅
1. Prepare legal corpus (5–20 files).
2. Ingest → chunk → embed → store (Chroma/local vector DB).
3. Implement retrieval + prompt template with citations and guardrails.
4. Build simple web UI + `/chat` and `/health` endpoints.
5. Create 15–30 evaluation queries; measure groundedness, citation accuracy, latency.
6. Add `README.md`, `design-and-evaluation.md`, `ai-tooling.md` to repo.
7. Add GitHub Actions workflow to run install + import/build check; optionally deploy.

---

## 5) Suggested free tooling & defaults 💡
- Embeddings: Cohere / HuggingFace / Open-source models (free tiers).
- LLM (inference): OpenRouter / other free-tier endpoints.
- Vector DB: `Chroma` (local) for reproducibility.
- Orchestration: LangChain (optional) for retrieval + prompt chaining.
- Web app: Flask or Streamlit.
- Host (optional): Render or Railway (free tiers).

---

## 6) Prompting & guardrails (implementation notes) 🔒
- Always prefix: “I can only answer questions about the company policies in my corpus.”
- Inject Top-k retrieved chunks with explicit `source_id` and snippet.
- Limit model output tokens and require a `Sources:` section that lists document IDs/titles with line/snippet references.

---

## 7) Repo structure (recommended) 📁

```
/ (repo root)
├─ app.py (or server/)
├─ requirements.txt
├─ README.md
├─ design-and-evaluation.md
├─ ai-tooling.md
├─ docs/PROJECT_OVERVIEW.md  <- this file
├─ policies/ (*.md, *.pdf, *.txt)
├─ src/ (ingest, index, rag logic)
└─ .github/workflows/ci.yml
```

---

## 8) Quick start (developer) ▶️
1. Create virtualenv and activate.
2. pip install -r requirements.txt
3. Add corpus files to `policies/`.
4. python src/ingest.py --corpus policies/   # parse, chunk, embed, save vectors
5. python app.py  # start web UI

---

## 9) Evaluation plan (brief) 🧪
- Create 15–30 representative Qs across topics (PTO, security, expenses, remote work, holidays).
- For each Q, record: answer text, supporting retrieved passages, annotated gold label (for exact/partial match optional).
- Calculate groundedness and citation accuracy percentages and measure p50/p95 latency.

---

## 10) Submission & demo checklist 🎯
- GitHub repo (share with `quantic-grader`) containing required docs.
- Recorded demo (5–10 minutes) showing: app usage, evaluation results, and CI/CD run.
- Optional: live deployed URL in `deployed.md`.

---

## Next steps (options) ➕
- Generate repo scaffold (ingest + Chroma + Flask UI + CI workflow).
- Create `design-and-evaluation.md` and `ai-tooling.md` now.

---

If you want the scaffold or additional docs created now, tell me which files to add next.