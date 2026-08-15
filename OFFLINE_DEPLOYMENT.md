# 📦 Offline Deployment Guide

Guide for packaging the voice assistant for air-gapped or corporate environments where executables are restricted.

---

## Problem: .EXE Files Blocked

Many corporate networks block executable files for security. This guide provides alternatives.

---

## Solution 1: Use Python Package (Recommended ✅)

### Step 1: Install Piper as Python Package
```bash
pip install piper-tts
```

### Step 2: Modify `assistant.py`

Replace the subprocess call with Python:

```python
# BEFORE (uses piper.exe)
def speak(text):
    result = subprocess.run([PIPER_EXE, "--model", PIPER_MODEL, ...])

# AFTER (uses piper-tts Python package)
from piper.voice import PiperVoice
import wave

VOICE = None  # Cache voice

def speak(text):
    global VOICE
    if VOICE is None:
        VOICE = PiperVoice.load(PIPER_MODEL)
    
    audio = VOICE.synthesize(text)
    
    # Play audio
    sd.play(audio, sr=22050)
    sd.wait()
```

**Advantages:**
- ✅ No executables needed
- ✅ Fully Python-based
- ✅ Easier to package for offline
- ✅ Works on locked-down systems

---

## Solution 2: Pre-built Wheels Offline Package

Create a self-contained package with wheels (no downloads needed):

### Directory Structure
```
voice-assistant-offline-wheels.zip (1.2 GB)
│
├── wheels/
│   ├── piper_tts-1.2.0-py3-none-win_amd64.whl
│   ├── sounddevice-0.4.6-cp312-cp312-win_amd64.whl
│   ├── soundfile-0.12.1-py2.py3-none-any.whl
│   ├── numpy-1.21.0-cp312-cp312-win_amd64.whl
│   └── faster_whisper-0.9.0-py3-none-any.whl
│
├── models/
│   ├── whisper-tiny.pt
│   ├── en_US-lessac-medium.onnx
│   └── en_US-lessac-medium.onnx.json
│
├── code/
│   ├── assistant.py (modified for piper-tts)
│   ├── assistant_faster.py
│   └── requirements.txt
│
├── setup.bat
└── README_OFFLINE.md
```

### Create setup.bat
```batch
@echo off
echo Installing offline dependencies...
pip install --no-index --find-links ./wheels -r code/requirements.txt
echo.
echo Setup complete! Run: python code/assistant.py
pause
```

---

## Solution 3: Docker (Best for Locked Systems)

Build a Docker image that includes everything:

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy code
COPY code/ /app/code/
COPY models/ /app/models/

# Install dependencies
RUN pip install sounddevice soundfile numpy faster-whisper piper-tts

# Install Ollama (if available)
RUN curl https://ollama.ai/install.sh | sh

# Expose Ollama port if needed
EXPOSE 11434

CMD ["python", "code/assistant.py"]
```

**Build and run:**
```bash
docker build -t voice-assistant .
docker run -it --rm voice-assistant
```

---

## Solution 4: Modified Deployment (No Executables)

### Steps:
1. **Remove Piper.exe reference** from package
2. **Install piper-tts via pip** on target machine
3. **Update code** to use Python bindings instead of subprocess
4. **Package only:** code + models + requirements.txt

### Modified assistant.py (excerpt)
```python
# Configuration
PIPER_MODEL = r"C:\voice-assistant\models\en_US-lessac-medium.onnx"
WHISPER_MODEL = "tiny"
DEVICE = "cpu"

# Initialize Piper (Python version, not exe)
try:
    from piper.voice import PiperVoice
    piper = PiperVoice.load(PIPER_MODEL)
except ImportError:
    print("Install piper-tts: pip install piper-tts")
    sys.exit(1)

def speak(text):
    print("🔊 Speaking...")
    start = time.time()
    
    try:
        # Generate audio with Piper
        audio = piper.synthesize(text)
        
        # Play audio
        sd.play(audio, samplerate=22050)
        sd.wait()
        
        elapsed = time.time() - start
        print(f"⏱️  TTS: {elapsed:.2f}s")
    except Exception as e:
        print(f"Error: {e}")
