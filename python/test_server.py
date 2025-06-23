import asyncio
import json

from aiohttp import WSMsgType, web

connected_clients = set()


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected_clients.add(ws)
    print("New client connected")

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = json.loads(msg.data)
                print(f"Received from {data['author']}: {data['content']}")
                await broadcast(msg.data)
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        connected_clients.remove(ws)
        print("Client disconnected")

    return ws


async def broadcast(message):
    if connected_clients:
        await asyncio.gather(*[ws.send_str(message) for ws in connected_clients])


async def start_server():
    app = web.Application()
    app.router.add_get("/ws", websocket_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8765)
    await site.start()
    print("WebSocket server started on ws://localhost:8765")
    while True:  # noqa: ASYNC110
        await asyncio.sleep(3600)  # Keep running


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Server shutting down...")
