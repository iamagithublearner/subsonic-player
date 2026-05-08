"""
Subsonic API Client for fetching songs and metadata
"""

import hashlib
import random
import string
from typing import Optional, List, Dict, Any
import requests
from urllib.parse import urljoin


class SubsonicClient:
    """Client for Subsonic API v1.16.1+"""
    
    def __init__(
        self,
        server_url: str,
        username: str,
        password: str,
        client_name: str = "SubsonicPythonPlayer",
        api_version: str = "1.16.1"
    ):
        """
        Initialize Subsonic client
        
        Args:
            server_url: Base URL of Subsonic server (e.g., http://subsonic.example.com)
            username: Subsonic username
            password: Subsonic password
            client_name: Client identifier for API calls
            api_version: API version to use
        """
        self.server_url = server_url.rstrip("/")
        self.username = username
        self.password = password
        self.client_name = client_name
        self.api_version = api_version
        self.session = requests.Session()
    
    def _get_salt(self) -> str:
        """Generate random salt for authentication"""
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))
    
    def _get_auth_params(self) -> Dict[str, str]:
        """Generate authentication parameters for API calls"""
        salt = self._get_salt()
        password_hash = hashlib.md5((self.password + salt).encode()).hexdigest()
        
        return {
            "u": self.username,
            "t": password_hash,
            "s": salt,
            "c": self.client_name,
            "v": self.api_version,
            "f": "json"
        }
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make authenticated request to Subsonic API
        
        Args:
            endpoint: API endpoint (e.g., 'rest/ping.view')
            params: Additional query parameters
            
        Returns:
            Response as dictionary
        """
        if params is None:
            params = {}
        
        # Add auth params
        auth_params = self._get_auth_params()
        params.update(auth_params)
        
        url = urljoin(self.server_url, endpoint)
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check Subsonic response status
            if data.get("subsonic-response", {}).get("status") != "ok":
                error = data.get("subsonic-response", {}).get("error", {})
                raise Exception(f"Subsonic API error: {error.get('message', 'Unknown error')}")
            
            return data.get("subsonic-response", {})
        
        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def ping(self) -> bool:
        """Test connection to Subsonic server"""
        try:
            self._make_request("rest/ping.view")
            return True
        except Exception:
            return False
    
    def get_starred(self, music_folder_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get starred songs from the server
        
        Returns:
            List of song objects with id, title, artist, album, path, etc.
        """
        params = {}
        if music_folder_id:
            params["musicFolderId"] = music_folder_id
        
        response = self._make_request("rest/getStarred.view", params)
        songs = response.get("starred", {}).get("song", [])
        
        # Ensure it's always a list
        if isinstance(songs, dict):
            songs = [songs]
        
        return songs
    
    def get_playlists(self) -> List[Dict[str, Any]]:
        """Get list of playlists"""
        response = self._make_request("rest/getPlaylists.view")
        playlists = response.get("playlists", {}).get("playlist", [])
        
        # Ensure it's always a list
        if isinstance(playlists, dict):
            playlists = [playlists]
        
        return playlists
    
    def get_playlist(self, playlist_id: str) -> List[Dict[str, Any]]:
        """
        Get songs in a playlist
        
        Args:
            playlist_id: Playlist ID
            
        Returns:
            List of song objects
        """
        response = self._make_request("rest/getPlaylist.view", {"id": playlist_id})
        songs = response.get("playlist", {}).get("entry", [])
        
        # Ensure it's always a list
        if isinstance(songs, dict):
            songs = [songs]
        
        return songs
    
    def get_stream_url(self, song_id: str) -> str:
        """
        Get streaming URL for a song
        
        Args:
            song_id: Song ID from Subsonic
            
        Returns:
            Full URL to stream the song
        """
        auth_params = self._get_auth_params()
        auth_params["id"] = song_id
        
        # Build query string
        query_string = "&".join(f"{k}={v}" for k, v in auth_params.items())
        return f"{self.server_url}/rest/stream.view?{query_string}"
