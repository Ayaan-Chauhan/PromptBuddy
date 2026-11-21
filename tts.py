import pyttsx3

def speak(text: str):
    """Convert text to speech using pyttsx3"""
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)   
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
