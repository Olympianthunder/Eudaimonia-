# State Persistence

Eudaimonia Core uses DataJar for explicit state saves and restores. Shortcuts can call the API to capture or reload the current state JSON.

## Endpoints
- `GET /get_state_to_save` – return the current mode and other state fields.
- `POST /update_eudaimonia_state` – accept JSON to rehydrate Eudaimonia Core.

## Workflow
1. **Save** – Shortcut `Save Eudaimonia State` calls the GET endpoint and stores the JSON in DataJar.
2. **Load** – Shortcut `Load Eudaimonia State` retrieves the JSON from DataJar and POSTs to the update endpoint.
3. *(Optional)* Automations can run daily at set times to persist and restore state.

## Next Steps
- Merge these docs under feature/state-persistence.
- Build and test the Shortcuts end-to-end.
- Explore push-based triggers later.
