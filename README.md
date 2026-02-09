# ARIA (Adaptive Residential Intelligence Assistant)

A fully autonomous, self-initiating AI home automation system with persistent memory, tool calling, voice capabilities, and web dashboard.

## Features

- 🤖 **AI-Powered**: Uses Ollama with llama3.2 for intelligent responses
- 🧠 **Three-Tier Memory**: Working, Short-term, and Long-term memory systems
- 🔧 **Tool Calling**: Web search, device control, notifications
- 🏠 **Home Assistant Ready**: Integration-ready for smart home control
- 🎙️ **Voice Synthesis**: Piper TTS for voice announcements (optional)
- 📊 **Web Dashboard**: Beautiful React UI for monitoring and interaction
- 🔒 **Privacy-First**: Runs 100% locally, no cloud dependency

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Ollama with `llama3.2:3b-instruct-q4_K_M` model

### Setup

1. **Install Ollama Model**:

   ```bash
   ollama pull llama3.2:3b-instruct-q4_K_M
   ```

2. **Run Setup Script**:

   ```bash
   scripts\setup_windows.bat
   ```

3. **Install Frontend Dependencies**:

   ```bash
   cd frontend
   npm install
   ```

4. **Start ARIA**:

   ```bash
   scripts\start_all.bat
   ```

5. **Open Dashboard**: http://localhost:5173

## Project Structure

```
aria-home-assistant/
├── backend/          # FastAPI Python backend
├── frontend/         # React + Vite frontend
├── voice/            # Piper TTS (optional)
├── data/             # SQLite + ChromaDB storage
├── scripts/          # Windows batch scripts
└── docs/             # Documentation
```

## API Endpoints

- `POST /api/chat` - Send message to ARIA
- `GET /api/system/status` - System health
- `GET /api/devices/list` - List smart devices
- `POST /api/devices/action` - Control devices
- `POST /api/memory/search` - Search memories
- `WS /api/events/ws` - Real-time event stream

## License

MIT
