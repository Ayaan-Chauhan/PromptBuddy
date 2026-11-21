import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import tempfile
import numpy as np
import os

SAMPLE_RATE = 16000  # Whisper expects 16kHz
DURATION = 5         # seconds

# Load Whisper once (global)
print("[INFO] Loading Whisper model...")
_model = whisper.load_model("base")


def record_audio(filename="recorded.wav", duration=DURATION, sample_rate=SAMPLE_RATE):
    """Record audio from microphone and save as WAV."""
    print("🎙️ Recording... Speak now.")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(filename, sample_rate, recording)
    print(f"✅ Recording saved to {filename}")
    return filename


def transcribe_audio_whisper(audio_file="recorded.wav"):
    """Transcribe audio file using Whisper."""
    if not audio_file or not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    print(f"[INFO] Transcribing {audio_file} with Whisper...")
    result = _model.transcribe(audio_file)
    text = result.get("text", "").strip()
    print(f"📝 Transcribed Text: {text}")
    return text


# For standalone testing
if __name__ == "__main__":
    file_path = record_audio()
    transcription = transcribe_audio_whisper(file_path)
    print("Transcription:", transcription)
