from .memory_store import MemoryStore

class DialogueLoop:
    """
    Manages the sliding window of recent memory entries and drives LLM dialogue.
    """

    def __init__(self, store: MemoryStore, *, ctx_window: int = 16) -> None:
        """
        :param store: your MemoryStore instance
        :param ctx_window: how many recent entries to keep
        """
        self.store = store
        self.ctx_window = ctx_window

    def get_context(self) -> list[dict]:
        """
        Retrieve the latest `ctx_window` memory events as context for the LLM.
        """
        return self.store.get_recent_events(limit=self.ctx_window)

    def add_user_message(self, message: str) -> None:
        """
        Log a new user message to memory.
        """
        self.store.add_event({"role": "user", "content": message})

    def add_assistant_message(self, message: str) -> None:
        """
        Log a new assistant message to memory.
        """
        self.store.add_event({"role": "assistant", "content": message})

    def run(self, user_input: str) -> str:
        """
        Full loop: add user message, build context, call LLM, log assistant reply.
        """
        self.add_user_message(user_input)
        context = self.get_context()
        assistant_reply = self._call_llm(context)
        self.add_assistant_message(assistant_reply)
        return assistant_reply

    def _call_llm(self, context: list[dict]) -> str:
        """
        Placeholder for your LLM invocation logic.
        """
        # e.g. openai.ChatCompletion.create(...)
        return "LLM response based on context"

