from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import os

from translate import run_translation, LANG_CODE_MAP
from sttmic import transcribe_audio_whisper
from tts import speak
from typing import Optional
from fastapi import UploadFile, File, Form

app = FastAPI()

@app.post("/translate")
async def translate_text(
    text: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None),
    src_lang: str = Form(...),
    tgt_lang: str = Form(...)
):
    try:
        # Map language names to codes
        src_code = LANG_CODE_MAP.get(src_lang.lower())
        tgt_code = LANG_CODE_MAP.get(tgt_lang.lower())

        if not src_code or not tgt_code:
            return JSONResponse({"error": "Unsupported language"}, status_code=400)

        # If no text but audio is given → transcribe first
        if not text and audio:
            file_path = f"temp_{audio.filename}"
            with open(file_path, "wb") as f:
                f.write(await audio.read())
            text = transcribe_audio_whisper(file_path)
            os.remove(file_path)

        if not text:
            return JSONResponse({"error": "No input text or audio"}, status_code=400)

        # Translate
        translated = run_translation(text, src_code, tgt_code)

        # Try text-to-speech
        try:
            speak(translated, tgt_lang)
        except Exception as e:
            print(f"[WARNING] TTS failed: {e}")

        return {"translated": translated}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
