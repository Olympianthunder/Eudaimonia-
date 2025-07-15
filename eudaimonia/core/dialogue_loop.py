--- a/eudaimonia/core/dialogue_loop.py
+++ b/eudaimonia/core/dialogue_loop.py
@@ -1,7 +1,7 @@
-from __future__ import annotations
-from datetime import datetime
-from typing import List, Dict
-import numpy as np
-import openai
+from datetime import datetime
+from typing import List, Dict
+import numpy as np
+import openai

 from .memory_store import MemoryStore

@@ -9,15 +9,41 @@
 class DialogueLoop:
-    """Simple controller for a text dialogue session."""
-    def __init__(self, store: MemoryStore, *, model: str = "text-embedding-ada-002"):
-    """
-    Manages the sliding window of recent memory entries and drives LLM dialogue.
-    """
-    def __init__(self, store: MemoryStore, *, ctx_window: int = 16) -> None:
-        """
-        :param store: your MemoryStore instance
-        :param ctx_window: how many recent entries to keep
-        """
-        self.store = store
-        self.model = model
-        self.session: List[Dict[str, str]] = []
+    """
+    Controller for dialogue sessions, combining memory, embedding storage,
+    and a sliding context window.
+    """
+    def __init__(
+        self,
+        store: MemoryStore,
+        *,
+        model: str = "text-embedding-ada-002",
+        ctx_window: int = 16,
+    ) -> None:
+        """
+        :param store: your MemoryStore instance
+        :param model: embedding model name for session close
+        :param ctx_window: how many recent memory events to pull for context
+        """
+        self.store = store
+        self.model = model
+        self.session: List[Dict[str, str]] = []
+        self.ctx_window = ctx_window
+
+    def start_session(self) -> None:
+        """Begin a fresh in-memory session log."""
+        self.session = []
+
+    def record_exchange(self, speaker: str, text: str) -> None:
+        """Append one turn (user or assistant) to the session log."""
+        self.session.append({"speaker": speaker, "text": text})
+
+    def close_session(self) -> str:
+        """
+        Persist the session and its embedding.
+        Returns the session ID.
+        """
+        session_id = datetime.utcnow().isoformat(timespec="seconds").replace(":", "-")
+        # store raw session JSON
+        self.store.put(session_id, self.session, fmt="json")
+        # build one string, get embedding, store as numpy array
+        joined = " ".join(item["text"] for item in self.session)
+        resp = openai.Embedding.create(input=joined, model=self.model)
+        embedding = resp["data"][0]["embedding"]
+        self.store.put(f"{session_id}_emb", np.array(embedding, dtype=float), fmt="npy")
+        return session_id

     def get_context(self) -> list[dict]:
         """
@@ -46,7 +72,7 @@ class DialogueLoop:
         """
         return self.store.get_recent_events(limit=self.ctx_window)

-    def add_user_message(self, message: str) -> None:
+    def add_user_message(self, message: str) -> None:
         """
         Log a new user message to memory.
         """
@@ -54,6 +80,7 @@ class DialogueLoop:
         self.store.add_event({"role": "assistant", "content": message})

     def run(self, user_input: str) -> str:
+        """Full loop: record user, fetch context, call LLM, record assistant."""
         self.add_user_message(user_input)
         context = self.get_context()
         assistant_reply = self._call_llm(context)

