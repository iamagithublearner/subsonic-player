"""
Python client library for the Subsonic Music Player API
Use this to easily control playback from your own Python scripts
"""

import requests
from typing import Dict, Any, List, Optional


class SubsonicPlayerClient:
    """Client for controlling the Subsonic Music Player API"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize client
        
        Args:
            host: API host
            port: API port
        """
        self.base_url = f"http://{host}:{port}"
    
    def health(self) -> bool:
        """Check if API is running"""
        try:
            r = requests.get(f"{self.base_url}/health", timeout=2)
            return r.status_code == 200
        except:
            return False
    
    def play(self) -> Dict[str, Any]:
        """Start playback"""
        return requests.post(f"{self.base_url}/play").json()
    
    def pause(self) -> Dict[str, Any]:
        """Pause playback"""
        return requests.post(f"{self.base_url}/pause").json()
    
    def resume(self) -> Dict[str, Any]:
        """Resume playback"""
        return requests.post(f"{self.base_url}/resume").json()
    
    def next(self) -> Dict[str, Any]:
        """Skip to next song"""
        return requests.post(f"{self.base_url}/next").json()
    
    def previous(self) -> Dict[str, Any]:
        """Go to previous song"""
        return requests.post(f"{self.base_url}/previous").json()
    
    def set_volume(self, volume: int) -> Dict[str, Any]:
        """
        Set volume (0-100)
        
        Args:
            volume: Volume level
        """
        return requests.post(
            f"{self.base_url}/volume",
            json={"volume": volume}
        ).json()
    
    def seek(self, seconds: float) -> Dict[str, Any]:
        """
        Seek to position in song
        
        Args:
            seconds: Position in seconds
        """
        return requests.post(
            f"{self.base_url}/seek",
            json={"seconds": seconds}
        ).json()
    
    def status(self) -> Dict[str, Any]:
        """Get current playback status"""
        return requests.get(f"{self.base_url}/status").json()
    
    def queue(self) -> Dict[str, Any]:
        """Get current queue"""
        return requests.get(f"{self.base_url}/queue").json()
    
    def add_to_queue(self, song_id: str, title: str, artist: str, album: str) -> Dict[str, Any]:
        """Add song to queue"""
        return requests.post(
            f"{self.base_url}/queue/add",
            json={
                "song_id": song_id,
                "title": title,
                "artist": artist,
                "album": album
            }
        ).json()
    
    def add_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Add entire playlist to queue"""
        return requests.post(
            f"{self.base_url}/queue/add-playlist",
            json={"playlist_id": playlist_id}
        ).json()
    
    def add_starred(self) -> Dict[str, Any]:
        """Add all starred songs to queue"""
        return requests.post(f"{self.base_url}/queue/add-starred").json()
    
    def remove_from_queue(self, index: int) -> Dict[str, Any]:
        """Remove song from queue"""
        return requests.post(f"{self.base_url}/queue/remove/{index}").json()
    
    def clear_queue(self) -> Dict[str, Any]:
        """Clear entire queue"""
        return requests.post(f"{self.base_url}/queue/clear").json()
    
    def play_index(self, index: int) -> Dict[str, Any]:
        """Play song at queue index"""
        return requests.post(f"{self.base_url}/play/{index}").json()
    
    def playlists(self) -> Dict[str, Any]:
        """Get available playlists from Subsonic"""
        return requests.get(f"{self.base_url}/playlists").json()
    
    def starred(self) -> Dict[str, Any]:
        """Get starred songs from Subsonic"""
        return requests.get(f"{self.base_url}/starred").json()


if __name__ == "__main__":
    # Example usage
    client = SubsonicPlayerClient()
    
    # Check connection
    if not client.health():
        print("✗ API not running at http://127.0.0.1:8000")
        print("Start the application with: python3 main.py")
        exit(1)
    
    print("✓ Connected to Subsonic Music Player API")
    print()
    
    # Example: Add starred songs and play
    print("Adding starred songs to queue...")
    client.add_starred()
    
    print("Starting playback...")
    result = client.play()
    
    if "status" in result:
        print(f"✓ {result['status']}")
        print()
        
        # Get and print status
        status = client.status()
        print("Current Status:")
        print(f"  Now Playing: {status['current_song']['title'] if status['current_song'] else 'None'}")
        print(f"  Volume: {status['volume']}%")
        print(f"  Queue Size: {status['queue_size']}")
    else:
        print("✗ Failed to start playback")
        print(result)
