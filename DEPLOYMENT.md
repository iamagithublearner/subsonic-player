# Deployment Guide - Subsonic Music Player

## Overview
Your Python Subsonic Music Player is ready for deployment. This guide covers setup, configuration, and deployment options.

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] VLC media player installed on target system
- [ ] Subsonic server running and accessible
- [ ] Network access from the player to Subsonic server
- [ ] Python dependencies installed (pip3 install -r requirements.txt)

## Local Deployment

### Step 1: Install System Dependencies

**macOS:**
```bash
brew install vlc
```

**Ubuntu/Debian:**
```bash
sudo apt-get install vlc libvlc-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install vlc
```

### Step 2: Clone/Set Up Project

```bash
cd ~/subsonic-player
pip3 install -r requirements.txt
```

### Step 3: Configure Application

```bash
cp .env.example .env
# Edit .env with your Subsonic credentials
nano .env
```

Required configuration:
```
SUBSONIC_SERVER_URL=http://your-server:port/subsonic
SUBSONIC_USERNAME=username
SUBSONIC_PASSWORD=password
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=false
```

### Step 4: Run Application

```bash
python3 main.py
```

Expected output:
```
✓ Playback manager initialized
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

## Server Deployment

### Option 1: Systemd Service (Recommended)

Create `/etc/systemd/system/subsonic-player.service`:

```ini
[Unit]
Description=Subsonic Music Player
After=network.target

[Service]
Type=simple
User=subsonic
WorkingDirectory=/home/subsonic/subsonic-player
ExecStart=/usr/bin/python3 /home/subsonic/subsonic-player/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable subsonic-player
sudo systemctl start subsonic-player
sudo systemctl status subsonic-player
```

### Option 2: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y vlc libvlc-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install -q -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python3", "main.py"]
```

Build and run:
```bash
docker build -t subsonic-player .
docker run -d --name subsonic-player \
  -e SUBSONIC_SERVER_URL=http://subsonic:8080/subsonic \
  -e SUBSONIC_USERNAME=user \
  -e SUBSONIC_PASSWORD=pass \
  -p 8000:8000 \
  subsonic-player
```

### Option 3: Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name music-player.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Considerations

1. **Environment Variables**: Store secrets in `.env`, never commit to version control
2. **Firewall**: Restrict API access to trusted IPs
3. **HTTPS**: Use reverse proxy with SSL/TLS in production
4. **Authentication**: Consider adding API key authentication if exposed publicly
5. **Subsonic Credentials**: Use dedicated Subsonic user with limited permissions

### Add Basic API Authentication (Optional)

Add to `main.py`:
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/health", dependencies=[Depends(security)])
async def health_check():
    ...
```

## Monitoring & Logging

### Check Service Status
```bash
sudo systemctl status subsonic-player
sudo journalctl -u subsonic-player -f
```

### Enable Debug Logging
Set `DEBUG=true` in `.env` for verbose output

### Monitor Resource Usage
```bash
top -p $(pgrep -f "python3 main.py")
```

## Troubleshooting

### VLC Not Found
```
OSError: dlopen(libvlccore.dylib, 0x0006)
```
Solution: Install VLC on the system

### Subsonic Connection Failed
```
Failed to connect to Subsonic server
```
- Verify `SUBSONIC_SERVER_URL` is correct
- Check Subsonic is running and accessible
- Verify credentials in `.env`
- Test with: `curl http://subsonic-url/rest/ping.view?u=user&p=pass`

### Port Already in Use
```
Address already in use
```
- Change `API_PORT` in `.env`
- Or kill existing process: `lsof -ti :8000 | xargs kill -9`

### Audio Playback Not Working
- Verify VLC is installed: `which vlc`
- Check audio device is configured: `aplay -l` (Linux) or `system_profiler SPAudioDataType` (macOS)

## Performance Tuning

### High Network Latency
- Enable local caching (modify `player.py`)
- Use lower bitrate in Subsonic

### Multiple Concurrent Requests
- Increase `workers` in uvicorn:
  ```bash
  uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
  ```

## Backup & Recovery

### Configuration Backup
```bash
cp .env .env.backup
```

### Queue Persistence (Optional Enhancement)
Modify `playback_manager.py` to save queue to file:
```python
import json

def save_queue(self):
    with open('queue.json', 'w') as f:
        json.dump(self.queue.get_queue(), f)
```

## Scaling Considerations

For multiple players:
- Run separate instances on different ports
- Use load balancer (Nginx, HAProxy)
- Consider shared queue storage (Redis)
- Monitor resource usage per instance

## Update & Maintenance

### Update Dependencies
```bash
pip3 install -r requirements.txt --upgrade
```

### Check for Security Updates
```bash
pip3 list --outdated
```

### Restart Service
```bash
sudo systemctl restart subsonic-player
```

## Support

For issues, check:
- `README.md` - Feature documentation
- `QUICKSTART.md` - Setup guide
- Application logs: `journalctl -u subsonic-player`

## API Testing in Production

```bash
curl -X GET http://your-server:8000/health
curl -X POST http://your-server:8000/queue/add-starred
curl -X POST http://your-server:8000/play
curl -X GET http://your-server:8000/status
```

Interactive documentation: `http://your-server:8000/docs`
