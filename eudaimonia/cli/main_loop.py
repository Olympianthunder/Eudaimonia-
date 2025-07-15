"""Interactive shell entrypoint with YAML config."""

from __future__ import annotations

import argparse
import yaml

from ..core.memory_store import MemoryStore
from ..core.dialogue_loop import DialogueLoop


def load_config(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Eudaimonia interactive loop")
    parser.add_argument('--config', default='config.yaml', help='Path to YAML config')
    parser.add_argument('--model', help='Override model from config')
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.model:
        cfg['model'] = args.model

    store = MemoryStore(cfg.get('memory_path', 'memory'), encrypt=cfg.get('encrypt', False))
    loop = DialogueLoop(store, model=cfg.get('model', 'gpt-4o-mini'))

    loop.start_session()
    try:
        while True:
            try:
                msg = input('> ')
            except EOFError:
                break
            if msg.strip().lower() in {'exit', 'quit'}:
                break
            loop.record_exchange('user', msg)
            response = f"echo: {msg}"
            print(response)
            loop.record_exchange('assistant', response)
    finally:
        sid = loop.close_session()
        print(f"Session saved as {sid}")


if __name__ == '__main__':
    main()
