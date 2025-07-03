# Memory Store

Eudaimonia keeps a lightweight event log using [TinyDB](https://tinydb.readthedocs.io/).
Agents append events and modes can query them via `storage.py`.
The database persists to a JSON file so context is kept between sessions.
