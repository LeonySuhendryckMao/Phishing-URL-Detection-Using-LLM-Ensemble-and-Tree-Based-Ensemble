import streamlit as st
import hashlib
import time
import random
import socket

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Phishing URL Detection",
    page_icon="🛡️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }

.hero { text-align: center; padding: 2.5rem 1rem 1.5rem; }
.hero-badge {
    display: inline-block;
    background: rgba(0, 212, 255, 0.15);
    color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 999px;
    font-size: 12px;
    font-weight: 500;
    padding: 4px 14px;
    margin-bottom: 16px;
    letter-spacing: 0.05em;
}
.hero h1 { font-size: 26px; font-weight: 700; color: #ffffff; line-height: 1.35; margin-bottom: 10px; }
.hero h1 span { color: #00d4ff; }
.hero p { font-size: 14px; color: rgba(255,255,255,0.55); max-width: 480px; margin: 0 auto; }

.card-title { font-size: 12px; font-weight: 600; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }

.stTextInput > div > div > input {
    background: #1a2235 !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    caret-color: #ffffff !important;
    font-family: 'Courier New', monospace !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.35) !important; }
.stTextInput > div > div > div { color: rgba(255,255,255,0.45) !important; }
.stTextInput [data-testid="InputInstructions"] { color: rgba(255,255,255,0.45) !important; }

.section-label { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.35); text-transform: uppercase; letter-spacing: 0.08em; margin: 16px 0 8px; }

