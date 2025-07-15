import pytest

from eudaimonia.core.memory_store import MemoryStore


def test_encryption_round_trip(tmp_path):
    store = MemoryStore(tmp_path, encrypt=True)
    store.put('secret', {'value': 42})
    path = tmp_path / 'secret.json'
    # plaintext should not be visible
    assert b'42' not in path.read_bytes()
    assert store.get('secret')['value'] == 42


def test_wrong_key_fails(tmp_path):
    store = MemoryStore(tmp_path, encrypt=True)
    store.put('a', {'v': 1})
    # new store with different key can't decrypt
    other = MemoryStore(tmp_path, encrypt=True)
    with pytest.raises(ValueError):
        other.get('a')
