# 🎵 Subsonic Music Player - Project Index

Welcome! This is a complete Python application for streaming music from a Subsonic server with a REST API for playback control.

## 📚 Documentation Guide (Start Here!)

### **👤 New Users - START HERE:**
1. **[QUICKSTART.md](QUICKSTART.md)** - Installation and first steps (5 min read)
2. **[README.md](README.md)** - Complete feature documentation (15 min read)

### **🔧 For Setup & Configuration:**
- **[.env.example](.env.example)** - Configuration template with all settings
- **[setup.sh](setup.sh)** - Automated setup script

### **🚀 For Production Deployment:**
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide (Systemd, Docker, Nginx)

### **📋 Project Overview:**
- **[PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt)** - High-level overview
- **[FINAL_SUMMARY.txt](FINAL_SUMMARY.txt)** - Detailed completion report

---

## 🚀 Quick Start (90 seconds)

```bash
# 1. Copy configuration template
cp .env.example .env

# 2. Edit with your Subsonic details (nano .env)
# 3. Run the application
python3 main.py

# 4. Open in browser
# http://127.0.0.1:8000/docs
```

---

## 📦 What's Included

### Core Application (1,185 lines)
- **main.py** - FastAPI server with 20+ REST endpoints
- **playback_manager.py** - Orchestration layer
- **subsonic_client.py** - Subsonic API integration
- **player.py** - VLC audio player wrapper
- **music_queue.py** - Thread-safe queue management
- **config.py** - Configuration management
- **client.py** - Python client library for testing

### Configuration
- **requirements.txt** - Python dependencies
- **.env.example** - Configuration template
- **setup.sh** - Automated setup

### Documentation
- **README.md** - Full documentation
- **QUICKSTART.md** - Quick start guide
- **DEPLOYMENT.md** - Production guide
- Project overview documents

---

## ✨ Key Features

✅ **Stream from Subsonic** - Direct real-time streaming  
✅ **Full Playback Control** - Play, pause, next, previous, seek, volume  
✅ **Queue Management** - Add/remove songs, manage playlists  
✅ **REST API** - 20+ endpoints with interactive documentation  
✅ **Thread-Safe** - Safe concurrent operations  
✅ **Production Ready** - Deployment guides included  

---

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/play` | Start playback |
| POST | `/pause` | Pause playback |
| POST | `/next` | Skip to next |
| POST | `/previous` | Go to previous |
| POST | `/seek` | Seek to position |
| POST | `/volume` | Set volume |
| POST | `/queue/add` | Add song to queue |
| POST | `/queue/add-starred` | Add starred songs |
| GET | `/queue` | Get current queue |
| GET | `/status` | Get playback status |
| GET | `/playlists` | List playlists |

See [README.md](README.md) for complete endpoint documentation.

---

## 🔧 System Requirements

- **Python** 3.9+
- **VLC** media player (brew install vlc)
- **Subsonic** server with network access
- **100 MB** free disk space

---

## 📋 File Reference

```
subsonic-player/
├── Core Application
│   ├── main.py ..................... FastAPI server
│   ├── playback_manager.py ......... Orchestration
│   ├── subsonic_client.py ......... Subsonic API
│   ├── player.py .................. VLC wrapper
│   ├── music_queue.py ............. Queue manager
│   ├── config.py .................. Configuration
│   └── client.py .................. Test client
│
├── Configuration
│   ├── requirements.txt ........... Dependencies
│   ├── .env.example ............... Config template
│   └── setup.sh ................... Setup script
│
└── Documentation
    ├── README.md .................. Full docs
    ├── QUICKSTART.md .............. Quick start
    ├── DEPLOYMENT.md .............. Production guide
    ├── PROJECT_SUMMARY.txt ........ Overview
    ├── FINAL_SUMMARY.txt .......... Completion
    └── INDEX.md ................... This file
```

---

## 🎯 Getting Started Paths

**Just Want to Play Music?**
→ Go to [QUICKSTART.md](QUICKSTART.md)

**Need Detailed Documentation?**
→ Read [README.md](README.md)

**Deploying to Production?**
→ Check [DEPLOYMENT.md](DEPLOYMENT.md)

**Want to Understand the Architecture?**
→ See [PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt)

**Looking for API Reference?**
→ Run the app and visit http://127.0.0.1:8000/docs

---

## 💡 Usage Examples

### Start Playing Starred Songs
```bash
curl -X POST http://127.0.0.1:8000/queue/add-starred
curl -X POST http://127.0.0.1:8000/play
```

### Skip to Next Song
```bash
curl -X POST http://127.0.0.1:8000/next
```

### Set Volume to 75%
```bash
curl -X POST http://127.0.0.1:8000/volume \
  -H "Content-Type: application/json" \
  -d '{"volume": 75}'
```

### Get Current Status
```bash
curl http://127.0.0.1:8000/status
```

### Using Python Client
```python
from client import SubsonicPlayerClient

client = SubsonicPlayerClient()
client.add_starred()
client.play()
print(client.status())
```

---

## 🆘 Need Help?

1. **First time setup?** → [QUICKSTART.md](QUICKSTART.md)
2. **Installation issues?** → [DEPLOYMENT.md](DEPLOYMENT.md) - Troubleshooting section
3. **API questions?** → [README.md](README.md) - API Endpoints section
4. **Configuration?** → [.env.example](.env.example) - all options explained

---

## 🎵 Ready to Use!

```bash
cd ~/subsonic-player
cp .env.example .env
# Edit .env with your Subsonic credentials
python3 main.py
```

Then open: **http://127.0.0.1:8000/docs**

Happy listening! 🎶
