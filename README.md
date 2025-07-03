# Eudaimonia-
Modular AI assistant with voice-aware behavior, dynamic mode switching, and Bahamian cultural tone. Built for real-world interaction, tactical decision-making, and emotional context.

## Requirements

The project relies solely on the Python standard library. Ensure Python 3.8 or newer is available. To run the test suite you will also need `pytest` installed:

```bash
pip install pytest
```

## Running the assistant

Use the module entry point located in `eudaimonia/main.py`:

```bash
python -m eudaimonia.main
```

This script initializes the assistant and processes several sample requests so you can confirm that everything is working.

## Running the tests

After the path fix, the test runner works without additional configuration. Execute:

```bash
pytest -q
```

At the moment no formal test cases are included so the command may report that zero tests were collected, but it should run successfully.
