import sounddevice as sd
import soundfile as sf
import subprocess
import tempfile
import os

def speak(text):
    print("Generating speech...")
    
    # Create temp file and close it immediately so Piper can write to it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav_path = tmp.name

    # 1. Update this to the exact, absolute path where your piper.exe is extracted
    piper_path = r"H:\\piper\\piper.exe" 
    
    # 2. Use absolute paths for your model to prevent working directory issues
    model_path = r"H:\\python\\voice-assistant\\models\\en_US-libritts-high.onnx"

    try:
        # Run subprocess and capture errors
        result = subprocess.run([
            piper_path,
            "--model", model_path,
            "--output_file", wav_path  # Note: Piper uses --output_file or -f, not --output
        ], input=text.encode("utf-8"), capture_output=True, text=False)

        # Check if Piper threw an error
        if result.returncode != 0:
            print(f"Piper Error: {result.stderr.decode('utf-8', errors='ignore')}")
            return

        # Check if file is empty
        if os.path.getsize(wav_path) == 0:
            print("Error: Generated WAV file is empty. Check your model path.")
            return

        print("Playing audio...")
        audio, sr = sf.read(wav_path)
        sd.play(audio, sr)
        sd.wait()

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Always clean up the file
        if os.path.exists(wav_path):
            os.remove(wav_path)
        print("Done.")

if __name__ == "__main__":
    speak("Hello Amit, your voice assistant is now speaking.")
