from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="Phishing URL Detection API")

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request schema ────────────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    url: str
    strategy: str = "tree"  # tree | model | prompt_llama | prompt_gpt | prompt_qwen | hybrid

# ── Strategy metadata ─────────────────────────────────────────────────────────
STRATEGY_META = {
    "model":        {"name": "Model-Based Ensemble",                    "acc": 86.00, "prec": 93.10, "rec": 77.80, "f1": 84.70},
    "prompt_llama": {"name": "Prompt-Based Ensemble (LLaMA 3.3 70B)",   "acc": 86.70, "prec": 94.90, "rec": 77.60, "f1": 85.40},
    "prompt_gpt":   {"name": "Prompt-Based Ensemble (GPT-OSS 120B)",    "acc": 81.60, "prec": 96.70, "rec": 65.40, "f1": 78.00},
    "prompt_qwen":  {"name": "Prompt-Based Ensemble (Qwen 3.6-27B)",    "acc": 73.50, "prec": 99.20, "rec": 47.40, "f1": 64.10},
    "hybrid":       {"name": "Hybrid-Based Ensemble",                   "acc": 74.50, "prec": 99.20, "rec": 49.40, "f1": 65.90},
    "tree":         {"name": "Tree-Based Ensemble",                     "acc": 98.90, "prec": 99.20, "rec": 98.60, "f1": 98.90},
}

# ── Dummy prediction ──────────────────────────────────────────────────────────
def dummy_predict(url: str, strategy: str):
    """
    Dummy prediction based on URL hash.
    Replace this with real model inference later.
    """
    # Simple heuristic for demo: flag obviously suspicious patterns
    suspicious_keywords = ["login", "verify", "secure", "account", "update", "bank", "paypal", "signin"]
    url_lower = url.lower()

    is_phishing = any(kw in url_lower for kw in suspicious_keywords)

    # Add some randomness for demo
    if not is_phishing:
        is_phishing = random.random() < 0.3

    confidence = round(random.uniform(0.75, 0.99), 4) if is_phishing else round(random.uniform(0.80, 0.99), 4)
    meta = STRATEGY_META.get(strategy, STRATEGY_META["tree"])

    explanation = None
    if strategy != "tree":
        explanation = (
            f"The URL '{url}' exhibits suspicious lexical patterns including keyword overlap "
            f"with known phishing domains. Confidence score: {confidence:.2%}."
            if is_phishing else
            f"The URL '{url}' appears structurally consistent with legitimate domains. "
            f"No phishing indicators detected. Confidence score: {confidence:.2%}."
        )

    return {
        "url": url,
        "label": "phishing" if is_phishing else "legitimate",
        "confidence": confidence,
        "strategy": meta["name"],
        "explanation": explanation,
        "metrics": {
            "accuracy": meta["acc"],
            "precision": meta["prec"],
            "recall": meta["rec"],
            "f1_score": meta["f1"],
        }
    }

# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Phishing URL Detection API is running."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    result = dummy_predict(req.url, req.strategy)
    return result
