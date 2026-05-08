# Subsonic Music Player

A Python application that streams music from a Subsonic server and exposes an HTTP API for controlling playback.

## Features

- **Stream from Subsonic**: Direct streaming of music from your Subsonic server
- **Playback Control**: Play, pause, next, previous, seek, volume control
- **Queue Management**: Add/remove songs, manage playlists, auto-advance to next song
- **REST API**: Full HTTP API for remote control
- **Thread-Safe**: Safe concurrent access to player state

## Setup

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Configure Subsonic Server

Copy `.env.example` to `.env` and fill in your Subsonic server details:

```bash
cp .env.example .env
```

Edit `.env`:
```
SUBSONIC_SERVER_URL=http://your-subsonic-server.com
SUBSONIC_USERNAME=your_username
SUBSONIC_PASSWORD=your_password
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=false
```

### 3. Run the Application

```bash
python3 main.py
```

The API will be available at `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

### Health Check
- `GET /health` - Check server status

### Playback Control
- `POST /play` - Start playback of current song
- `POST /play/{index}` - Play song at queue index
- `POST /pause` - Pause playback
- `POST /resume` - Resume playback
- `POST /next` - Skip to next song
- `POST /previous` - Go to previous song
- `POST /volume` - Set volume (0-100)
  ```json
  {"volume": 50}
  ```
- `POST /seek` - Seek to position (seconds)
  ```json
  {"seconds": 120.5}
  ```

### Queue Management
- `GET /queue` - Get current queue and playback status
- `POST /queue/add` - Add song to queue
  ```json
  {
    "song_id": "123",
    "title": "Song Title",
    "artist": "Artist Name",
    "album": "Album Name"
  }
  ```
- `POST /queue/add-playlist` - Add entire playlist
  ```json
  {"playlist_id": "playlist-id"}
  ```
- `POST /queue/add-starred` - Add all starred songs
- `POST /queue/remove/{index}` - Remove song from queue
- `POST /queue/clear` - Clear entire queue

### Playback Status
- `GET /status` - Get current playback status

### Subsonic Data
- `GET /playlists` - Get available playlists from Subsonic
- `GET /starred` - Get starred songs from Subsonic

## Usage Example

### Using cURL

```bash
# Add starred songs to queue
curl -X POST http://127.0.0.1:8000/queue/add-starred

# Start playback
curl -X POST http://127.0.0.1:8000/play

# Skip to next song
curl -X POST http://127.0.0.1:8000/next

# Set volume to 75%
curl -X POST http://127.0.0.1:8000/volume \
  -H "Content-Type: application/json" \
  -d '{"volume": 75}'

# Get queue status
curl http://127.0.0.1:8000/queue
```

### Using Python

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Add starred songs
requests.post(f"{BASE_URL}/queue/add-starred")

# Start playback
requests.post(f"{BASE_URL}/play")

# Get status
status = requests.get(f"{BASE_URL}/status").json()
print(status)
```

## Project Structure

```
subsonic-player/
├── main.py                  # FastAPI application & endpoints
├── config.py               # Configuration management
├── subsonic_client.py      # Subsonic API client
├── player.py               # VLC player wrapper
├── queue.py                # Queue management
├── playback_manager.py     # Coordinates all components
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
└── README.md              # This file
```

## Architecture

1. **SubsonicClient** - Handles authentication and API calls to Subsonic server
2. **VLCPlayer** - Wraps python-vlc for audio playback control
3. **Queue** - Manages song queue with thread-safe operations
4. **PlaybackManager** - Orchestrates player, queue, and Subsonic integration
5. **FastAPI** - Exposes HTTP API for remote control

## Threading

All components are thread-safe:
- Queue uses `threading.RLock` for concurrent access
- PlaybackManager uses locks to coordinate player and queue state
- VLC player handles thread-safe media operations

## Notes

- Streaming is direct from Subsonic (no local caching)
- Song auto-advances to next in queue when finished
- Volume range is 0-100
- Seek position is in seconds
- All API responses include current queue size and playback status
