import pytest

from eudaimonia.core.base_mode import BaseMode
from eudaimonia.core.mode_manager import ModeManager


class DefaultMode(BaseMode):
    name = "default"

    def __init__(self):
        self.activated = 0
        self.deactivated = 0

    def on_activate(self, context):
        self.activated += 1

    def on_deactivate(self):
        self.deactivated += 1


class DummyMode(BaseMode):
    name = "dummy"

    def __init__(self):
        self.activated = 0
        self.deactivated = 0

    def should_trigger(self, context):
        return context.get("dummy", False)

    def on_activate(self, context):
        self.activated += 1

    def on_deactivate(self):
        self.deactivated += 1


def test_switch_back_to_default_on_deactivate():
    default = DefaultMode()
    dummy = DummyMode()
    manager = ModeManager([default, dummy], default)

    # First evaluation should activate default mode
    manager.evaluate_modes({})
    assert manager.current_mode is default
    assert default.activated == 1
    assert default.deactivated == 0

    # Trigger dummy mode
    manager.evaluate_modes({"dummy": True})
    assert manager.current_mode is dummy
    assert default.deactivated == 1
    assert dummy.activated == 1

    # No trigger -> should switch back to default
    manager.evaluate_modes({})
    assert manager.current_mode is default
    assert dummy.deactivated == 1
    assert default.activated == 2

