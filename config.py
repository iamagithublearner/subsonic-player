"""
Configuration from environment variables using python-dotenv
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration"""
    
    # Subsonic Server
    subsonic_server_url: str = os.getenv("SUBSONIC_SERVER_URL", "")
    subsonic_username: str = os.getenv("SUBSONIC_USERNAME", "")
    subsonic_password: str = os.getenv("SUBSONIC_PASSWORD", "")
    subsonic_client_name: str = os.getenv("SUBSONIC_CLIENT_NAME", "SubsonicPythonPlayer")
    subsonic_api_version: str = os.getenv("SUBSONIC_API_VERSION", "1.16.1")
    
    # API Server
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


_settings = None


def get_settings() -> Settings:
    """Get settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

