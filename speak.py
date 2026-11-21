from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# Mapping for gTTS language codes and their TLD (for accent/pronunciation)
LANG_TLD_MAP = {
    'hindi': ('hi', 'co.in'),
    'english': ('en', 'com'),
    'tamil': ('ta', 'co.in'),
    'telugu': ('te', 'co.in'),
    'marathi': ('mr', 'co.in'),
    'bengali': ('bn', 'co.in'),
    'gujarati': ('gu', 'co.in'),
    'kannada': ('kn', 'co.in'),
    'malayalam': ('ml', 'co.in'),
    'punjabi': ('pa', 'co.in'),
    'urdu': ('ur', 'co.in'),
}

def speak(text, lang_input):
    lang_input = lang_input.strip().lower()
    lang_code, tld = LANG_TLD_MAP.get(lang_input, ('en', 'com'))

    try:
        tts = gTTS(text=text, lang=lang_code, tld=tld, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio = AudioSegment.from_file(fp.name, format="mp3")
            play(audio)
    except Exception as e:
        print(f"[!] Text-to-Speech failed: {e}")
        