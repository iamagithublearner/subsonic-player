"""
Playback manager - coordinates player, queue, and Subsonic API
"""

import threading
from typing import Optional, Dict, Any
from music_queue import Queue, Song
from player import VLCPlayer
from subsonic_client import SubsonicClient


class PlaybackManager:
    """Manages playback state, queue, and Subsonic integration"""
    
    def __init__(self, subsonic_client: SubsonicClient):
        """
        Initialize playback manager
        
        Args:
            subsonic_client: Configured Subsonic API client
        """
        self.subsonic = subsonic_client
        self.queue: Queue = Queue()
        self.player = VLCPlayer(on_end_reached=self._on_song_finished)
        self.lock = threading.RLock()
        self._stopped = False
    
    def _on_song_finished(self):
        """Called when current song finishes"""
        with self.lock:
            next_song = self.queue.next()
        if next_song:
            # Play in background thread to avoid blocking
            thread = threading.Thread(target=self._play_song_internal, args=(next_song,))
            thread.daemon = True
            thread.start()
    
    def _play_song_internal(self, song: Song):
        """Internal method to play a song"""
        try:
            # Fetch stream URL - runs in background thread to avoid blocking API requests
            url = self.subsonic.get_stream_url(song.id)
            self.player.play_now(url, song.title, song.id)
        except Exception as e:
            print(f"Error playing song: {e}")
    
    def add_to_queue(self, song: Song):
        """Add song to queue"""
        with self.lock:
            self.queue.add_song(song)
    
    def add_playlist_to_queue(self, playlist_id: str):
        """Fetch and add entire playlist to queue"""
        try:
            songs_data = self.subsonic.get_playlist(playlist_id)
            songs = [
                Song(
                    song_id=s.get("id"),
                    title=s.get("title", "Unknown"),
                    artist=s.get("artist", "Unknown"),
                    album=s.get("album", "Unknown"),
                    url="",  # Will be fetched when playing
                    duration=s.get("duration", 0)
                )
                for s in songs_data
            ]
            self.queue.add_songs(songs)
            return len(songs)
        except Exception as e:
            raise Exception(f"Failed to add playlist: {str(e)}")
    
    def add_starred_to_queue(self):
        """Fetch and add all starred songs to queue"""
        try:
            songs_data = self.subsonic.get_starred()
            songs = [
                Song(
                    song_id=s.get("id"),
                    title=s.get("title", "Unknown"),
                    artist=s.get("artist", "Unknown"),
                    album=s.get("album", "Unknown"),
                    url="",
                    duration=s.get("duration", 0)
                )
                for s in songs_data
            ]
            self.queue.add_songs(songs)
            return len(songs)
        except Exception as e:
            raise Exception(f"Failed to add starred songs: {str(e)}")
    
    def play(self):
        """Start playback of current song"""
        with self.lock:
            song = self.queue.get_current_song()
        if song:
            # Play in background thread to avoid blocking API requests
            thread = threading.Thread(target=self._play_song_internal, args=(song,))
            thread.daemon = True
            thread.start()
            return True
        return False
    
    def play_index(self, index: int) -> bool:
        """Play song at queue index"""
        with self.lock:
            if self.queue.play_song(index):
                song = self.queue.get_current_song()
            else:
                song = None
        if song:
            # Play in background thread to avoid blocking API requests
            thread = threading.Thread(target=self._play_song_internal, args=(song,))
            thread.daemon = True
            thread.start()
            return True
        return False
    
    def pause(self):
        """Pause playback"""
        self.player.pause()
    
    def resume(self):
        """Resume playback"""
        self.player.play()
    
    def next(self) -> bool:
        """Skip to next song"""
        with self.lock:
            next_song = self.queue.next()
        if next_song:
            # Play in background thread to avoid blocking API requests
            thread = threading.Thread(target=self._play_song_internal, args=(next_song,))
            thread.daemon = True
            thread.start()
            return True
        return False
    
    def previous(self) -> bool:
        """Go to previous song"""
        with self.lock:
            prev_song = self.queue.previous()
        if prev_song:
            # Play in background thread to avoid blocking API requests
            thread = threading.Thread(target=self._play_song_internal, args=(prev_song,))
            thread.daemon = True
            thread.start()
            return True
        return False
    
    def set_volume(self, volume: int):
        """Set volume (0-100)"""
        self.player.set_volume(volume)
    
    def get_volume(self) -> int:
        """Get current volume"""
        return self.player.get_volume()
    
    def seek(self, seconds: float):
        """Seek to position in current song"""
        self.player.seek(seconds)
    
    def remove_from_queue(self, index: int) -> bool:
        """Remove song from queue"""
        with self.lock:
            return self.queue.remove_song(index)
    
    def clear_queue(self):
        """Clear entire queue"""
        with self.lock:
            self.player.stop()
            self.queue.clear()
    
    def get_queue(self) -> Dict[str, Any]:
        """Get queue status"""
        with self.lock:
            current = self.queue.get_current_song()
            is_playing = self.player.is_playing()
            
            return {
                "is_playing": is_playing,
                "current_song": current.to_dict() if current else None,
                "current_index": self.queue.current_index,
                "queue_size": self.queue.length(),
                "volume": self.player.get_volume(),
                "current_time": self.player.get_current_time() if is_playing else 0,
                "duration": self.player.get_duration() if current else 0,
                "queue": self.queue.get_queue()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get playback status"""
        with self.lock:
            current = self.queue.get_current_song()
            is_playing = self.player.is_playing()
            
            status = {
                "is_playing": is_playing,
                "current_song": current.to_dict() if current else None,
                "current_time": self.player.get_current_time() if is_playing else 0,
                "duration": self.player.get_duration() if current else 0,
                "volume": self.player.get_volume(),
                "queue_size": self.queue.length(),
                "current_index": self.queue.current_index
            }
            return status
