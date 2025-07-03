# API Bridge

Eudaimonia exposes a lightweight HTTP interface using FastAPI. This makes it easy to integrate the assistant with other services.

## Endpoints

### `POST /speak`
Send JSON `{ "text": "hello" }` to invoke the text‑to‑speech helper.

### `POST /mode`
Provide `{ "mode": "mode_name" }` to switch the active mode programmatically.

### `GET /log`
Query parameters `type` and optional `limit` return recent events from the memory store.
