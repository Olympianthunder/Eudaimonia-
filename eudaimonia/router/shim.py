from dataclasses import dataclass
from urllib.parse import urlparse

PAID_HOSTS = {"api.openai.com"}

@dataclass
class BudgetPolicy:
    daily_usd_cap: float = 3.00
    per_call_cap: float = 0.12
    warn_ratio: float = 0.80  # 80%

class BudgetGuardShim:
    """
    Decide-only guard. No network calls. For runtime integration later.
    """
    def __init__(self, policy: BudgetPolicy):
        self.policy = policy
        self.spent_today = 0.00  # updated from telemetry snapshots later

    def is_paid_host(self, base_url: str) -> bool:
        try:
            host = urlparse(base_url).hostname or ""
        except Exception:
            host = ""
        return any(h in host for h in PAID_HOSTS)

    def check(self, *, base_url: str, est_cost_usd: float) -> dict:
        if self.spent_today >= self.policy.daily_usd_cap:
            return {"ok": False, "action": "freeze", "reason": "daily_cap_reached"}
        if est_cost_usd > self.policy.per_call_cap:
            return {"ok": False, "action": "truncate", "reason": "per_call_over_cap"}
        result = {"ok": True, "action": "allow", "notes": []}
        ratio = (self.spent_today / self.policy.daily_usd_cap) if self.policy.daily_usd_cap else 0.0
        if ratio >= self.policy.warn_ratio:
            result["notes"].append("warn_80pct")
        if self.is_paid_host(base_url) and self.spent_today >= self.policy.daily_usd_cap:
            return {"ok": False, "action": "block_paid", "reason": "freeze_paid_hosts"}
        return result
