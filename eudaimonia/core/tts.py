"""Simple cross-platform text-to-speech helper."""

import platform
import subprocess


def speak(text: str) -> None:
    """Speak the provided ``text`` using basic platform utilities.

    On macOS the builtin ``say`` command is used. On Linux ``espeak`` will be
    attempted. On Windows PowerShell's speech synthesis is invoked. If none of
    these options succeed the text is printed instead.
    """
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["say", text], check=True)
        elif system == "Linux":
            subprocess.run(["espeak", text], check=True)
        elif system == "Windows":
            command = (
                "Add-Type -AssemblyName System.Speech;"
                "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{}')"
            ).format(text.replace("'", "''"))
            subprocess.run(["powershell", "-Command", command], check=True)
        else:
            print(text)
    except Exception:
        # Fallback to simply printing if tts fails
        print(text)
