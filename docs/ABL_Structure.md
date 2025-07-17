```text
eudaimonia/
└── core/
    ├── abl_core.py       # main engine (FSM, enums, memory)
    ├── abl_config.json   # threat→mode map + keywords + form labels
    └── __init__.py
tests/
└── test_abl_core.py      # unit tests (21 ✓)
docs/
├── ABL_Master_Directive.md
└── ABL_Struct.md
```

```mermaid
sequenceDiagram
    participant User
    participant Guardian
    participant ABL
    participant Tactical

    User->>Guardian: message / event text
    Guardian->>ABL: run_protocol(text, early?)
    ABL-->>Guardian: status (mode, state)
    Guardian-->>Tactical: (optional) bus event
    loop every N sec
        Tactical->>ABL: get_status()
        ABL-->>Tactical: {mode}
        alt mode = ESCALATE or TERMINATE
            Tactical-->>Tactical: trigger_defense_sop()
        end
    end
```
