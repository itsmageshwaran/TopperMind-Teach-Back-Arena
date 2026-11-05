---
title: TopperMind: Teach-Back Arena
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.23.1
app_file: app.py
pinned: false
---

# TopperMind: Teach-Back Arena

**Don't just ask AI. Teach it.** TopperMind makes focused exam preparation available through a teach-back practice loop for school, college, UPSC and UGC NET learners.

## Problem and solution

Good coaching can be unaffordable or unavailable. TopperMind gives learners a lightweight practice coach: students explain a concept, a curious student asks a follow-up, an examiner gives reproducible feedback, and a strategist allocates study time to weak topics.

## Features

- Three seeded note collections: UPSC Polity, College CS (DSA + DBMS), and Class 10 Science.
- Three-round, Python-controlled teach-back flow with deterministic embedding similarity scores.
- Grounded question answering, optional DuckDuckGo current-affairs search, and user-added notes.
- Note-grounded MCQ generation, weighted study plan, and per-user progress view.
- English, Hindi, Telugu, and Tamil prompt language selection.

## Architecture

```text
Gradio UI + per-user gr.State
  ├─ Teach-Back state machine (Python, max 3 rounds)
  │    ├─ 🧒 Curious Student ── retrieve ──> ChromaDB notes
  │    ├─ 📝 Examiner <── cosine similarity + key-term check
  │    └─ 📅 Strategist <── weak scores
  ├─ Ask / Quiz ──> ChromaDB + Groq (grounded prompts)
  └─ Latest news ──> DuckDuckGo search tool (optional)
Embeddings: sentence-transformers/all-MiniLM-L6-v2
LLM: Groq API, model configured once in config.py
```

## Workshop concepts

| Feature | Workshop concept |
|---|---|
| Seeded notes and Ask | RAG: retrieve relevant notes before answering |
| Teach-Back score | Embeddings and cosine similarity, mapped to a stable 0–100 score |
| Curious Student, Examiner, Strategist | Agent roles expressed through system prompts and explicit Python orchestration |
| Latest news | Tool use through web search |
| Public app | Gradio deploy on Hugging Face Spaces |

## Run locally

Use Python 3.11 for this pinned dependency set. In particular, NumPy 1.26.4 does not provide a wheel for Python 3.15, so pip tries to compile it and requires a C compiler. On Windows, install Python 3.11, then create the virtual environment with the Python launcher (this can coexist with newer Python versions):

```bash
py -3.11 -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
# PowerShell: $env:GROQ_API_KEY="your-key"
# macOS/Linux: export GROQ_API_KEY="your-key"
python app.py
```

The app prints a startup self-test with key presence, model name, and the note count in each collection. The embedding model is downloaded on the first start. If the key is missing, the UI displays a clear setup message when an LLM feature is used.

## Deploy on Hugging Face Spaces

1. Create a Space and select **Gradio** as the SDK.
2. Upload these files from this folder, including `requirements.txt`.
3. In Space **Settings → Variables and secrets**, add `GROQ_API_KEY` as a secret.
4. Let the Space build. `app.py` launches on `0.0.0.0`; Spaces provides the public URL.

## Demo walkthrough

Start with the default **Stack** topic and click Start Teach-Back. Submit an explanation three times to show the follow-ups and final score. Then demonstrate Ask's honesty response, build a study plan after an attempt, switch to Hindi, and add a short note before querying it in Ask.

