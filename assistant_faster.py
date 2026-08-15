import sounddevice as sd
import soundfile as sf
import numpy as np
import subprocess
import tempfile
import os
import time
from faster_whisper import WhisperModel

# -----------------------------
# CONFIGURATION (OPTIMIZED FOR CPU)
# -----------------------------

# Absolute paths (recommended)
PIPER_EXE = r"H:\piper\piper.exe"
PIPER_MODEL = r"H:\python\voice-assistant\models\en_US-lessac-medium.onnx"
WHISPER_MODEL = "tiny"  # Fastest: tiny, base, small, medium
DEVICE = "cpu"
OLLAMA_MODEL = "llama3.2:3b"  # Using your existing 2.0GB model

# Performance tuning
RECORDING_DURATION = 4  # Seconds (shorter = faster response)
SAMPLE_RATE = 16000

# Initialize Whisper STT
print("⏳ Loading Whisper model (tiny)...")
whisper = WhisperModel(WHISPER_MODEL, device=DEVICE)

# -----------------------------
# PERFORMANCE TRACKING
# -----------------------------
def log_time(step_name, elapsed):
    print(f"⏱️  {step_name}: {elapsed:.2f}s")

# -----------------------------
# RECORD AUDIO
# -----------------------------
def record_audio(duration=RECORDING_DURATION, samplerate=SAMPLE_RATE):
    print("\n🎤 Listening...")
    start = time.time()
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    elapsed = time.time() - start
    log_time("Recording", elapsed)
    return audio.flatten(), samplerate

# -----------------------------
# SPEECH TO TEXT
# -----------------------------
def transcribe(audio, sr):
    print("📝 Transcribing...")
    start = time.time()
    segments, _ = whisper.transcribe(audio, vad_filter=True)
    text = "".join(seg.text for seg in segments).strip()
    elapsed = time.time() - start
    log_time("Speech-to-Text", elapsed)
    print(f"👂 You said: {text}")
    return text

# -----------------------------
# LLM RESPONSE (Ollama - Optimized for speed)
# -----------------------------
def think(prompt):
    print("🤖 Thinking...")
    start = time.time()
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=30  # Add timeout to prevent hanging
        )
        reply = result.stdout.decode("utf-8").strip()
        elapsed = time.time() - start
        log_time("LLM Response", elapsed)
        print(f"💬 Assistant: {reply}")
        return reply
    except subprocess.TimeoutExpired:
        print("⚠️  Ollama timeout - using fallback response")
        return "I'm thinking too slowly. Please try again."
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return "I encountered an error. Please try again."

# -----------------------------
# TEXT TO SPEECH (Piper)
# -----------------------------
def speak(text):
    print("🔊 Speaking...")
    start = time.time()

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
    
    elapsed = time.time() - start
    log_time("Text-to-Speech", elapsed)

    os.remove(wav_path)

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    print("\n🚀 Voice Assistant Started (Optimized for CPU)")
    print("📊 Model: Whisper tiny + Llama 3.2 3B")
    print("Say 'stop assistant' to exit.\n")

    loop_count = 0
    while True:
        loop_count += 1
        print(f"\n━━━ Loop #{loop_count} ━━━")
        loop_start = time.time()

        audio, sr = record_audio()

        text = transcribe(audio, sr)
        if not text:
            print("⚠️  No speech detected. Try again.")
            continue

        if "stop assistant" in text.lower():
            print("🛑 Assistant stopped.")
            break

        reply = think(text)
        speak(reply)

        total_loop_time = time.time() - loop_start
        log_time("Total Loop Time", total_loop_time)

if __name__ == "__main__":
    main()
