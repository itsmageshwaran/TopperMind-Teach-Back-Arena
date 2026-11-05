"""Safe retrieval and optional web search tools."""
import logging
log = logging.getLogger(__name__)

def retrieve(collection, query, n=4):
    try:
        result = collection.query(query_texts=[query], n_results=min(n, max(1, collection.count())))
        docs = (result or {}).get("documents") or [[]]
        return docs[0] if docs else []
    except Exception:
        log.exception("Retrieval failed")
        return []

def add_note(collection, text, note_id):
    try:
        collection.add(ids=[note_id], documents=[text], metadatas=[{"topic": "user_note"}])
        return True, "Your note is added and available in Ask now. Keep learning!"
    except Exception as exc:
        log.exception("Adding note failed")
        return False, f"Couldn't add that note: {exc}. Please try again."

def web_search(query):
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            rows = list(ddgs.text(query, max_results=3))
        if not rows:
            return "Search unavailable"
        return "\n".join(f"- {r.get('title','')} — {r.get('body','')} ({r.get('href','')})" for r in rows)
    except Exception:
        log.exception("Web search failed")
        return "Search unavailable"

