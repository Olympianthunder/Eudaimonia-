# Guardian Rules

Guardian mode activation is driven by rules in `config/guardian_rules.yml`.

Each rule can specify:

- `when_text_contains`: list of keywords triggering the rule when found in the user text.
- `time_between`: start and end times in 24h format, evaluated in the user's timezone.
- `context_requires`: context flags that must be truthy.

Edit the YAML and reload the application to apply changes.
