"""
================================================
Project 1: Education Tutor for Remote India
Streamlit Web App
================================================
"""

import os
import pickle
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
from scaledown.compressor import ScaleDownCompressor
from scaledown.exceptions import AuthenticationError, APIError

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🎓 Python Tutor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

.hero {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p { color: #94a3b8; font-size: 1rem; margin: 0; }

.pipeline {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 1rem 0 1.5rem;
}
.badge {
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(167,139,250,0.35);
    color: #c4b5fd;
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
}
.badge.green { background: rgba(52,211,153,0.12); border-color: rgba(52,211,153,0.3); color: #6ee7b7; }
.badge.blue  { background: rgba(96,165,250,0.12); border-color: rgba(96,165,250,0.3); color: #93c5fd; }

.msg-user {
    background: rgba(167,139,250,0.12);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    color: #e2e8f0;
    max-width: 80%;
    margin-left: auto;
}
.msg-bot {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px 16px 16px 4px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    color: #e2e8f0;
    max-width: 92%;
}
.msg-label {
    font-size: 0.68rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.08em;
    margin-bottom: 0.35rem;
    opacity: 0.55;
    text-transform: uppercase;
}

.cost-card {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: #6ee7b7;
    font-family: 'Space Mono', monospace;
}

.stTextInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}
.stTextInput input:focus {
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.1) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.7rem 1rem;
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; }

hr { border-color: rgba(255,255,255,0.08) !important; }

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px dashed rgba(167,139,250,0.3) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
MODEL      = "gemini-2.5-flash"
CACHE_FILE = "textbook_cache.pkl"

# ─────────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────────

def extract_textbook(pdf_file) -> str:
    """Extract full text from uploaded PDF."""
    reader        = PdfReader(pdf_file)
    textbook_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            textbook_text += f"\n\n[Page {i+1}]\n{text.strip()}"
    return textbook_text


def scaledown_compress(textbook_text: str, question: str, sd_key: str) -> str:
    """STEP 2 — ScaleDown compress: full textbook → relevant paragraphs only."""
    compressor = ScaleDownCompressor(
        api_key=sd_key,
        target_model="gpt-4o",
        rate="auto"
    )
    result = compressor.compress(
        context=textbook_text,
        prompt=question
    )
    return str(result)


def generate_answer(compressed: str, question: str, model) -> str:
    """STEP 3 — Gemini answers from compressed content only."""
    prompt = (
        f"Textbook content:\n{compressed}"
        f"\n\nStudent's question: {question}"
    )
    response = model.generate_content(prompt)
    return response.text


def cost_info(tokens_sent: int) -> dict:
    full_tokens  = 85_000
    price_per_1m = 0.075
    usd_to_inr   = 84
    cost_full    = (full_tokens  / 1_000_000) * price_per_1m * usd_to_inr
    cost_smart   = (tokens_sent  / 1_000_000) * price_per_1m * usd_to_inr
    savings_pct  = round((1 - tokens_sent / full_tokens) * 100)
    return {
        "tokens":  tokens_sent,
        "full":    f"₹{cost_full:.2f}",
        "smart":   f"₹{cost_smart:.4f}",
        "savings": f"{savings_pct}%"
    }

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages"       not in st.session_state: st.session_state.messages       = []
if "textbook_text"  not in st.session_state: st.session_state.textbook_text  = None
if "q_count"        not in st.session_state: st.session_state.q_count        = 0
if "total_saved"    not in st.session_state: st.session_state.total_saved    = 0

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ API Keys")

    sd_key = st.text_input(
        "ScaleDown API Key",
        type="password",
        placeholder="bBVTq...",
        value=os.environ.get("SCALEDOWN_API_KEY", ""),
        help="Your ScaleDown API key"
    )

    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIzaSy...",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Get free key at aistudio.google.com"
    )

    st.markdown("---")
    st.markdown("### 📚 Textbook PDF")

    uploaded_file = st.file_uploader(
        "Upload textbook PDF",
        type=["pdf"],
        help="Upload your Python textbook PDF"
    )

    if uploaded_file and st.session_state.textbook_text is None:
        with st.spinner("📖 Extracting PDF text..."):
            text = extract_textbook(uploaded_file)
            st.session_state.textbook_text = text
        tokens = len(text.split())
        st.success(f"✅ Loaded ~{tokens:,} tokens from PDF!")

    if st.session_state.textbook_text:
        tokens = len(st.session_state.textbook_text.split())
        st.markdown(f"""
        <div style='background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.2);
        border-radius:10px;padding:0.6rem 1rem;margin-top:0.4rem;'>
        <div style='color:#6ee7b7;font-size:0.75rem;font-family:Space Mono,monospace;'>
        📄 ~{tokens:,} tokens loaded<br>
        ❓ {st.session_state.q_count} questions asked
        </div></div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    c1, c2 = st.columns(2)
    c1.metric("Questions", st.session_state.q_count)
    c2.metric("Tokens Saved", f"{st.session_state.total_saved:,}")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='color:#64748b;font-size:0.72rem;line-height:1.7;'>
    <b style='color:#94a3b8;'>Pipeline:</b><br>
    1️⃣ PDF → full text<br>
    2️⃣ ScaleDown compress<br>
    &nbsp;&nbsp;&nbsp;85,000 → ~3,400 tokens<br>
    3️⃣ Gemini answers<br><br>
    💰 Saves 96% on API costs!
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────

st.markdown("""
<div class='hero'>
    <h1>🎓 Python Tutor AI</h1>
    <p>Education Tutor for Remote India · Powered by ScaleDown + Gemini 2.5 Flash</p>
</div>
<div class='pipeline'>
    <span class='badge'>📄 PDF</span>
    <span class='badge blue'>→ ScaleDown Compress</span>
    <span class='badge'>85K → 3.4K tokens</span>
    <span class='badge green'>→ Gemini Answer</span>
</div>
""", unsafe_allow_html=True)

# ── Validation ──
if not sd_key or not gemini_key:
    st.info("👈 Enter your **ScaleDown** and **Gemini API keys** in the sidebar.")
    st.stop()

if st.session_state.textbook_text is None:
    st.info("👈 Upload your **textbook PDF** in the sidebar.")
    st.stop()

# ── Setup Gemini ──
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel(
    model_name=MODEL,
    system_instruction=(
        "You are a patient, encouraging tutor for Indian high school students. "
        "Explain concepts clearly using simple language and everyday examples. "
        "Answer ONLY from the provided textbook content. "
        "If the content doesn't cover the question, say so."
    )
)

# ── Chat history ──
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='msg-user'>
            <div class='msg-label'>🧑‍🎓 You</div>
            {msg['content']}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='msg-bot'>
            <div class='msg-label'>🤖 Tutor</div>
            {msg['content']}
        </div>""", unsafe_allow_html=True)
        if "cost" in msg:
            c = msg["cost"]
            st.markdown(f"""
            <div class='cost-card'>
            📌 ScaleDown: {c['tokens']:,} tokens sent &nbsp;|&nbsp;
            ❌ Before: {c['full']} &nbsp;|&nbsp;
            ✅ After: {c['smart']} &nbsp;|&nbsp;
            🎉 Saved: {c['savings']}
            </div>""", unsafe_allow_html=True)

# ── Input ──
st.markdown("<br>", unsafe_allow_html=True)
col_q, col_btn = st.columns([5, 1])
with col_q:
    question = st.text_input(
        "question",
        placeholder="e.g. What is a for loop? · Explain functions · What is a list?",
        label_visibility="collapsed",
        key="q_input"
    )
with col_btn:
    ask = st.button("Ask ➤", use_container_width=True)

# ── Suggested questions ──
suggestions = ["What is a for loop?", "Explain functions", "What is a list?", "How do dictionaries work?"]
s_cols = st.columns(4)
for i, s in enumerate(suggestions):
    if s_cols[i].button(s, key=f"s{i}", use_container_width=True):
        question = s
        ask = True

# ── Process ──
if ask and question.strip():
    st.session_state.messages.append({"role": "user", "content": question})

    try:
        # STEP 2: ScaleDown
        with st.spinner("📌 Step 2: ScaleDown compressing textbook..."):
            compressed = scaledown_compress(
                st.session_state.textbook_text,
                question,
                sd_key
            )

        if not compressed.strip():
            st.warning("⚠️ ScaleDown returned empty. Try rephrasing.")
        else:
            # STEP 3: Gemini
            with st.spinner("📌 Step 3: Gemini generating answer..."):
                answer = generate_answer(compressed, question, model)
                tokens_sent = len(compressed.split()) + len(question.split())
                c = cost_info(tokens_sent)

            st.session_state.q_count     += 1
            st.session_state.total_saved += (85_000 - tokens_sent)
            st.session_state.messages.append({
                "role":    "assistant",
                "content": answer,
                "cost":    c
            })

    except AuthenticationError:
        st.error("❌ ScaleDown API key invalid! Check your key in the sidebar.")
    except APIError as e:
        st.error(f"❌ ScaleDown API error: {e}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

    st.rerun()