import asyncio
import json

from aiohttp import ClientSession, WSMsgType

tasks: list[asyncio.Task[None]] = []


async def chat_client():
    async with ClientSession() as session, session.ws_connect("http://localhost:8765/") as ws:
        # Start a listener to receive messages
        async def receive_messages():
            async for msg in ws:
                if msg.type == WSMsgType.BINARY:
                    content = msg.data.decode()
                elif msg.type == WSMsgType.TEXT:
                    content = msg.data
                else:
                    print(f"Unknown message type: {msg.type}")
                    continue

                data = json.loads(content)
                print(f"\n{data['t']}: {data['d']}\n> ", end="", flush=True)

        tasks.append(asyncio.create_task(receive_messages()))

        # Send messages in a non-blocking way
        async def send_messages():
            while True:
                content = await asyncio.to_thread(input, "> ")
                if content.lower() == "ping":
                    await ws.send_json({"t": "PING", "d": {"content": "ping!"}})
                    continue
                if content.lower() == "glc":
                    await ws.send_json({"t": "GET_LEVEL_CABLES", "d": {"level_id": 1}})
                    continue
                if content.lower() == "no":
                    await ws.send_json({"t": "NO", "d": {}})
                    continue
                if content.lower() == "exit":
                    break
                if content.lower() == "dev_props":
                    await ws.send_json({"t": "GET_DEVICE_PROPS", "d": {"id": 1}})
                    continue
                if content.lower() == "glt":
                    await ws.send_json({"t": "GET_LEVEL_TASKS", "d": {"level_id": 1}})
                    continue

        await asyncio.create_task(send_messages())

        # # Wait for all tasks to complete
        # await asyncio.gather(*tasks)
        for task in tasks:
            if not task.done():
                task.cancel()


asyncio.run(chat_client())
