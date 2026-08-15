import sounddevice as sd
import soundfile as sf
import numpy as np
import subprocess
import tempfile
import os
from faster_whisper import WhisperModel

# -----------------------------
# CONFIGURATION
# -----------------------------

# Absolute paths (recommended)
PIPER_EXE = r"H:\piper\piper.exe"
PIPER_MODEL = r"H:\python\voice-assistant\models\en_US-lessac-medium.onnx"
WHISPER_MODEL = "small"  # or "medium"
DEVICE = "cpu"

# Initialize Whisper STT
whisper = WhisperModel(WHISPER_MODEL, device=DEVICE)

# -----------------------------
# RECORD AUDIO
# -----------------------------
def record_audio(duration=4, samplerate=16000):
    print("\n🎤 Listening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    return audio.flatten(), samplerate

# -----------------------------
# SPEECH TO TEXT
# -----------------------------
def transcribe(audio, sr):
    print("📝 Transcribing...")
    segments, _ = whisper.transcribe(audio, vad_filter=True)
    text = "".join(seg.text for seg in segments).strip()
    print(f"👂 You said: {text}")
    return text

# -----------------------------
# LLM RESPONSE (Ollama)
# -----------------------------
def think(prompt):
    print("🤖 Thinking...")
    result = subprocess.run(
        ["ollama", "run", "llama3.2:3b"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    reply = result.stdout.decode("utf-8").strip()
    print(f"💬 Assistant: {reply}")
    return reply

# -----------------------------
# TEXT TO SPEECH (Piper)
# -----------------------------
def speak(text):
    print("🔊 Speaking...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav_path = tmp.name

    result = subprocess.run([
        PIPER_EXE,
        "--model", PIPER_MODEL,
        "--output_file", wav_path
    ], input=text.encode("utf-8"), capture_output=True)

    if result.returncode != 0:
        print("TTS Error:", result.stderr.decode("utf-8", errors="ignore"))
        return

    audio, sr = sf.read(wav_path)
    sd.play(audio, sr)
    sd.wait()

    os.remove(wav_path)

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    print("\n🚀 Voice Assistant Started")
    print("Say 'stop assistant' to exit.\n")

    while True:
        audio, sr = record_audio()

        text = transcribe(audio, sr)
        if not text:
            continue

        if "stop assistant" in text.lower():
            print("🛑 Assistant stopped.")
            break

        reply = think(text)
        speak(reply)

if __name__ == "__main__":
    main()
