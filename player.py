"""
VLC Media Player wrapper for playback control
"""

import vlc
from typing import Optional, Callable
import threading
import time


class VLCPlayer:
    """Wrapper around VLC for music playback control"""
    
    def __init__(self, on_end_reached: Optional[Callable] = None):
        """
        Initialize VLC player
        
        Args:
            on_end_reached: Callback function when song finishes
        """
        self.instance = vlc.Instance()
        self.media_list_player = self.instance.media_list_player_new()
        self.media_list = self.instance.media_list_new()
        self.media_list_player.set_media_list(self.media_list)
        
        self.current_song_id: Optional[str] = None
        self.current_song_title: Optional[str] = None
        self.current_song_url: Optional[str] = None
        self.on_end_reached = on_end_reached
        self._setup_events()
    
    def _setup_events(self):
        """Setup event callbacks"""
        self.media_list_player.event_manager().event_attach(
            vlc.EventType.MediaListPlayerNextItemSet,
            self._on_next_item
        )
    
    def _on_next_item(self, event):
        """Called when media player moves to next item"""
        if self.on_end_reached:
            self.on_end_reached()
    
    def add_to_queue(self, url: str, title: str, song_id: str):
        """
        Add song to queue
        
        Args:
            url: Stream URL
            title: Song title for display
            song_id: Unique song ID
        """
        media = self.instance.media_new(url)
        media.get_mrl()  # Ensure media is initialized
        self.media_list.lock()
        try:
            self.media_list.add_media(media)
        finally:
            self.media_list.unlock()
    
    def play_now(self, url: str, title: str, song_id: str):
        """
        Clear queue and play song immediately
        
        Args:
            url: Stream URL
            title: Song title
            song_id: Song ID
        """
        self.stop()
        # Clear the media list and add new song
        self.media_list.lock()
        try:
            while self.media_list.count() > 0:
                self.media_list.remove_index(0)
            media = self.instance.media_new(url)
            self.media_list.add_media(media)
        finally:
            self.media_list.unlock()
        self.current_song_id = song_id
        self.current_song_title = title
        self.current_song_url = url
        
        self.media_list_player.play()
        
        # Wait for playback to start
        time.sleep(0.1)
    
    def play(self):
        """Start or resume playback"""
        self.media_list_player.play()
    
    def pause(self):
        """Pause playback"""
        self.media_list_player.pause()
    
    def stop(self):
        """Stop playback"""
        self.media_list_player.stop()
    
    def next(self):
        """Skip to next song in queue"""
        if self.media_list_player.next():
            self.current_song_id = None
            self.current_song_title = None
    
    def previous(self):
        """Go back to previous song in queue"""
        if self.media_list_player.previous():
            self.current_song_id = None
            self.current_song_title = None
    
    def set_volume(self, volume: int):
        """
        Set volume level
        
        Args:
            volume: Volume from 0 to 100
        """
        volume = max(0, min(100, volume))
        self.media_list_player.get_media_player().audio_set_volume(volume)
    
    def get_volume(self) -> int:
        """Get current volume level (0-100)"""
        return self.media_list_player.get_media_player().audio_get_volume()
    
    def seek(self, seconds: float):
        """
        Seek to position in current song
        
        Args:
            seconds: Position in seconds
        """
        player = self.media_list_player.get_media_player()
        # Convert to milliseconds
        player.set_time(int(seconds * 1000))
    
    def get_current_time(self) -> float:
        """Get current playback position in seconds"""
        player = self.media_list_player.get_media_player()
        return player.get_time() / 1000.0
    
    def get_duration(self) -> float:
        """Get duration of current song in seconds"""
        player = self.media_list_player.get_media_player()
        return player.get_length() / 1000.0
    
    def is_playing(self) -> bool:
        """Check if currently playing"""
        return self.media_list_player.is_playing()
    
    def get_queue(self):
        """Get list of songs in queue"""
        # Note: This would need to track added songs separately
        # since VLC API doesn't expose full media list easily
        pass
    
    def remove_from_queue(self, index: int) -> bool:
        """
        Remove song from queue by index
        
        Args:
            index: Queue position (0-based)
            
        Returns:
            True if successful
        """
        self.media_list.lock()
        try:
            return self.media_list.remove_index(index) == 0
        finally:
            self.media_list.unlock()
    
    def clear_queue(self):
        """Clear entire queue"""
        # Clear the media list by removing all items
        self.media_list.lock()
        try:
            while self.media_list.count() > 0:
                self.media_list.remove_index(0)
        finally:
            self.media_list.unlock()
        self.current_song_id = None
        self.current_song_title = None
