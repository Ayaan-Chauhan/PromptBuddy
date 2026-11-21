import gradio as gr
from translate import translate, LANG_CODE_MAP
from speak import speak
from sttmic import transcribe_audio_whisper as transcribe
import numpy as np
import soundfile as sf

# Supported Languages
LANGUAGES = list(LANG_CODE_MAP.keys())

# Normalize Audio (to fix silent recordings)
def normalize_audio(audio_path):
    try:
        data, samplerate = sf.read(audio_path)

        # Convert stereo to mono if needed
        if len(data.shape) == 2:
            data = data.mean(axis=1)

        # Normalize volume
        if np.max(np.abs(data)) > 0:
            data = data / np.max(np.abs(data))

        sf.write(audio_path, data, samplerate)
        print(f"[DEBUG] Normalized and converted audio: {audio_path}")
    except Exception as e:
        print(f"[WARNING] Could not normalize audio: {e}")
    return audio_path

# Main Handler
def process_input(text, audio, src_lang, tgt_lang):
    print(f"[INFO] text='{text}'  audio={audio}  src={src_lang}  tgt={tgt_lang}")

    if not text and not audio:
        return "Please provide text or audio.", None

    if not text and audio:
        try:
            # ✅ Extra Debug: Check if audio is valid
            if not audio or audio == "":
                print("[ERROR] No valid audio received from mic.")
                return "Audio not received properly.", None

            print(f"[INFO] Normalizing audio: {audio}")
            audio = normalize_audio(audio)

            print(f"[INFO] Transcribing from audio...")
            text = transcribe(audio)
            print(f"[INFO] Transcribed text: {text}")
        except Exception as e:
            return f"[ERROR] Audio Transcription Failed: {e}", None

    src_code = LANG_CODE_MAP.get(src_lang.lower())
    tgt_code = LANG_CODE_MAP.get(tgt_lang.lower())

    if not src_code or not tgt_code:
        return "[ERROR] Unsupported language selected.", None

    try:
        print(f"[INFO] Translating from {src_code} to {tgt_code}")
        translated = translate(text, src_code, tgt_code)
        print(f"[INFO] Translated: {translated}")
    except Exception as e:
        return f"[ERROR] Translation Failed: {e}", None

    try:
        speak(translated, tgt_lang)
    except Exception as e:
        print(f"[WARNING] TTS failed: {e}")

    return translated, translated

# Gradio UI
app = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Textbox(label="Enter text", placeholder="Type or leave blank to use mic..."),
        gr.Audio(type="filepath", label="Upload or record audio"),
        gr.Dropdown(choices=LANGUAGES, label="Source Language", value="english"),
        gr.Dropdown(choices=LANGUAGES, label="Target Language", value="hindi"),
    ],
    outputs=[
        gr.Textbox(label="Translated Text"),
        gr.Textbox(visible=False),
    ],
    title="PromptBuddy Translator",
    description="🎙️ Translate between English ↔ Indian languages using Whisper, IndicTrans, and TTS"
)

if __name__ == "__main__":
    print("[INFO] Starting PromptBuddy Translator...")
    app.launch()
