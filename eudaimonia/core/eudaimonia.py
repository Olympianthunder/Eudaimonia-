from eudaimonia.core.mode_manager import ModeManager
from eudaimonia.modes.default_mode import DefaultMode
from eudaimonia.modes.guardian_mode import GuardianMode
from eudaimonia.modes.tactical_mode import TacticalMode
from eudaimonia.modes.empathy_mode import EmpathyMode

class Eudaimonia:
    def __init__(self):
        self.default_mode = DefaultMode()
        self.modes = [
            self.default_mode,
            GuardianMode(),
            TacticalMode(),
            EmpathyMode()
        ]
        self.mode_manager = ModeManager(self.modes, self.default_mode)

    def process_request(self, request, context):
        try:
            self.mode_manager.evaluate_modes(context)
            return self.mode_manager.current_mode.process_request(request, context)
        except Exception as e:
            print("Error:", e)
            self.mode_manager.fallback_mode()
            return "[Fallback] Switching to default mode due to error."
