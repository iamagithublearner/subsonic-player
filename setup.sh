#!/bin/bash
# Installation and setup guide for Subsonic Music Player

echo "=== Subsonic Music Player Setup ==="
echo

# Check Python version
echo "Checking Python version..."
python3 --version

# Install dependencies
echo
echo "Installing Python dependencies..."
pip3 install -q -r requirements.txt

# Check if VLC is installed
echo
echo "Checking VLC installation..."
if command -v vlc &> /dev/null; then
    echo "✓ VLC is installed"
else
    echo "⚠ VLC is not installed"
    echo "On macOS, install with: brew install vlc"
    echo "On Linux (Ubuntu), install with: sudo apt-get install vlc"
    echo "On Linux (Fedora), install with: sudo dnf install vlc"
fi

# Setup .env file
echo
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your Subsonic credentials."
else
    echo ".env file already exists."
fi

# Run basic tests
echo
echo "Running import tests..."
python3 -c "
from config import get_settings
from subsonic_client import SubsonicClient
from music_queue import Queue, Song
print('✓ All core modules imported successfully')
"

echo
echo "Setup complete! Run the application with:"
echo "  python3 main.py"
echo
echo "API documentation will be available at:"
echo "  http://127.0.0.1:8000/docs"
