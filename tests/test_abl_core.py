import pytest
from eudaimonia.core.abl_core import ABLCore, DefenseMode

@pytest.mark.parametrize(
    "text,early,expected",
    [
        ("passive-aggressive DM", True, DefenseMode.INTERCEPT),
        ("verbal attack on phone", False, DefenseMode.DEFLECT),
        ("coercion via text", False, DefenseMode.ESCALATE),
        ("physical threat issued", False, DefenseMode.TERMINATE),
    ],
)
def test_mode_transitions(text, early, expected):
    abl = ABLCore()
    abl.run_protocol(text, early=early)
    assert abl.mode == expected

