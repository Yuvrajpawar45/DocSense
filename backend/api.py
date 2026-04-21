"""
FastAPI Backend — RAG Q&A API
Run: uvicorn backend.api:app --reload --port 8000
"""

import shutil,tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_engine import RAGEngine

app = FastAPI(title="RAG Q&A API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGEngine()


class TextIngestRequest(BaseModel):
    text: str
    source: str = "manual_input"

class QueryRequest(BaseModel):
    query: str
    chat_history: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stats")
def stats():
    return rag.get_stats()

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    chunks_added = rag.ingest_pdf(tmp_path)
    Path(tmp_path).unlink()
    return {"message": f"✅ Ingested '{file.filename}' — {chunks_added} chunks", "chunks_added": chunks_added, "stats": rag.get_stats()}

@app.post("/ingest/text")
def ingest_text(req: TextIngestRequest):
    if len(req.text.strip()) < 50:
        raise HTTPException(400, "Text too short (minimum 50 characters)")
    chunks_added = rag.ingest_text(req.text, req.source)
    return {"message": f"✅ Ingested '{req.source}' — {chunks_added} chunks", "chunks_added": chunks_added, "stats": rag.get_stats()}

@app.post("/query")
def query(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(400, "Query cannot be empty")
    return rag.answer(req.query, req.chat_history)

@app.delete("/clear")
def clear_index():
    rag.clear_index()
    return {"message": "Index cleared"}
