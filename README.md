# 📖 DocMind — RAG Document Intelligence

A production-grade Retrieval-Augmented Generation (RAG) system. Upload PDFs or paste text, then ask questions and get answers with full source citations.

**Built with:** sentence-transformers · FAISS · Groq Llama 3 (FREE) · FastAPI · Vanilla HTML/CSS/JS

---

## 🏗 Architecture

```
User Question
     │
     ▼
[ index.html ]  ──HTTP──►  [ FastAPI /query ]
                                   │
               ┌───────────────────┼────────────────────┐
               ▼                   ▼                    ▼
     Embed query (MiniLM)   FAISS top-K search   Groq Llama 3 generate
               └───────────────────┴────────────────────┘
                                   │
                             Answer + Citations
```

| Component | Technology |
|---|---|
| Embeddings | `sentence-transformers` all-MiniLM-L6-v2 |
| Vector Store | `FAISS` — local, no cloud needed |
| LLM | Llama 3 8B via **Groq API (FREE)** |
| Backend | `FastAPI` + `uvicorn` |
| Frontend | Pure HTML / CSS / JavaScript |
| PDF Parsing | `PyMuPDF (fitz)` |

---

## 🚀 Setup (5 minutes)

### 1. Install Python dependencies
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 2. Get FREE Groq API key
1. Go to **https://console.groq.com**
2. Sign up (no credit card required)
3. Click **API Keys** → **Create API Key**
4. Copy your key (starts with `gsk_...`)

### 3. Create your `.env` file
```bash
# Copy the template
copy .env.example .env     # Windows
# cp .env.example .env     # Mac/Linux
```
Then open `.env` and paste your key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 4. Start the backend (Terminal 1)
```bash
uvicorn backend.api:app --reload --port 8000
```
✅ You should see: `Uvicorn running on http://127.0.0.1:8000`

### 5. Open the frontend
Just **double-click** `frontend/index.html` in File Explorer — opens in your browser.

Or navigate to it manually in Chrome: `Ctrl+O` → select `frontend/index.html`

---

## 💡 How to Use

| Step | Action |
|---|---|
| 1 | Upload a PDF via the sidebar (drag & drop works too) |
| 2 | OR paste any text → give it a name → click "Index Text" |
| 3 | Wait for "X chunks ✓" confirmation |
| 4 | Type your question in the chat box and press Enter |
| 5 | Get answers with source citations! |

---

## 📁 Project Structure

```
DocMind/
├── backend/
│   ├── __init__.py
│   ├── rag_engine.py       # Chunking, FAISS indexing, retrieval, Groq generation
│   └── api.py              # FastAPI REST endpoints
├── frontend/
│   └── index.html          # Complete UI (HTML + CSS + JS, single file)
├── data/                   # Auto-created on first ingest
│   ├── faiss.index         # Vector index (persists between runs)
│   └── metadata.pkl        # Chunk metadata
├── .env                    # Your API key (never commit this)
├── .env.example            # Template
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Configuration

In `backend/rag_engine.py` you can tune:
```python
EMBED_MODEL   = "all-MiniLM-L6-v2"  # swap for larger model for better quality
GROQ_MODEL    = "llama3-8b-8192"     # or "mixtral-8x7b-32768" for longer context
CHUNK_SIZE    = 500                  # characters per chunk (try 300–800)
CHUNK_OVERLAP = 100                  # overlap to avoid missing context at boundaries
TOP_K         = 5                    # how many chunks to retrieve per query
```

---

## 🎯 Interview Talking Points

1. **Chunking** — Sliding window with overlap prevents losing context at chunk boundaries
2. **Embedding** — MiniLM is fast and CPU-friendly; can swap for `text-embedding-3-small` in production
3. **FAISS choice** — Avoids cloud DB dependency; in production you'd use Pinecone or Weaviate
4. **Conversation memory** — Last 6 turns sent as context to Groq for coherent multi-turn dialogue
5. **Free LLM** — Groq gives 14,400 free requests/day; production would use a paid tier
6. **Production path** — Add auth, containerize with Docker, replace FAISS with cloud vector DB

---

## 🔄 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/stats` | Index stats (chunk count, sources) |
| POST | `/ingest/pdf` | Upload & index a PDF |
| POST | `/ingest/text` | Index raw text |
| POST | `/query` | Ask a question |
| DELETE | `/clear` | Clear entire index |

Interactive API docs: **http://localhost:8000/docs**
