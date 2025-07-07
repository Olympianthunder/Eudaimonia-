from functools import lru_cache
import os
import json

import hvac


@lru_cache
def get_secret(key: str) -> str:
    """Retrieve ``key`` from HashiCorp Vault if available.

    Falls back to local ``local_settings.json`` or environment variables
    when Vault credentials are not provided.
    """
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    if vault_addr and vault_token:
        client = hvac.Client(url=vault_addr, token=vault_token)
        secret = client.secrets.kv.v2.read_secret_version(path=f"eudaimonia/{key}")
        return secret["data"]["data"][key]

    # Fallback to local settings file
    local_cfg = os.path.join(os.path.dirname(__file__), "local_settings.json")
    if os.path.exists(local_cfg):
        with open(local_cfg) as f:
            data = json.load(f)
            if key in data:
                return data[key]

    value = os.getenv(key.upper())
    if value is not None:
        return value
    raise KeyError(f"Secret '{key}' not found")
