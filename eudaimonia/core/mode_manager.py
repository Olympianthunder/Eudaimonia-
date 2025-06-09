class ModeManager:
    def __init__(self, modes, default_mode):
        self.modes = {mode.name: mode for mode in modes}
        self.default_mode = default_mode
        self.current_mode = None

    def evaluate_modes(self, context):
        for mode in self.modes.values():
            if mode.should_trigger(context):
                self.try_switch_to_mode(mode.name)
                break
        if self.current_mode is None:
            self.try_switch_to_mode(self.default_mode.name)

    def try_switch_to_mode(self, mode_name):
        if self.current_mode and self.current_mode.name == mode_name:
            return False
        if self.current_mode:
            self.current_mode.on_deactivate()
        self.current_mode = self.modes[mode_name]
        self.current_mode.on_activate({})
        return True

    def fallback_mode(self):
        self.try_switch_to_mode(self.default_mode.name)
