# eudaimonia/core/dialogue_loop.py
from __future__ import annotations
"""
dialogue_loop.py — Dialogue controller (v0.2)
Persists every turn, generates embeddings on close_session().
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np  # type: ignore
import openai  # type: ignore

from .memory_store import MemoryStore

EMBED_MODEL = "text-embedding-3-small"


class DialogueLoop:
    def __init__(self, store: MemoryStore, *, ctx_window: int = 16) -> None:
        self.store = store
        self.ctx_window = ctx_window
        self.session_id: Optional[str] = None
        self.log: List[Dict[str, Any]] = []
        self.timestamp_start: Optional[str] = None

    # ───────── session ─────────
    def open_session(self, *, resume_last: bool = True) -> str:
        if resume_last:
            sessions = sorted(self.store.list("conversation"), 
reverse=True)
            if sessions:
                self.session_id = sessions[0]
                data = self.store.load("conversation", id=self.session_id, 
default={})
                self.log = data.get("messages", [])
                self.timestamp_start = data.get("timestamp_start")
                return self.session_id

        self.session_id = self.store.save(
            "conversation",
            {
                "schema_version": "0.1",
                "messages": [],
                "tags": [],
                "timestamp_start": self._now(),
                "timestamp_end": None,
            },
        )
        self.log = []
        self.timestamp_start = self._now()
        return self.session_id

    def close_session(self) -> None:
        if not self.session_id:
            return

        self.store.save(
            "conversation",
            {
                "schema_version": "0.1",
                "messages": self.log,
                "tags": [],
                "timestamp_start": self.timestamp_start,
                "timestamp_end": self._now(),
            },
            id=self.session_id,
        )

        try:
            flat = "\n".join(m["content"] for m in self.log)
            resp = openai.Embedding.create(model=EMBED_MODEL, 
input=[flat])
            vec = np.asarray(resp["data"][0]["embedding"], 
dtype="float32")
            self.store.save("embeddings", vec, id=self.session_id)
        except Exception as exc:
            print(f"[Embedding skipped: {exc}]")

    # ───────── record ─────────
    def record_user(self, txt: str) -> None:
        self._append("user", txt)

    def record_assistant(self, txt: str) -> None:
        self._append("assistant", txt)

    def _append(self, role: str, txt: str) -> None:
        self.log.append({"role": role, "content": txt, "timestamp": 
self._now()})
        if self.session_id:
            self.store.save(
                "conversation",
                {
                    "schema_version": "0.1",
                    "messages": self.log,
                    "tags": [],
                    "timestamp_start": self.timestamp_start,
                    "timestamp_end": None,
                },
                id=self.session_id,
            )

    def get_context_window(self) -> List[Dict[str, str]]:
        return self.log[-self.ctx_window :]

    @staticmethod
    def _now() -> str:
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

