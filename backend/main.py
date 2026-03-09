from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json, asyncio, uuid

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()
scene_objects = []  # [{id, type, position, rotation, scale, color, creator}]


@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    # Send current scene to new connection
    await websocket.send_json({"type": "scene_sync", "objects": scene_objects})
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "add_object":
                obj = data["object"]
                # Ensure unique id
                if "id" not in obj:
                    obj["id"] = str(uuid.uuid4())
                scene_objects.append(obj)
                broadcast = {"type": "add_object", "object": obj}
                for c in list(clients - {websocket}):
                    try:
                        await c.send_json(broadcast)
                    except Exception:
                        clients.discard(c)

            elif msg_type == "update_object":
                obj_id = data.get("id")
                updates = data.get("updates", {})
                for obj in scene_objects:
                    if obj.get("id") == obj_id:
                        obj.update(updates)
                        break
                broadcast = {"type": "update_object", "id": obj_id, "updates": updates}
                for c in list(clients - {websocket}):
                    try:
                        await c.send_json(broadcast)
                    except Exception:
                        clients.discard(c)

            elif msg_type == "clear":
                scene_objects.clear()
                broadcast = {"type": "clear"}
                for c in list(clients):
                    try:
                        await c.send_json(broadcast)
                    except Exception:
                        clients.discard(c)

            elif msg_type == "cursor":
                # Broadcast cursor position to others
                broadcast = {"type": "cursor", "clientId": data.get("clientId"), "x": data.get("x"), "y": data.get("y")}
                for c in list(clients - {websocket}):
                    try:
                        await c.send_json(broadcast)
                    except Exception:
                        clients.discard(c)

    except WebSocketDisconnect:
        clients.discard(websocket)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "connections": len(clients),
        "objects": len(scene_objects),
    }
