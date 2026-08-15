# 🎯 Feature Roadmap: Wake Word & Online LLMs

Planned enhancements for the voice assistant.

---

## Feature 1: Wake Word Detection ("Amit Assistant")

### Purpose
Only process audio and generate responses when hearing the wake word. Saves CPU and avoids unwanted interactions.

### Approach

#### Option A: Porcupine Wake Word (Recommended)
[Porcupine](https://github.com/picovoice/porcupine) - Lightweight, offline wake word detection

```bash
pip install pvporcupine
```

**Implementation:**
```python
import pvporcupine

# Initialize Porcupine with custom wake word
porcupine = pvporcupine.create(
    keywords=['americano'],  # Or custom "amit"
    access_key='YOUR_ACCESS_KEY'  # Free tier available
)

def listen_for_wake_word():
    """Listen until wake word detected"""
    print("🔍 Listening for wake word: 'Amit Assistant'")
    
    while True:
        audio = sd.rec(int(0.512 * 16000), ...)
        
        pcm = pvporcupine.process(audio)
        if pcm:
            print("✅ Wake word detected! Processing now...")
            return True

def main():
    while True:
        # Wait for wake word
        if listen_for_wake_word():
            # Start conversation
            audio, sr = record_audio()
            text = transcribe(audio, sr)
            reply = think(text)
            speak(reply)
```

**Pros:**
- ✅ Lightweight (CPU efficient)
- ✅ Offline
- ✅ Custom wake words available
- ✅ Low latency

**Cons:**
- Requires access key (free tier: 1 access key)
- Custom wake word training may be limited

---

#### Option B: Keyword Spotting with TinyML
Use [TensorFlow Lite](https://www.tensorflow.org/lite) for wake word detection

```bash
pip install tensorflow-lite
```

**Pros:**
- ✅ Fully offline
- ✅ Custom models can be trained
- ✅ Very lightweight

**Cons:**
- Requires model training
- More complex setup

---

#### Option C: Simple Loudness-Based Detection
Detect audio bursts and start recording

```python
def detect_speech_activity():
    """Simple VAD - detects loud enough audio"""
    print("🔍 Listening...")
    
    while True:
        audio = sd.rec(int(1 * 16000), ...)
        
        # Check if audio is loud enough
        rms = np.sqrt(np.mean(audio ** 2))
        if rms > AUDIO_THRESHOLD:
            print("✅ Speech detected!")
            return audio
```

**Pros:**
- ✅ No extra dependencies
- ✅ Simple implementation

**Cons:**
- ❌ Will activate on any loud noise
- ❌ No actual wake word detection

---

### Recommendation
**Use Porcupine (Option A)** - Best balance of simplicity, accuracy, and efficiency

---

## Feature 2: Online LLM Support

### Purpose
Allow switching between:
- **Offline:** Ollama (local, private, slow)
- **Online:** OpenAI, Claude, Gemini (faster, but requires API key)

### Implementation

#### Option A: Abstract LLM Interface
Create a common interface for both offline and online LLMs:

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class OllamaProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:3b"],
            input=prompt.encode("utf-8"),
            capture_output=True
        )
        return result.stdout.decode("utf-8").strip()

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-3-haiku",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
    
    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
```

#### Option B: Configuration File

Create `config.yaml`:
```yaml
# LLM Configuration
llm:
  provider: "ollama"  # or "openai", "claude", "gemini"
  
  # Offline LLM
  ollama:
    model: "llama3.2:3b"
    base_url: "http://localhost:11434"
  
  # Online LLMs
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4"
  
  claude:
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-haiku-20240307"
  
  gemini:
    api_key: "${GOOGLE_API_KEY}"
    model: "gemini-pro"

# Wake Word
wake_word:
  enabled: true
  keyword: "amit assistant"
  provider: "porcupine"  # or "porcupine"
```

#### Option C: Command-Line Switch

```bash
# Use offline Ollama (default)
python assistant.py --llm ollama

# Use OpenAI
python assistant.py --llm openai --api-key sk-...

# Use Claude
python assistant.py --llm claude --api-key sk-ant-...

# Use Gemini
python assistant.py --llm gemini --api-key AI...
```

---

### LLM Comparison

| Provider | Speed | Cost | Privacy | Accuracy |
|----------|-------|------|---------|----------|
| **Ollama (Local)** | Slow (CPU) | Free | ✅ Private | Medium |
| **OpenAI (GPT-4)** | Fast | $0.03-0.06/1K tokens | ❌ Cloud | Excellent |
| **Claude (Haiku)** | Fast | $0.80/$24 per M tokens | ❌ Cloud | Very Good |
| **Gemini (Free)** | Fast | Free (limited) | ❌ Cloud | Good |

---

## Implementation Roadmap

### Phase 1: Wake Word (Week 1-2)
- [ ] Install Porcupine and test wake word
- [ ] Integrate into `assistant.py`
- [ ] Create `assistant_wake_word.py` variant
- [ ] Test on different audio inputs
- [ ] Add custom wake word support

### Phase 2: Online LLMs (Week 2-3)
- [ ] Create LLM provider abstraction
- [ ] Implement OpenAI provider
- [ ] Implement Claude provider
- [ ] Implement Gemini provider
- [ ] Add configuration file support
- [ ] Create environment variable setup guide

### Phase 3: Integration (Week 3-4)
- [ ] Combine wake word + online LLMs
- [ ] Create `assistant_online.py` (wake word + online LLMs)
- [ ] Add cost tracking for API calls
- [ ] Update documentation
- [ ] Test end-to-end

---

## Example: Wake Word + Online LLM

```python
#!/usr/bin/env python3
"""
assistant_online.py - Voice assistant with wake word + online LLMs
"""

import os
import pvporcupine
import sounddevice as sd
from faster_whisper import WhisperModel
from openai import OpenAI

# Configuration
WAKE_WORD = "amit assistant"
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize
porcupine = pvporcupine.create(
    keywords=[WAKE_WORD],
    access_key=PORCUPINE_ACCESS_KEY
)
whisper = WhisperModel("tiny", device="cpu")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def listen_for_wake_word():
    """Listen until wake word is detected"""
    print("🔍 Listening for wake word...")
    
    while True:
        audio = sd.rec(int(0.512 * 16000), samplerate=16000, channels=1)
        sd.wait()
        
        if porcupine.process(audio.flatten()):
            print("✅ Wake word detected!")
            return True

def record_audio(duration=3):
    """Record audio after wake word"""
    print("🎤 Recording...")
    audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
    sd.wait()
    return audio.flatten()

def transcribe(audio):
    """Speech-to-text"""
    segments, _ = whisper.transcribe(audio, vad_filter=True)
    return "".join(seg.text for seg in segments).strip()

def think(prompt):
    """Query OpenAI"""
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content

def speak(text):
    """Use system text-to-speech or Piper"""
    # Placeholder: implement TTS
    print(f"💬 Assistant: {text}")

def main():
    print("🚀 Voice Assistant (Wake Word + Online LLM)")
    print("Say: 'Amit Assistant' followed by your question\n")
    
    while True:
        # Listen for wake word
        listen_for_wake_word()
        
        # Record user input
        audio = record_audio(duration=3)
        
        # Transcribe
        text = transcribe(audio)
        print(f"👂 You said: {text}")
        
        if not text:
            continue
        
        # Get response from OpenAI
        reply = think(text)
        speak(reply)

if __name__ == "__main__":
    main()
```

---

## Environment Setup

### For Porcupine (Wake Word)
```bash
pip install pvporcupine

# Get free access key from: https://console.picovoice.co/
export PORCUPINE_ACCESS_KEY="your_key_here"
```

### For OpenAI
```bash
pip install openai

# Get API key from: https://platform.openai.com/
export OPENAI_API_KEY="sk-..."
```

### For Claude
```bash
pip install anthropic

# Get API key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY="sk-ant-..."
```

### For Gemini
```bash
pip install google-generativeai

# Get API key from: https://ai.google.dev/
export GOOGLE_API_KEY="AI..."
```

---

## Cost Estimation (Monthly)

### 100 interactions/day:

| LLM | Cost | Details |
|-----|------|---------|
| **Ollama** | $0 | Free (CPU power) |
| **OpenAI GPT-4** | $50-100 | ~$0.015 per interaction |
| **Claude Haiku** | $10-20 | Cheapest paid option |
| **Gemini** | Free | Limited quota |

---

## Testing Checklist

- [ ] Wake word triggers reliably
- [ ] No false positives in quiet environment
- [ ] LLM switching works correctly
- [ ] API costs are within budget
- [ ] Fallback to Ollama if API fails
- [ ] Performance is acceptable
- [ ] Configuration loading works

---

**Status:** Planned for future releases
**Priority:** High (requested feature)
**Effort:** Medium (2-3 weeks estimated)

---
### Back of mind thoughts:
- wake word (“Amit Assistant”)
- streaming LLM responses
- background noise suppression
- VAD-based auto-stop recording
- conversation memory
- multi-turn context
- hotword detection using Silero
- GUI interface
- microphone gain control
- speaker selection
- faster Whisper model
- GPU acceleration
