class ModeManager:
    def __init__(self, modes, default_mode):
        self.modes = {mode.name: mode for mode in modes}
        self.default_mode = default_mode
        self.current_mode = None

    def evaluate_modes(self, context):
        """Evaluate which mode should be active based on the given context."""
        triggered = False
        for mode in self.modes.values():
            if mode.should_trigger(context):
                self.try_switch_to_mode(mode.name)
                triggered = True
                break

        if not triggered:
            self.try_switch_to_mode(self.default_mode.name)

    def try_switch_to_mode(self, mode_name):
        if self.current_mode and self.current_mode.name == mode_name:
            return False
        if self.current_mode:
            self.current_mode.on_deactivate()
        self.current_mode = self.modes[mode_name]
        self.current_mode.on_activate({})
        return True

    def switch_mode(self, mode_name):
        """Public helper to switch modes programmatically."""
        return self.try_switch_to_mode(mode_name)

    def fallback_mode(self):
        self.try_switch_to_mode(self.default_mode.name)
