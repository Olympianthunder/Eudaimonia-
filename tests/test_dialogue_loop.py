import numpy as np
import openai

from eudaimonia.core.memory_store import MemoryStore
from eudaimonia.core.dialogue_loop import DialogueLoop


def test_close_session_stores_embedding(monkeypatch, tmp_path):
    store = MemoryStore(tmp_path)
    called = {}

    def fake_create(input, model):
        called['input'] = input
        return {'data': [{'embedding': [0.1, 0.2, 0.3]}]}

    monkeypatch.setattr(openai.Embedding, 'create', fake_create)

    loop = DialogueLoop(store, model='fake-model')
    loop.start_session()
    loop.record_exchange('user', 'hi')
    loop.record_exchange('assistant', 'hello')
    sid = loop.close_session()

    assert store.get(sid)[0]['text'] == 'hi'
    emb = store.get(f'{sid}_emb', fmt='npy')
    assert np.allclose(emb, [0.1, 0.2, 0.3])
    assert called['input'] == 'hi hello'
