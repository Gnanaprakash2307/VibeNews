# text_to_speech.py

import pyttsx3

# ✅ Global engine (to prevent garbage collection issues)
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 2)

# Optional: Choose a voice (0 = male, 1 = female if available)
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-Speech error: {e}")