.stRadio > div { display: flex; flex-direction: column; gap: 8px; }
.stRadio > div > label {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    cursor: pointer;
    transition: all 0.2s;
}
.stRadio > div > label:hover {
    background: rgba(0, 212, 255, 0.08) !important;
    border-color: rgba(0, 212, 255, 0.25) !important;
}
.stRadio > div > label p,
.stRadio > div > label span,
.stRadio > div > label div,
.stRadio label { color: #ffffff !important; font-size: 14px !important; }
.stRadio > div > label:hover p,
.stRadio > div > label:hover span { color: #00d4ff !important; }

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00d4ff, #0088cc) !important;
    color: #0a0f1e !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px !important;
    letter-spacing: 0.03em;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

.result-phishing { background: rgba(220, 38, 38, 0.12); border: 1px solid rgba(220, 38, 38, 0.35); border-radius: 14px; padding: 1.5rem; margin-top: 1rem; }
.result-legitimate { background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 14px; padding: 1.5rem; margin-top: 1rem; }
.result-dns { background: rgba(234, 179, 8, 0.12); border: 1px solid rgba(234, 179, 8, 0.35); border-radius: 14px; padding: 1.5rem; margin-top: 1rem; }
.result-title-phishing { font-size: 20px; font-weight: 700; color: #f87171; margin-bottom: 6px; }
.result-title-legit { font-size: 20px; font-weight: 700; color: #34d399; margin-bottom: 6px; }
.result-title-dns { font-size: 20px; font-weight: 700; color: #fbbf24; margin-bottom: 6px; }
.result-sub { font-size: 12px; color: rgba(255,255,255,0.45); margin-bottom: 16px; }

.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 12px; }
.metric-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 8px; text-align: center; }
.metric-val { font-size: 17px; font-weight: 700; color: #00d4ff; }
.metric-label { font-size: 10px; color: rgba(255,255,255,0.4); margin-top: 3px; text-transform: uppercase; letter-spacing: 0.05em; }

.explanation-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #00d4ff;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-top: 12px;
    font-size: 13px;
    color: rgba(255,255,255,0.65);
    line-height: 1.6;
}
.explanation-title { font-size: 11px; font-weight: 600; color: #00d4ff; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }

.footer { text-align: center; padding: 2rem 0 1rem; font-size: 12px; color: rgba(255,255,255,0.2); }

@media (max-width: 768px) {
    .hero h1 { font-size: 18px; }
    .hero p { font-size: 13px; }
    .hero { padding: 1.5rem 0.5rem 1rem; }
    .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    .metric-val { font-size: 15px; }
    .result-title-phishing, .result-title-legit, .result-title-dns { font-size: 16px; }
    .stRadio > div > label p, .stRadio > div > label span { font-size: 13px !important; }
    .footer { font-size: 11px; padding: 1.5rem 0.5rem 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Strategy metadata ─────────────────────────────────────────────────────────
STRATEGIES = {
    "🤖 Model-Based Ensemble": {
        "key": "model", "type": "llm",
        "desc": "LLaMA 3.3 70B · GPT-OSS 120B · Qwen 3.6-27B",
        "acc": 86.00, "prec": 93.10, "rec": 77.80, "f1": 84.70,
    },
    "💬 Prompt-Based Ensemble (LLaMA 3.3 70B)": {
        "key": "prompt_llama", "type": "llm",
        "desc": "zero-shot · one-shot · two-shot",
        "acc": 86.70, "prec": 94.90, "rec": 77.60, "f1": 85.40,
    },
    "💬 Prompt-Based Ensemble (GPT-OSS 120B)": {
        "key": "prompt_gpt", "type": "llm",
        "desc": "zero-shot · one-shot · two-shot",
        "acc": 81.60, "prec": 96.70, "rec": 65.40, "f1": 78.00,
    },
    "💬 Prompt-Based Ensemble (Qwen 3.6-27B)": {
        "key": "prompt_qwen", "type": "llm",
        "desc": "zero-shot · one-shot · two-shot",
        "acc": 73.50, "prec": 99.20, "rec": 47.40, "f1": 64.10,
    },
    "🔀 Hybrid-Based Ensemble": {
        "key": "hybrid", "type": "llm",
        "desc": "LLaMA · GPT-OSS · Qwen × zero/one/two-shot",
        "acc": 74.50, "prec": 99.20, "rec": 49.40, "f1": 65.90,
    },
    "🌲 Tree-Based Ensemble": {
        "key": "tree", "type": "ml",
        "desc": "Decision Tree · Random Forest · XGBoost",
        "acc": 98.90, "prec": 99.20, "rec": 98.60, "f1": 98.90,
    },
}

# ── DNS Check ─────────────────────────────────────────────────────────────────
def check_dns(url: str) -> bool:
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).hostname
        if not domain:
            return False
        socket.setdefaulttimeout(3)
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

# ── Dummy Prediction ──────────────────────────────────────────────────────────
def dummy_predict(url: str, strategy_key: str) -> dict:
    """
    Dummy prediction — replace with real model inference later.
    LLM: replace with Groq API call.
    Tree-Based: replace with joblib.load() model inference.
    """
    suspicious_keywords = ["login", "verify", "secure", "account", "update", "bank", "paypal", "signin", "confirm", "password"]
    url_lower = url.lower()
    is_phishing = any(kw in url_lower for kw in suspicious_keywords)
    if not is_phishing:
        hash_val = int(hashlib.md5(url.encode()).hexdigest(), 16)
        is_phishing = hash_val % 3 == 0

    confidence = round(random.uniform(0.78, 0.99), 4)

    explanation = None
    if strategy_key != "tree":
        explanation = (
            "The URL exhibits suspicious patterns including mismatched domain names, "
            "unusual subdomains, and high similarity index to known phishing sites. "
            "The ensemble flagged this URL based on structural and lexical features."
            if is_phishing else
            "The URL structure appears consistent with legitimate domains. "
            "No suspicious patterns such as IP-based URLs, excessive subdomains, "
            "or phishing-related keywords were detected."
        )

    return {
        "is_phishing": is_phishing,
        "confidence": confidence,
        "explanation": explanation,
    }

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ Research Demo · Binus University</div>
    <h1>Phishing URL Detection Using<br><span>LLM Ensemble</span> and Tree-Based Ensemble</h1>
    <p>Enter a URL and select a detection strategy to classify it as phishing or legitimate.</p>
</div>
""", unsafe_allow_html=True)

# ── URL Input ─────────────────────────────────────────────────────────────────
st.markdown('<div class="card-title">🔗 Target URL</div>', unsafe_allow_html=True)
url_input = st.text_input(
    label="url",
    placeholder="https://example.com",
    label_visibility="collapsed"
)

# ── Strategy Selection ────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Detection Strategy</div>', unsafe_allow_html=True)
strategy_name = st.radio(
    label="strategy",
    options=list(STRATEGIES.keys()),
    label_visibility="collapsed"
)
strategy = STRATEGIES[strategy_name]

# ── Predict Button ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict = st.button("🔍 Detect URL", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────────────
if predict:
    if not url_input.strip():
        st.error("Please enter a URL.")
    else:
        with st.spinner("Analyzing URL..."):
            time.sleep(1.0)

            # ── Step 1: DNS Check ─────────────────────────────────────────────
            domain_exists = check_dns(url_input.strip())

            if not domain_exists:
                st.markdown(f"""
                <div class="result-dns">
                    <div class="result-title-dns">⚠️ Domain Not Found</div>
                    <div class="result-sub">URL: {url_input}</div>
                    <div class="explanation-box">
                        <div class="explanation-title">⚠️ DNS Check Failed</div>
                        This domain could not be resolved. It may be a fake, misspelled, or malicious URL.
                        Proceed with extreme caution.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                # ── Step 2: Model Prediction ──────────────────────────────────
                result = dummy_predict(url_input.strip(), strategy["key"])
                is_phishing = result["is_phishing"]

                label = "🚨 Phishing URL Detected" if is_phishing else "✅ Legitimate URL"
                css_class = "result-phishing" if is_phishing else "result-legitimate"
                title_class = "result-title-phishing" if is_phishing else "result-title-legit"

                explanation_html = ""
                if result["explanation"]:
                    explanation_html = f"""
                    <div class="explanation-box">
                        <div class="explanation-title">💡 Natural Language Explanation</div>
                        {result['explanation']}
                    </div>
                    """

                st.markdown(f"""
                <div class="{css_class}">
                    <div class="{title_class}">{label}</div>
                    <div class="result-sub">Strategy: {strategy_name.split(' ', 1)[1]} · {strategy['desc']} · Confidence: {result['confidence']:.2%}</div>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-val">{strategy['acc']}%</div>
                            <div class="metric-label">Accuracy</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-val">{strategy['prec']}%</div>
                            <div class="metric-label">Precision</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-val">{strategy['rec']}%</div>
                            <div class="metric-label">Recall</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-val">{strategy['f1']}%</div>
                            <div class="metric-label">F1-Score</div>
                        </div>
                    </div>
                    {explanation_html}
                </div>
                """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Phishing URL Detection · Binus University · 2026<br>
    Leony Suhendryck Mao · Fernando Luis Gerrard · Samuel Aditya Jimmy Saputra · Ventje Jeremias Lewi Engel
</div>
""", unsafe_allow_html=True)
