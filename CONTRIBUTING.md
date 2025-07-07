# Contributing to Eudaimonia MCP

Thank you for wanting to contribute! This project uses **pre-commit** to ensure
a consistent code style and to prevent accidental commits of secrets.

## Setup

1. Install the pre-commit tool:
   ```bash
   pip install pre-commit
   ```
2. Install the git hooks:
   ```bash
   pre-commit install
   ```
   The hooks will run automatically on each commit.

If a hook fails, fix the reported issues and re-run `git commit`.
