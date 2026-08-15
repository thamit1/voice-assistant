import sounddevice as sd
import soundfile as sf

def record(seconds=3, samplerate=16000):
    print("Recording...")
    audio = sd.rec(
        int(seconds * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    sf.write("test.wav", audio, samplerate)
    print("Saved test.wav")

def play():
    print("Playing back...")
    audio, sr = sf.read("test.wav")
    sd.play(audio, sr)
    sd.wait()
    print("Playback complete")

if __name__ == "__main__":
    record()
    play()
