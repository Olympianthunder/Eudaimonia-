from eudaimonia.modes.guardian_mode import GuardianMode


def test_guardian_mode_trigger():
    mode = GuardianMode()
    assert mode.should_trigger({"is_family_context": True}) is True
