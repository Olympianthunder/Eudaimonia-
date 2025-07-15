from datetime import datetime
from typing import List, Dict

import numpy as np
import openai

from .memory_store import MemoryStore


class DialogueLoop:
    """
    Manages the sliding window of recent memory entries and drives LLM dialogue.
    """

    def __init__(
        self,
        store: MemoryStore,
        *,
        model: str = "text-embedding-ada-002",
        ctx_window: int = 16,
    ) -> None:
        """
        :param store: your MemoryStore instance
        :param model: embedding model name for session close
        :param ctx_window: how many recent memory events to pull for context
        """
        self.store = store
        self.model = model
        self.session: List[Dict[str, str]] = []
        self.ctx_window = ctx_window

    # ────────────────────────────────────────────────────────────
    # Memory-window helpers
    # ────────────────────────────────────────────────────────────
    def get_context(self) -> list[dict]:
        """Return the latest `ctx_window` memory events for the LLM."""
        return self.store.get_recent_events(limit=self.ctx_window)

    def add_user_message(self, message: str) -> None:
        """Log a new user message to memory."""
        self.store.add_event({"role": "user", "content": message})

    def add_assistant_message(self, message: str) -> None:
        """Log a new assistant message to memory."""
        self.store.add_event({"role": "assistant", "content": message})

    # ────────────────────────────────────────────────────────────
    # Session-logging helpers (needed by tests)
    # ────────────────────────────────────────────────────────────
    def start_session(self) -> None:
        """Begin a fresh in-memory session log."""
        self.session = []

    def record_exchange(self, speaker: str, text: str) -> None:
        """Append one turn (user or assistant) to the session log."""
        self.session.append({"speaker": speaker, "text": text})

    def close_session(self) -> str:
        """
        Persist the session JSON and its embedding; return the session-ID.
        (The tests monkey-patch `openai.Embedding.create`, so this is safe.)
        """
        session_id = datetime.utcnow().isoformat(timespec="seconds").replace(":", "-")

        # raw session JSON
        self.store.put(session_id, self.session, fmt="json")

        # embedding
        joined = " ".join(item["text"] for item in self.session)
        resp = openai.Embedding.create(input=joined, model=self.model)
        embedding = resp["data"][0]["embedding"]
        self.store.put(f"{session_id}_emb", np.array(embedding, dtype=float), fmt="npy")

        return session_id

    # ────────────────────────────────────────────────────────────
    # Full dialogue loop (optional for now)
    # ────────────────────────────────────────────────────────────
    def run(self, user_input: str) -> str:
        """Record user input, build context, call LLM, record assistant reply."""
        self.add_user_message(user_input)
        context = self.get_context()
        assistant_reply = self._call_llm(context)
        self.add_assistant_message(assistant_reply)
        return assistant_reply

    def _call_llm(self, context: list[dict]) -> str:
        """Placeholder for actual LLM invocation."""
        # e.g. openai.ChatCompletion.create(...)
        return "LLM response based on context"

