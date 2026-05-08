"""
Music queue management
"""

from typing import List, Dict, Any, Optional
from collections import deque
import threading


class Song:
    """Represents a song in the queue"""
    
    def __init__(self, song_id: str, title: str, artist: str, album: str, url: str, duration: int = 0):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.album = album
        self.url = url
        self.duration = duration
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration
        }


class Queue:
    """Music queue manager with thread safety"""
    
    def __init__(self):
        self.songs: List[Song] = []
        self.current_index: int = -1
        self.lock = threading.RLock()
    
    def add_song(self, song: Song):
        """Add song to end of queue"""
        with self.lock:
            self.songs.append(song)
    
    def add_songs(self, songs: List[Song]):
        """Add multiple songs to queue"""
        with self.lock:
            self.songs.extend(songs)
    
    def remove_song(self, index: int) -> bool:
        """
        Remove song from queue by index
        
        Returns:
            True if successful
        """
        with self.lock:
            if 0 <= index < len(self.songs):
                # Adjust current_index if needed
                if index < self.current_index:
                    self.current_index -= 1
                elif index == self.current_index:
                    self.current_index = -1
                
                self.songs.pop(index)
                return True
            return False
    
    def clear(self):
        """Clear entire queue"""
        with self.lock:
            self.songs.clear()
            self.current_index = -1
    
    def get_current_song(self) -> Optional[Song]:
        """Get currently playing song"""
        with self.lock:
            if 0 <= self.current_index < len(self.songs):
                return self.songs[self.current_index]
            return None
    
    def get_next_song(self) -> Optional[Song]:
        """Get next song in queue"""
        with self.lock:
            next_index = self.current_index + 1
            if 0 <= next_index < len(self.songs):
                return self.songs[next_index]
            return None
    
    def get_previous_song(self) -> Optional[Song]:
        """Get previous song in queue"""
        with self.lock:
            prev_index = self.current_index - 1
            if 0 <= prev_index < len(self.songs):
                return self.songs[prev_index]
            return None
    
    def next(self) -> Optional[Song]:
        """Advance to next song and return it"""
        with self.lock:
            if self.current_index + 1 < len(self.songs):
                self.current_index += 1
                return self.songs[self.current_index]
            return None
    
    def previous(self) -> Optional[Song]:
        """Go back to previous song and return it"""
        with self.lock:
            if self.current_index - 1 >= 0:
                self.current_index -= 1
                return self.songs[self.current_index]
            return None
    
    def play_song(self, index: int) -> bool:
        """Set current song by index"""
        with self.lock:
            if 0 <= index < len(self.songs):
                self.current_index = index
                return True
            return False
    
    def play_song_by_id(self, song_id: str) -> bool:
        """Set current song by ID"""
        with self.lock:
            for i, song in enumerate(self.songs):
                if song.id == song_id:
                    self.current_index = i
                    return True
            return False
    
    def get_queue(self) -> List[Dict[str, Any]]:
        """Get entire queue as list of dicts"""
        with self.lock:
            return [song.to_dict() for song in self.songs]
    
    def get_queue_with_status(self) -> Dict[str, Any]:
        """Get queue with current playing info"""
        with self.lock:
            current = self.songs[self.current_index] if 0 <= self.current_index < len(self.songs) else None
            return {
                "current_index": self.current_index,
                "now_playing": current.to_dict() if current else None,
                "queue_size": len(self.songs),
                "queue": [song.to_dict() for song in self.songs]
            }
    
    def length(self) -> int:
        """Get queue length"""
        with self.lock:
            return len(self.songs)
