from faster_whisper import WhisperModel
import soundfile as sf
import numpy as np

model = WhisperModel("small", device="cpu")

def test_stt():
    print("Loading test.wav...")
    audio, sr = sf.read("test.wav")

    # FIX: convert audio to float32
    audio = audio.astype(np.float32)

    print("Transcribing...")
    segments, _ = model.transcribe(audio, vad_filter=True)

    text = "".join(seg.text for seg in segments)
    print("\n📝 Transcription:")
    print(text)

if __name__ == "__main__":
    test_stt()
