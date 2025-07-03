import os
import platform


def speak(text: str) -> None:
    """Simple cross-platform text-to-speech helper."""
    system = platform.system()
    if system == "Darwin":
        os.system(f'say "{text}"')
    elif system == "Windows":
        try:
            import win32com.client  # type: ignore
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        except Exception:
            print(text)
    else:
        try:
            import pyttsx3  # type: ignore
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            print(text)
