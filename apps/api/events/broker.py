from fastapi import WebSocket


class EventBroker:
    def __init__(self):
        self.clients: set[WebSocket] = set()

    async def connect(self, socket: WebSocket):
        await socket.accept()
        self.clients.add(socket)

    def disconnect(self, socket: WebSocket):
        self.clients.discard(socket)

    async def publish(self, event: str, data: dict):
        for socket in list(self.clients):
            try:
                await socket.send_json({"event": event, "data": data})
            except Exception:
                self.disconnect(socket)


broker = EventBroker()
