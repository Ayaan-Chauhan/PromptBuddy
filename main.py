from fastapi import FastAPI
import sttmic  
import translate
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Translation API is running!"}


@app.post("/transcribe/")
def transcribe_audio():
    """Record audio and transcribe with Whisper"""
    audio_file = sttmic.record_audio()
    text = sttmic.transcribe_audio_whisper(audio_file)
    return {
        "audio_file": audio_file,
        "transcription": text
    }


@app.post("/translate/")
def translate_text(text: str, src_lang: str, tgt_lang: str):
    """
    Translate text using IndicTrans2.
    Example: {"text": "Hello", "src_lang": "eng_Latn", "tgt_lang": "hin_Deva"}
    """
    translated = translate.run_translation(text, src_lang, tgt_lang)
    return {
        "input": text,
        "from": src_lang,
        "to": tgt_lang,
        "translation": translated
    }
