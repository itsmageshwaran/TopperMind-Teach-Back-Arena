"""Agent roles, safe Groq calls, and deterministic scoring."""
import os, time, logging, re
import numpy as np
from groq import Groq
from config import MODEL_NAME
from knowledge import FOLLOWUPS
from tools import retrieve
log = logging.getLogger(__name__)

def llm(prompt, system="You are a kind, precise study coach."):
    try:
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            return "GROQ_API_KEY is missing. Add it as an environment variable or Space secret, then restart."
        for attempt in range(2):
            try:
                client = Groq(api_key=key)
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
                    temperature=0.3,
                )
                return response.choices[0].message.content.strip()
            except Exception as exc:
                if attempt == 0 and ("rate_limit" in str(exc).lower() or "429" in str(exc)):
                    time.sleep(3); continue
                log.exception("LLM call failed")
                return "I couldn't reach the study coach just now. Please try again in a moment."
    except Exception:
        log.exception("LLM setup failed")
        return "The study coach is temporarily unavailable. Please try again."

def choose_topic(collection_name, requested, model):
    try:
        choices = list(model.get(collection_name, {}))
        exact = next((x for x in choices if x.casefold() == requested.strip().casefold()), None)
        return exact or next((x for x in choices if requested.strip().casefold() in x.casefold() or x.casefold() in requested.strip().casefold()), None)
    except Exception:
        return None

def followup(topic, notes, language):
    try:
        context = "\n".join(notes)
        result = llm(f"Write exactly one short, friendly tricky follow-up question for a confused 10-year-old about {topic}. Ground it in these notes: {context}. {language}", "You are 🧒 Curious Student. Ask one question only.")
        if result.startswith(("GROQ_API_KEY is missing", "I couldn't reach", "The study coach is temporarily")):
            return FOLLOWUPS.get(topic, "Can you give me a small example?")
        return result
    except Exception:
        return FOLLOWUPS.get(topic, "Can you give me a small example?")

def score_explanation(explanation, answer, embedder):
    """Cosine similarity maps to 0–100 via clip((cosine - .15)/.65, 0, 1); this lets a solid paraphrase reach 80+ while avoiding high scores for generic overlap."""
    try:
        model = getattr(embedder, "model", embedder)
        vecs = np.asarray(model.encode([explanation, answer], normalize_embeddings=True), dtype=float)
        cosine = float(np.dot(vecs[0], vecs[1]))
        score = int(round(float(np.clip((cosine - .15) / .65, 0, 1)) * 100))
        words = re.findall(r"[A-Za-z0-9]+", answer.lower())
        stop = {"the","and","for","with","from","that","this","are","is","in","of","to","a","an","it","by","on","as","or","be"}
        terms = list(dict.fromkeys(w for w in words if len(w) >= 4 and w not in stop))
        missed = [w for w in terms if w not in explanation.lower()][:8]
        explained = [w for w in terms if w in explanation.lower()][:8]
        return score, explained, missed
    except Exception:
        log.exception("Scoring failed")
        return 0, [], []

def examiner(topic, score, explained, missed, language):
    facts = f"Score {score}/100. Explained well: {', '.join(explained) or 'core idea needs more detail'}. Missed key terms: {', '.join(missed) or 'none'}."
    return llm(f"In 2-3 short lines, encourage the student and give one specific improvement based only on these facts. {facts} {language}", "You are 📝 Examiner. Be kind, concise, and factual.")

def answer_from_notes(query, collection, language):
    try:
        docs = retrieve(collection, query, n=4)
        if not docs:
            return "I don't have that info in my notes."
        notes_text = "\n".join(docs)
        prompt = f"Answer using ONLY the notes below. If they do not contain the answer, reply exactly: I don't have that info in my notes. Notes:\n{notes_text}\nQuestion: {query}\n{language}. End with a short motivational one-liner."
        return llm(prompt, "You are a grounded tutor. Do not use outside knowledge.")
    except Exception:
        log.exception("Ask flow failed")
        return "I couldn't search the notes just now. Please try again. Keep going!"

