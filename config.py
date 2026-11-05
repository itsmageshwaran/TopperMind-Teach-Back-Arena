"""Shared application settings."""
MODEL_NAME = "qwen/qwen3.8-27b"
# Cross-lingual embeddings support Hindi, Telugu, and Tamil queries against English notes.
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
COLLECTIONS = {
    "UPSC Polity": "upsc_polity",
    "College CS (DSA + DBMS)": "college_cs",
    "School Science (Class 10)": "school_science",
}

