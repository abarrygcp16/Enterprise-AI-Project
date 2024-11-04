# app/utils/test_tts.py
from tts import speak_text

def test_speak_text():
    try:
        speak_text("This is a test of the text-to-speech function.")
        success = True
    except Exception as e:
        print(e)
        success = False
    assert success, "Text-to-speech function failed."
