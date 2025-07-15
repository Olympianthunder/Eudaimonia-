import numpy as np
from eudaimonia.core.memory_store import MemoryStore


def test_round_trip_json_yaml_npy(tmp_path):
    store = MemoryStore(tmp_path)
    store.put('j', {'a': 1})
    assert store.get('j') == {'a': 1}

    store.put('y', {'b': 2}, fmt='yaml')
    assert store.get('y', fmt='yaml') == {'b': 2}

    arr = np.array([1, 2, 3])
    store.put('n', arr, fmt='npy')
    loaded = store.get('n', fmt='npy')
    assert np.array_equal(loaded, arr)


def test_backup_created(tmp_path):
    store = MemoryStore(tmp_path)
    store.put('x', {'v': 1})
    store.put('x', {'v': 2})
    assert (tmp_path / 'x.json').exists()
    assert (tmp_path / 'x.json.bak').exists()
