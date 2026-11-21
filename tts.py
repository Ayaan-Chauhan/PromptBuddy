import pyttsx3

def speak(text: str):
    """Convert text to speech using pyttsx3"""
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)   # speaking speed
    engine.setProperty("volume", 1.0) # max volume
    engine.say(text)
    engine.runAndWait()
