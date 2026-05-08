"""
Subsonic Music Player - Main Application with API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import threading

from config import get_settings
from subsonic_client import SubsonicClient
from playback_manager import PlaybackManager
from music_queue import Song

# Initialize
settings = get_settings()
app = FastAPI(
    title="Subsonic Music Player API",
    description="Control music playback from Subsonic server",
    version="0.1.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global playback manager
playback_manager: Optional[PlaybackManager] = None


# Pydantic models for API
class PlaySongRequest(BaseModel):
    song_id: str
    title: str
    artist: str
    album: str


class QueueAddRequest(BaseModel):
    song_id: str
    title: str
    artist: str
    album: str


class PlaylistAddRequest(BaseModel):
    playlist_id: str


class VolumeRequest(BaseModel):
    volume: int


class SeekRequest(BaseModel):
    seconds: float


class RemoveFromQueueRequest(BaseModel):
    index: int


# API Endpoints

@app.on_event("startup")
async def startup_event():
    """Initialize playback manager on startup"""
    global playback_manager
    
    if not settings.subsonic_server_url or not settings.subsonic_username or not settings.subsonic_password:
        raise RuntimeError("Subsonic credentials not configured. Set SUBSONIC_SERVER_URL, SUBSONIC_USERNAME, and SUBSONIC_PASSWORD in .env")
    
    try:
        subsonic = SubsonicClient(
            server_url=settings.subsonic_server_url,
            username=settings.subsonic_username,
            password=settings.subsonic_password,
            client_name=settings.subsonic_client_name,
            api_version=settings.subsonic_api_version
        )
        
        # Test connection
        if not subsonic.ping():
            raise RuntimeError("Failed to connect to Subsonic server")
        
        playback_manager = PlaybackManager(subsonic)
        print("✓ Playback manager initialized")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "server": settings.subsonic_server_url}


# Playback Control Endpoints

@app.post("/play")
async def play():
    """Start playback of current song"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    if playback_manager.play():
        return {"status": "playing", "song": playback_manager.queue.get_current_song().to_dict()}
    else:
        raise HTTPException(status_code=400, detail="No song to play")


@app.post("/play/{index}")
async def play_index(index: int):
    """Play song at queue index"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    if playback_manager.play_index(index):
        return {"status": "playing", "index": index}
    else:
        raise HTTPException(status_code=400, detail="Invalid queue index")


@app.post("/pause")
async def pause():
    """Pause playback"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    playback_manager.pause()
    return {"status": "paused"}


@app.post("/resume")
async def resume():
    """Resume playback"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    playback_manager.resume()
    return {"status": "playing"}


@app.post("/next")
async def next_song():
    """Skip to next song"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    if playback_manager.next():
        return {"status": "success", "song": playback_manager.queue.get_current_song().to_dict()}
    else:
        raise HTTPException(status_code=400, detail="No next song in queue")


@app.post("/previous")
async def previous_song():
    """Go to previous song"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    if playback_manager.previous():
        return {"status": "success", "song": playback_manager.queue.get_current_song().to_dict()}
    else:
        raise HTTPException(status_code=400, detail="No previous song in queue")


@app.post("/volume")
async def set_volume(request: VolumeRequest):
    """Set volume level (0-100)"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    if not 0 <= request.volume <= 100:
        raise HTTPException(status_code=400, detail="Volume must be between 0 and 100")
    
    playback_manager.set_volume(request.volume)
    return {"volume": playback_manager.get_volume()}


@app.post("/seek")
async def seek(request: SeekRequest):
    """Seek to position in current song"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    if request.seconds < 0:
        raise HTTPException(status_code=400, detail="Seek position must be positive")
    
    playback_manager.seek(request.seconds)
    return {"position": request.seconds}


# Queue Management Endpoints

@app.post("/queue/add")
async def queue_add(request: QueueAddRequest):
    """Add song to queue"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    song = Song(
        song_id=request.song_id,
        title=request.title,
        artist=request.artist,
        album=request.album,
        url=""
    )
    playback_manager.add_to_queue(song)
    return {"status": "added", "queue_size": playback_manager.queue.length()}


@app.post("/queue/add-playlist")
async def queue_add_playlist(request: PlaylistAddRequest):
    """Add entire playlist to queue"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    try:
        count = playback_manager.add_playlist_to_queue(request.playlist_id)
        return {"status": "added", "songs_added": count, "queue_size": playback_manager.queue.length()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/queue/add-starred")
async def queue_add_starred():
    """Add all starred songs to queue"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    try:
        count = playback_manager.add_starred_to_queue()
        return {"status": "added", "songs_added": count, "queue_size": playback_manager.queue.length()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/queue/remove/{index}")
async def queue_remove(index: int):
    """Remove song from queue"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    if playback_manager.remove_from_queue(index):
        return {"status": "removed", "queue_size": playback_manager.queue.length()}
    else:
        raise HTTPException(status_code=400, detail="Invalid queue index")


@app.post("/queue/clear")
async def queue_clear():
    """Clear entire queue"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    playback_manager.clear_queue()
    return {"status": "cleared", "queue_size": 0}


@app.get("/queue")
async def get_queue():
    """Get current queue"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    return playback_manager.get_queue()


@app.get("/status")
async def get_status():
    """Get playback status"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    return playback_manager.get_status()


# Subsonic API Access

@app.get("/playlists")
async def list_playlists():
    """Get available playlists from Subsonic"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    try:
        playlists = playback_manager.subsonic.get_playlists()
        return {"playlists": playlists}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/starred")
async def list_starred():
    """Get starred songs from Subsonic"""
    if not playback_manager:
        raise HTTPException(status_code=503, detail="Playback manager not initialized")
    
    try:
        songs = playback_manager.subsonic.get_starred()
        return {"songs": songs}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
