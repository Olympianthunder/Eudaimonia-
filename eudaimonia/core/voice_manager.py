import json
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "config", "voice_profiles.json"
)

with open(CONFIG_PATH, "r") as f:
    voice_profiles = json.load(f)


def get_voice_profile(mode_name):
    if mode_name in voice_profiles:
        profile = voice_profiles[mode_name]
        base = voice_profiles.get(profile.get("inherits_from", "default"), {})
        return {**base, **profile}
    return voice_profiles.get("default", {})
