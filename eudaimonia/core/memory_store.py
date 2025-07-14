import io
import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import yaml
from cryptography.fernet import Fernet, InvalidToken


class MemoryStore:
    """Filesystem backed key-value store with optional Fernet encryption."""

    def __init__(self, path: str | Path, *, encrypt: bool = False, key: bytes | None = None):
        self.base_path = Path(path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.encrypt = encrypt
        self.fernet = None
        if encrypt:
            self.fernet = Fernet(key or Fernet.generate_key())

    def get_key(self) -> bytes | None:
        if self.fernet:
            return self.fernet._signing_key + self.fernet._encryption_key
        return None

    # util
    def _file(self, key: str, ext: str) -> Path:
        return self.base_path / f"{key}.{ext}"

    def _write(self, path: Path, data: bytes) -> None:
        if path.exists():
            backup = path.with_suffix(path.suffix + ".bak")
            path.replace(backup)
        if self.encrypt and self.fernet:
            data = self.fernet.encrypt(data)
        path.write_bytes(data)

    def _read(self, path: Path) -> bytes:
        data = path.read_bytes()
        if self.encrypt and self.fernet:
            try:
                data = self.fernet.decrypt(data)
            except InvalidToken as e:
                raise ValueError("Invalid encryption key") from e
        return data

    # public API
    def put(self, key: str, value: Any, *, fmt: str = "json") -> Path:
        path = self._file(key, "yaml" if fmt == "yaml" else ("npy" if fmt == "npy" else "json"))
        if fmt == "json":
            raw = json.dumps(value).encode()
        elif fmt == "yaml":
            raw = yaml.safe_dump(value).encode()
        elif fmt == "npy":
            buf = io.BytesIO()
            np.save(buf, value)
            raw = buf.getvalue()
        else:
            raise ValueError(f"unknown format {fmt}")
        self._write(path, raw)
        return path

    def get(self, key: str, *, fmt: str = "json", default: Any | None = None) -> Any:
        path = self._file(key, "yaml" if fmt == "yaml" else ("npy" if fmt == "npy" else "json"))
        if not path.exists():
            return default
        raw = self._read(path)
        if fmt == "json":
            return json.loads(raw.decode())
        elif fmt == "yaml":
            return yaml.safe_load(raw.decode())
        elif fmt == "npy":
            buf = io.BytesIO(raw)
            return np.load(buf, allow_pickle=True)
        else:
            raise ValueError(f"unknown format {fmt}")

    def keys(self) -> Iterable[str]:
        for p in self.base_path.glob('*'):
            if p.suffix == '.bak' or not p.is_file():
                continue
            yield p.stem

    def reset(self) -> None:
        for p in self.base_path.glob('*'):
            p.unlink()
