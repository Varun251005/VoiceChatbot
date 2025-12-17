# 🎤 Voice-Based AI Chatbot (Local LLaMA)

## 📝 Project Description

A simple terminal-based voice chatbot that uses local LLaMA AI model. Speak to the bot, get responses, and hear them back—all running locally on your machine.

**No frontend. No database. No cloud. Just pure local AI.**

---

## ✨ Features

✅ **Voice Input** - Records audio from microphone  
✅ **Speech-to-Text** - Converts voice to text using OpenAI Whisper  
✅ **Local AI** - Uses LLaMA3.2 model via Ollama  
✅ **Text Response** - Displays AI response in terminal  
✅ **Text-to-Speech** - Speaks the response aloud  
✅ **Simple Loop** - Continuous conversation until you say "exit"  

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Voice Input** | `speech_recognition` + `pyaudio` |
| **Speech-to-Text** | OpenAI `whisper` |
| **AI Model** | LLaMA 3.2 (via Ollama) |
| **Text-to-Speech** | `pyttsx3` |
| **API Communication** | `requests` |
| **Deep Learning** | `torch` |

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Microphone connected to your machine

### Step 1: Install Python Dependencies

```bash
cd voice_llama_bot
pip install -r requirements.txt
```

**Dependencies:**
- `speechrecognition` - Microphone audio input
- `pyaudio` - Audio interface
- `pyttsx3` - Text-to-speech
- `requests` - HTTP API calls
- `openai-whisper` - Speech-to-text
- `torch` - Deep learning framework

### Step 2: Start Ollama with LLaMA

```bash
ollama run llama3
```

> **Note:** This will download the LLaMA 3 model (first time only, ~5GB)

---

## 🚀 How to Run

Once Ollama is running in one terminal, open a new terminal:

```bash
python main.py
```

---

## 💬 Example Usage

```
==================================================
🎤 Voice LLaMA Chatbot Started
==================================================
💡 Say 'exit' to quit

🎤 Listening... Speak now!
✅ Audio saved. Processing with Whisper...
📝 You said: What is artificial intelligence?
🧠 Sending to LLaMA...
🤖 LLaMA says: Artificial intelligence is the simulation of human intelligence...

==================================================
📄 Response:
Artificial intelligence is the simulation of human intelligence...
==================================================

🔊 Speaking: Artificial intelligence is...
✅ Speech complete
```

---

## 🔄 Complete Voice Flow

```
1. 🎤 User speaks into microphone
   ↓
2. 🔊 Audio recorded and saved as audio.wav
   ↓
3. 📝 Whisper converts speech to text
   ↓
4. 🧠 Text sent to local LLaMA API
   ↓
5. 📄 LLaMA generates response
   ↓
6. 🔊 pyttsx3 speaks the response
   ↓
7. 🔁 Loop continues until user says "exit"
```

---

## 📁 Project Structure

```
voice_llama_bot/
├── main.py              # Main controller (all modules glued together)
├── voice_input.py       # 🎤 Voice to text (Whisper)
├── llama_client.py      # 🧠 Text to LLaMA to text
├── text_to_speech.py    # 🔊 Text to voice (pyttsx3)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🛑 Troubleshooting

### ❌ "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama run llama3`
- Check if it's on `http://localhost:11434`

### ❌ "No audio input detected"
- Check microphone connection
- Run: `python -m speech_recognition` to test mic

### ❌ "Whisper model not found"
- First run downloads the model (~2.7GB)
- Ensure you have internet connection

---

## 📝 Notes

- This is a **beginner-friendly** simple project
- No memory between conversations
- No UI—terminal only
- No streaming (full responses only)
- Perfect for learning voice AI concepts

---

## 🚀 Future Enhancements (Optional)

- Conversation memory
- Web UI
- Database to store chat history
- Streaming responses
- Multiple voice options

---

## 📄 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ for learning voice-based AI**
