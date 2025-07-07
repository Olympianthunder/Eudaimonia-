from functools import lru_cache
import hvac
import os


@lru_cache
def get_secret(key: str) -> str:
    vault_addr = os.environ["VAULT_ADDR"]
    vault_token = os.environ["VAULT_TOKEN"]
    client = hvac.Client(url=vault_addr, token=vault_token)
    data = client.secrets.kv.v2.read_secret_version(path=f"eudaimonia/{key}")["data"][
        "data"
    ]
    if key not in data:
        raise RuntimeError(f"Missing secret: {key}")
    return data[key]
