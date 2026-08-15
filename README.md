# 🧠 Local Voice Assistant (Python + Whisper + Ollama + Piper)

A fully local, privacy‑friendly voice assistant built using open-source tools. Everything runs offline on your machine—no cloud services required.

**Components:**
- **Speech-to-Text:** [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (OpenAI Whisper)  
- **LLM Reasoning:** [Ollama](https://ollama.ai/) (Llama 3.2, Phi, Gemma, etc.)  
- **Text-to-Speech:** [Piper](https://github.com/rhasspy/piper) (fast, offline TTS)  
- **Audio I/O:** sounddevice, soundfile  

---

## ✨ Features

- ✅ **100% Offline** – No external APIs or internet required
- ✅ **Privacy-First** – All processing happens locally on your machine
- ✅ **Modular Architecture** – Easy to extend and customize
- ✅ **Real-Time Voice Interaction** – Listen → Transcribe → Think → Speak

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Ollama** – [Download and install](https://ollama.ai/)
3. **Piper TTS** – [Download for Windows](https://github.com/rhasspy/piper/releases)
   - Extract the ZIP file to a local directory (e.g., `C:\piper\`)
   - Note the path to `piper.exe`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
   ```

2. Install Python dependencies:
   ```bash
   pip install sounddevice soundfile numpy faster-whisper
   ```

3. Download Ollama models:
   ```bash
   ollama pull llama3.2:3b
   ```

4. Download Piper voice models:
   - Download from [Hugging Face: rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US)
   - Extract the `.onnx` and `.onnx.json` files to the `models/` directory
   - Available voices: `en_US-lessac-medium`, `en_US-libritts-high`, etc.
   - Example:
     ```
     models/
     ├── en_US-lessac-medium.onnx
     ├── en_US-lessac-medium.onnx.json
     └── en_US-libritts-high.onnx
     └── en_US-libritts-high.onnx.json
     ```

5. Configure paths in `assistant.py`:
   ```python
   PIPER_EXE = r"C:\path\to\piper.exe"  # Windows path
   PIPER_MODEL = r"C:\path\to\models\en_US-lessac-medium.onnx"
   WHISPER_MODEL = "small"  # or "tiny", "base", "medium"
   ```

### Usage

Run the main assistant:
```bash
python assistant.py
```

Then speak naturally. Say **"stop assistant"** to exit.

---

## 📁 Project Structure

```
voice-assistant/
├── assistant.py              # Main voice assistant (listen → transcribe → think → speak)
├── audio_test.py             # Audio recording and playback test
├── stt_test.py               # Speech-to-text test
├── tts_test.py               # Text-to-speech test
├── models/                   # ONNX models for Piper TTS
│   ├── en_US-lessac-medium.onnx
│   ├── en_US-lessac-medium.onnx.json
│   ├── en_US-libritts-high.onnx
│   └── en_US-libritts-high.onnx.json
└── README.md
```

### Future Structure (Planned)

```
voice-assistant/
├── core/
│   ├── orchestrator.py       # Main loop (future refactor)
│   └── state.py              # Assistant state machine
├── stt/
│   ├── recorder.py           # Microphone recording
│   └── transcriber.py        # Whisper STT
├── llm/
│   ├── brain.py              # Ollama interface
│   └── prompts.py            # System prompts & persona
├── tts/
│   └── speaker.py            # Piper TTS interface
├── tools/
│   └── system_tools.py       # System commands, app launcher
└── tests/
    ├── test_audio.py
    ├── test_stt.py
    └── test_tts.py
```

---

## 🧪 Testing Individual Components

### Test Audio I/O
```bash
python audio_test.py
```
Records 3 seconds of audio and plays it back.

### Test Speech-to-Text
```bash
python stt_test.py
```
Transcribes `test.wav` using Whisper.

### Test Text-to-Speech
```bash
python tts_test.py
```
Generates speech and plays it back using Piper.

---

## ⚙️ Configuration

Edit `assistant.py` to customize:

| Setting | Description |
|---------|-------------|
| `PIPER_EXE` | Path to piper.exe executable |
| `PIPER_MODEL` | Path to ONNX model file |
| `WHISPER_MODEL` | Whisper model size: "tiny", "base", "small", "medium" |
| `DEVICE` | "cpu" or "cuda" (if GPU available) |

---

## 📚 Dependencies

```
sounddevice>=0.4.5
soundfile>=0.12.1
numpy>=1.21.0
faster-whisper>=0.9.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔧 Troubleshooting

**No audio input?**
- Check microphone permissions
- Test with `audio_test.py`

**Piper not found?**
- Verify `PIPER_EXE` path is correct and absolute
- Ensure piper.exe is extracted, not in a ZIP file

**Whisper model not loading?**
- First run will auto-download the model (~140 MB for "small")
- Ensure internet connection for initial download

**Ollama not responding?**
- Start Ollama: `ollama serve`
- Verify model is pulled: `ollama list`

---

## 📝 License

MIT License – Feel free to use and modify.

---

## 🎯 Roadmap

- [ ] Refactor to modular architecture (core/, stt/, llm/, tts/)
- [ ] Add tool support (open apps, web search, system commands)
- [ ] Implement assistant memory/context
- [ ] Web UI dashboard
- [ ] Docker containerization
- [ ] Multi-language support
- [ ] Custom wake word detection

---

**Built with ❤️ for privacy-conscious developers.**
