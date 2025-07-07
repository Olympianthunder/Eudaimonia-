# Eudaimonia MCP

[![CI](https://github.com/OWNER/Eudaimonia-/actions/workflows/tests.yml/badge.svg)](https://github.com/OWNER/Eudaimonia-/actions/workflows/tests.yml)
[![Docs](https://github.com/OWNER/Eudaimonia-/actions/workflows/docs.yml/badge.svg)](https://OWNER.github.io/Eudaimonia-/)
[![TestPyPI](https://github.com/OWNER/Eudaimonia-/actions/workflows/release.yml/badge.svg)](https://test.pypi.org/project/eudaimonia-mcp/)

Eudaimonia MCP is a modular AI assistant with voice-aware behavior and dynamic mode switching, inspired by Bahamian culture.

## Installation

```bash
pip install eudaimonia-mcp
```

## Usage

```bash
python -m eudaimonia.main
```

For full documentation visit the project site.

## Features

- [Guardian Rules](docs/guardian_rules.md) - customize when Guardian mode activates.
- Memory store - TinyDB-based event log for agents and modes.
- API bridge - interact with the assistant over HTTP.

## Task Automation

New endpoints provide automated task suggestions and execution:

```python
from backend.api import app
```

POST `/tasks/suggest` with `{"goal": "report"}` returns matching tasks.
POST `/tasks/execute` executes an approved task.

## Security

Secrets are pulled from Vault using `get_secret()` and never stored in code.
Pre-commit hooks can be enabled with:

```bash
pip install pre-commit
pre-commit install
```
