import os
import yaml
from datetime import datetime, time
from zoneinfo import ZoneInfo

DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "config", "guardian_rules.yml"
)

_rules_cache = None


def load_rules(path: str = DEFAULT_PATH) -> list:
    """Load rule definitions from YAML file."""
    global _rules_cache
    if _rules_cache is None:
        with open(path, "r") as f:
            _rules_cache = yaml.safe_load(f) or []
    return _rules_cache


def _in_time_range(now: datetime, start: str, end: str) -> bool:
    start_t = time.fromisoformat(start)
    end_t = time.fromisoformat(end)
    now_t = now.timetz().replace(tzinfo=None)
    if start_t <= end_t:
        return start_t <= now_t <= end_t
    return now_t >= start_t or now_t <= end_t


def should_trigger_guardian(text: str, context: dict) -> bool:
    """Evaluate loaded rules to decide whether guardian should trigger."""
    text_lower = text.lower()
    rules = load_rules()
    tz = context.get("timezone")
    if tz:
        tzinfo = ZoneInfo(tz)
    else:
        tzinfo = datetime.now().astimezone().tzinfo
    now = datetime.now(tzinfo)

    for rule in rules:
        if rule.get("action") != "trigger_guardian":
            continue
        if "when_text_contains" in rule:
            keywords = rule["when_text_contains"]
            if not any(word.lower() in text_lower for word in keywords):
                continue
        if "time_between" in rule:
            start, end = rule["time_between"]
            if not _in_time_range(now, start, end):
                continue
        if "context_requires" in rule:
            if not all(context.get(flag) for flag in rule["context_requires"]):
                continue
        return True
    return False
