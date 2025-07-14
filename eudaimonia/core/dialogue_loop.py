from __future__ import annotations

from datetime import datetime
from typing import List, Dict

import numpy as np
import openai

from .memory_store import MemoryStore


class DialogueLoop:
    """Simple controller for a text dialogue session."""

    def __init__(self, store: MemoryStore, *, model: str = "text-embedding-ada-002"):
        self.store = store
        self.model = model
        self.session: List[Dict[str, str]] = []

    def start_session(self) -> None:
        self.session = []

    def record_exchange(self, speaker: str, text: str) -> None:
        self.session.append({"speaker": speaker, "text": text})

    def close_session(self) -> str:
        session_id = datetime.utcnow().isoformat(timespec="seconds").replace(":", "-")
        self.store.put(session_id, self.session, fmt="json")
        joined = " ".join(item["text"] for item in self.session)
        resp = openai.Embedding.create(input=joined, model=self.model)
        embedding = resp["data"][0]["embedding"]
        self.store.put(f"{session_id}_emb", np.array(embedding, dtype=float), fmt="npy")
        return session_id
