import speech_recognition as sr

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            return query
        except sr.WaitTimeoutError:
            return "Timeout"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Speech Recognition Error"