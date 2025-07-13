# room_server.py
import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 8000))
connected_clients = set()

async def handle_client(websocket, path):
    print(f"[CONNECTED] {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"[RECEIVED] {message[:50]}...")  # truncate preview
            # Broadcast to all other clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print(f"[DISCONNECTED] {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        print(f"[LISTENING] WebSocket server on port {PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
