# ✦ AIR — Gesture 3D Collaboration Board

**[air.iamblwb.com](https://air.iamblwb.com)**

Draw shapes with your mouse → watch 3D objects materialize in real-time. Share the URL — everyone sees the same scene live.

## Gesture Recognition

| Draw | Gets | Object |
|------|------|--------|
| ○ Circle | 🔵 | Metal sphere |
| — Straight line | 📦 | Metallic bar |
| △ Triangle | 🔺 | Glowing cone |
| ≋ Wave line | 🌀 | Spring coil |
| Z shape | ⚡ | Lightning particles |

## Controls

- **Draw** — click and drag on the canvas
- **Shift + drag** — orbit camera
- **Clear** — reset scene (broadcasts to all)

## Stack

- **Backend**: FastAPI + WebSocket (Python 3.11)
- **Frontend**: Three.js r160 + UnrealBloom post-processing
- **Real-time**: WebSocket multi-user sync
- **Visual**: Dark + neon + particle glow

## Dev Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8005 --reload

# Frontend
# Serve index.html from frontend/ via any static server
python -m http.server 3000 -d frontend/
```

## Deploy

Managed via GitHub Actions CI/CD — pushes to `main` auto-deploy to VPS.
