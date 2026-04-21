"""
DocMind - RAG Document Intelligence
Streamlit Frontend - Professional warm UI
Run: streamlit run app.py
"""

import streamlit as st
import requests
import json

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocMind – RAG Document Intelligence",
    page_icon="🟫",
    layout="wide",
    initial_sidebar_state="expanded",
)

API = "http://localhost:8000"

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #faf7f2;
    color: #1c1612;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ── App background ── */
.stApp {
    background-color: #faf7f2;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #f4ede3 !important;
    border-right: 1px solid #e8d5c0;
}
[data-testid="stSidebar"] * {
    color: #1c1612 !important;
}

/* ── Top header bar ── */
.docmind-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 32px;
    background: #faf7f2;
    border-bottom: 1px solid #e8d5c0;
    margin: -1rem -1rem 2rem -1rem;
}
.docmind-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}
.docmind-logo-icon {
    width: 38px; height: 38px;
    background: #c8701a;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.docmind-logo-text {
    font-family: 'Fraunces', serif;
    font-size: 22px;
    font-weight: 600;
    color: #1c1612;
}
.docmind-logo-sub {
    font-size: 12px;
    color: #8b6f4e;
    font-weight: 400;
    margin-top: -2px;
}
.docmind-badges {
    display: flex;
    gap: 10px;
    align-items: center;
}
.badge {
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    border: 1px solid #e8d5c0;
    background: #fff;
    color: #5c4a35;
}
.badge-green { background: #f0faf0; border-color: #b8ddb8; color: #2d6e2d; }
.badge-amber { background: #fdf6ec; border-color: #e8c98a; color: #7a5c1e; }

/* ── Sidebar section headers ── */
.sidebar-section {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b6f4e;
    margin: 20px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid #e0cfba;
}

/* ── Chat area ── */
.chat-title {
    font-family: 'Fraunces', serif;
    font-size: 26px;
    font-weight: 500;
    color: #1c1612;
    margin-bottom: 24px;
}

/* ── Message bubbles ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 12px 0;
}
.msg-user-bubble {
    background: #c8701a;
    color: #fff;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 70%;
    font-size: 14px;
    line-height: 1.5;
    font-weight: 400;
}
.msg-bot {
    display: flex;
    flex-direction: column;
    margin: 12px 0;
}
.msg-bot-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8b6f4e;
    margin-bottom: 6px;
}
.msg-bot-bubble {
    background: #fff;
    border: 1px solid #e8d5c0;
    color: #1c1612;
    padding: 14px 18px;
    border-radius: 4px 18px 18px 18px;
    max-width: 80%;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.msg-bot-meta {
    font-size: 11px;
    color: #a08060;
    margin-top: 6px;
    display: flex;
    gap: 8px;
    align-items: center;
}
.source-tag {
    background: #fdf0e0;
    border: 1px solid #e8c98a;
    color: #7a5c1e;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
}

/* ── Input area ── */
.stTextInput input, .stTextArea textarea {
    background: #fff !important;
    border: 1px solid #e0cfba !important;
    border-radius: 10px !important;
    color: #1c1612 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #c8701a !important;
    box-shadow: 0 0 0 2px rgba(200,112,26,0.15) !important;
}

/* ── Buttons ── */
.stButton button {
    background: #c8701a !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
    transition: background 0.2s !important;
    width: 100%;
}
.stButton button:hover {
    background: #a85d14 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #fff !important;
    border: 1.5px dashed #d4b896 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

/* ── Indexed sources list ── */
.source-item {
    background: #fff;
    border: 1px solid #e8d5c0;
    border-left: 3px solid #c8701a;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 6px 0;
    font-size: 13px;
    color: #3d2b1a;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Model badge top right ── */
.model-badge {
    background: #f4ede3;
    border: 1px solid #e0cfba;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: #5c4a35;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* ── Divider ── */
hr { border-color: #e8d5c0 !important; }

/* ── Scrollable chat ── */
.chat-container {
    max-height: 520px;
    overflow-y: auto;
    padding: 8px 4px;
}

/* ── Success/Error ── */
.stSuccess { background: #f0faf0 !important; border-color: #b8ddb8 !important; }
.stError { background: #fdf0f0 !important; }
</style>
""", unsafe_allow_html=True)


# ── API helpers ────────────────────────────────────────────────────────────────
def api_health():
    try:
        r = requests.get(f"{API}/health", timeout=2)
        return r.status_code == 200
    except:
        return False

def api_stats():
    try:
        r = requests.get(f"{API}/stats", timeout=2)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def api_ingest_text(source_name, content):
    try:
        r = requests.post(f"{API}/ingest/text",
                          json={"source_name": source_name, "content": content},
                          timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_ingest_pdf(file_bytes, filename):
    try:
        r = requests.post(f"{API}/ingest/pdf",
                          files={"file": (filename, file_bytes, "application/pdf")},
                          timeout=60)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_query(question, history):
    try:
        r = requests.post(f"{API}/query",
                          json={"query": question, "chat_history": history},
                          timeout=60)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_clear():
    try:
        r = requests.delete(f"{API}/clear", timeout=10)
        return r.status_code == 200
    except:
        return False


# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources" not in st.session_state:
    st.session_state.sources = []


# ── Header ────────────────────────────────────────────────────────────────────
online = api_health()
stats = api_stats()
chunks = stats.get("total_chunks", 0)
docs = stats.get("total_documents", 0)

st.markdown(f"""
<div class="docmind-header">
  <div class="docmind-logo">
    <div class="docmind-logo-icon">📄</div>
    <div>
      <div class="docmind-logo-text">DocMind</div>
      <div class="docmind-logo-sub">RAG Document Intelligence</div>
    </div>
  </div>
  <div class="docmind-badges">
    <span class="badge {'badge-green' if online else 'badge'}">
      {'● API Online' if online else '○ API Offline'}
    </span>
    <span class="badge badge-amber">{chunks} chunks indexed</span>
    <span class="badge badge-amber">{docs} document{'s' if docs != 1 else ''}</span>
    <span class="model-badge">🟣 llama-3.3-70b · Groq (Free)</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Layout: sidebar + main ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section">📄 Upload PDF</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    if uploaded:
        if st.button("Index PDF"):
            with st.spinner("Processing PDF..."):
                result = api_ingest_pdf(uploaded.read(), uploaded.name)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"✅ Indexed {result.get('chunks_added', '?')} chunks!")
                st.rerun()

    st.markdown('<div class="sidebar-section">✏️ Paste Text</div>', unsafe_allow_html=True)
    src_name = st.text_input("Source name", value="notes", label_visibility="collapsed",
                              placeholder="Source name...")
    content = st.text_area("Content", height=140, label_visibility="collapsed",
                            placeholder="Paste any text to index...")
    if st.button("Index Text"):
        if content.strip():
            with st.spinner("Indexing..."):
                result = api_ingest_text(src_name, content)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"✅ Indexed {result.get('chunks_added', '?')} chunks!")
                st.rerun()
        else:
            st.warning("Please paste some text first.")

    # Indexed sources
    st.markdown('<div class="sidebar-section">📚 Indexed Sources</div>', unsafe_allow_html=True)
    stats2 = api_stats()
    sources = stats2.get("sources", [])
    if sources:
        for s in sources:
            st.markdown(f'<div class="source-item">📎 {s}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#a08060;font-size:13px;font-style:italic;">No documents indexed yet</p>',
                    unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear All Documents & History"):
        if api_clear():
            st.session_state.messages = []
            st.success("Cleared!")
            st.rerun()


# ── Main chat area ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown('<div class="chat-title">Ask your documents anything</div>', unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
          <div class="msg-user-bubble">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        sources_html = ""
        for s in msg.get("sources", []):
            sources_html += f'<span class="source-tag">📎 {s}</span>'
        chunks_text = f"◎ {msg.get('chunks', 0)} chunks retrieved"
        st.markdown(f"""
        <div class="msg-bot">
          <div class="msg-bot-label">DOCMIND</div>
          <div class="msg-bot-bubble">{msg['content']}</div>
          <div class="msg-bot-meta">{chunks_text} {sources_html}</div>
        </div>
        """, unsafe_allow_html=True)

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; color: #a08060;">
      <div style="font-size:48px; margin-bottom:16px;">📄</div>
      <div style="font-family:'Fraunces',serif; font-size:20px; color:#5c4a35; margin-bottom:8px;">
        No conversation yet
      </div>
      <div style="font-size:14px;">Upload a PDF or paste text on the left, then ask a question below.</div>
    </div>
    """, unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown("---")
col_input, col_btn = st.columns([5, 1])
with col_input:
    question = st.text_input("", placeholder="Ask a question about your documents...",
                              label_visibility="collapsed", key="question_input")
with col_btn:
    send = st.button("➤ Send")

if send and question.strip():
    if not online:
        st.error("Backend is offline. Run: uvicorn backend.api:app --reload --port 8000")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
        ]
        with st.spinner("Thinking..."):
            result = api_query(question, history)

        if "error" in result:
            answer = f"⚠️ Error: {result['error']}"
            srcs, n_chunks = [], 0
        else:
            answer = result.get("answer", "No answer returned.")
            srcs = result.get("sources", [])
            n_chunks = result.get("chunks_retrieved", 0)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": srcs,
            "chunks": n_chunks,
        })
        st.rerun()