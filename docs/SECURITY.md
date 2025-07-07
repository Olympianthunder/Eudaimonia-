# Security

## Vault-backed Secrets

Secrets are loaded at runtime via HashiCorp Vault. Use `backend/config/secure_loader.py` and call `get_secret('KEY')` to access stored secrets. This removes the need for plaintext environment variables.

## CI Security Scans

The CI workflow runs dependency vulnerability checks for Python and Node packages and executes Bandit to scan the backend codebase:

```
pip-audit --fail-on high
npm audit --audit-level=moderate
bandit -r backend/ -ll
```

## Pre-commit Hooks

Pre-commit hooks prevent accidental inclusion of secrets or malformed files. Install them once per clone:

```bash
pip install pre-commit
pre-commit install
```