```

---

## Solution 5: Build Piper from Source (Visual Studio)

If you have **Visual Studio with C++ build tools** installed:

### Requirements
- Visual Studio 2019 or later (with C++ workload)
- CMake (included with Visual Studio or install separately)
- Git

### Build Steps
```bash
# Clone Piper source
git clone https://github.com/rhasspy/piper.git
cd piper

# Create build directory
mkdir build && cd build

# Generate Visual Studio project
cmake .. -G "Visual Studio 17 2022"

# Build in Release mode
cmake --build . --config Release

# Binary will be at: piper\build\Release\piper.exe
```

### Advantages
- ✅ No executables downloaded (custom-built)
- ✅ Better chance of passing security scans (built in-house)
- ✅ Full source code control
- ✅ Can be distributed as DLLs instead of EXE

### Configure in assistant.py
```python
PIPER_EXE = r"C:\path\to\piper\build\Release\piper.exe"
PIPER_MODEL = r"C:\path\to\models\en_US-lessac-medium.onnx"
```

---

## Comparison: All Solutions

| Solution | Size | Complexity | Blocked .exe | Requires |
|----------|------|-----------|---|---|
| **1. piper-tts pip** | 50 MB | ⭐ Easy | ✅ No | Python |
| **2. Wheels zip** | 1.2 GB | ⭐⭐ Medium | ✅ No | Python |
| **3. Docker** | 2 GB | ⭐⭐⭐ Hard | ✅ No | Docker |
| **4. Modified code** | 400 MB | ⭐⭐ Medium | ✅ No | Python |
| **5. Build from source** | 50 MB | ⭐⭐ Medium | ✅ No | Visual Studio + CMake |

---

## Recommended Offline Package

**Best for corporate/air-gapped systems:**

```
voice-assistant-corporate.zip (500 MB)
├── code/
│   ├── assistant.py (using piper-tts)
│   ├── assistant_faster.py
│   ├── requirements.txt
│   └── *.py test files
├── models/
│   ├── whisper-tiny.pt (140 MB)
│   ├── en_US-lessac-medium.onnx (60 MB)
│   └── *.onnx.json
├── setup.bat
│   └── [Installs: pip install -r requirements.txt]
├── OFFLINE_DEPLOYMENT.md
└── README.md
```

**Setup on target machine:**
```bash
1. Extract zip file
2. Install Python 3.9+
3. Run: setup.bat
4. Download Ollama separately
5. Run: python code/assistant.py
```

---

## Checklist for Offline Package

- [ ] No `.exe` files included
- [ ] All Python packages in `requirements.txt`
- [ ] All models included (whisper + Piper ONNX)
- [ ] `setup.bat` for automated installation
- [ ] Clear instructions for Ollama (separate download)
- [ ] Version compatibility documented
- [ ] Tested on target system
- [ ] Checksums included (SHA256) for verification

---

## Troubleshooting

**Q: "ImportError: No module named 'piper'"**
A: Run `pip install piper-tts` or use wheels offline installer

**Q: ".exe still detected as virus"**
A: Use Python package only, no executables

**Q: "Ollama blocked"**
A: Ollama may need separate approval. Alternative: Use pre-cached models locally

**Q: "How to pre-cache Ollama models?"**
A: Pull on one machine, copy `~/.ollama/models/` to target

---

## Creating Pre-cached Ollama

On a machine with internet:
```bash
ollama pull llama3.2:3b
ollama pull neural-chat

# Find models directory (usually C:\Users\[user]\.ollama\models)
# Copy entire folder to USB drive or network share
```

On target machine:
```bash
# Set environment variable
set OLLAMA_MODELS=D:\ollama-models

# Start Ollama (will use pre-cached models)
ollama serve
```

---

**For questions: Check README.md or GitHub Issues**
