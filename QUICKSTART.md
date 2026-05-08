# Quick Start Guide

## Installation

### 1. Prerequisites

- Python 3.9+
- VLC media player installed on your system
- Subsonic server

### 2. Install VLC (if not already installed)

**macOS:**
```bash
brew install vlc
```

**Ubuntu/Debian:**
```bash
sudo apt-get install vlc
```

**Fedora/RHEL:**
```bash
sudo dnf install vlc
```

### 3. Setup Application

```bash
cd ~/subsonic-player
bash setup.sh
```

Or manually:
```bash
pip3 install -r requirements.txt
cp .env.example .env
# Edit .env with your Subsonic credentials
```

## Configuration

Edit `.env` with your Subsonic server details:

```env
SUBSONIC_SERVER_URL=http://192.168.1.100:8080/subsonic
SUBSONIC_USERNAME=yourUsername
SUBSONIC_PASSWORD=yourPassword
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=false
```

## Running the App

```bash
python3 main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
✓ Playback manager initialized
```

## Using the API

### Interactive Docs (Swagger UI)
Open your browser: http://127.0.0.1:8000/docs

### Example: Play Your Starred Songs

```bash
# 1. Get starred songs
curl http://127.0.0.1:8000/starred

# 2. Add them to queue
curl -X POST http://127.0.0.1:8000/queue/add-starred

# 3. Start playing
curl -X POST http://127.0.0.1:8000/play

# 4. Check status
curl http://127.0.0.1:8000/status
```

### Example: Control Playback

```bash
# Skip to next
curl -X POST http://127.0.0.1:8000/next

# Pause
curl -X POST http://127.0.0.1:8000/pause

# Resume
curl -X POST http://127.0.0.1:8000/resume

# Set volume to 75%
curl -X POST http://127.0.0.1:8000/volume \
  -H "Content-Type: application/json" \
  -d '{"volume": 75}'
```

## Common Issues

### "Failed to connect to Subsonic server"
- Check `SUBSONIC_SERVER_URL` in `.env` is correct
- Verify Subsonic server is running and accessible
- Check username/password are correct

### "VLC library not found" (OSError)
- Install VLC: `brew install vlc` (macOS) or `sudo apt-get install vlc` (Linux)
- Restart the application after installing VLC

### Port 8000 already in use
- Change `API_PORT` in `.env` to a different port (e.g., 8001)
- Or find and stop the process using port 8000

## Architecture Overview

```
FastAPI Server (Port 8000)
    ↓
PlaybackManager (Orchestrates)
    ├─ SubsonicClient (Fetches songs from Subsonic server)
    ├─ VLCPlayer (Plays audio via VLC)
    └─ Queue (Manages song queue)
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/status` | Current playback status |
| GET | `/queue` | Current queue |
| GET | `/playlists` | Available playlists |
| GET | `/starred` | Starred songs |
| POST | `/play` | Play current song |
| POST | `/pause` | Pause playback |
| POST | `/resume` | Resume playback |
| POST | `/next` | Skip to next |
| POST | `/previous` | Go to previous |
| POST | `/seek` | Seek to position |
| POST | `/volume` | Set volume |
| POST | `/queue/add` | Add song to queue |
| POST | `/queue/add-playlist` | Add playlist |
| POST | `/queue/add-starred` | Add starred songs |
| POST | `/queue/remove/{index}` | Remove from queue |
| POST | `/queue/clear` | Clear queue |

## Next Steps

- Integrate with a frontend UI (web/mobile app)
- Add playlist browsing features
- Implement playback history
- Add user preferences (default volume, etc.)
- Deploy to a server
