import json
import logging
from WebSocket.websocket_server.cb_websocket_server import CallbacksWebSocketServer
from database.storage import User


# Singleton
class WebSocket(CallbacksWebSocketServer):
    def __new__(cls, *args, **kwargs):  # make singleton
        if not hasattr(cls, 'instance'):
            cls._init(cls, *args, **kwargs)
            cls.instance = super(WebSocket, cls).__new__(cls)
        return cls.instance

    def onConnected(self, client):
        print(client.address)
    def onDisconnected(self, client):
        print(client.address)

    def _init(self, *args, **kwargs):
        print("WS server created")
        self.onConnectedCallback = self.onConnected
        self.onDisconnectedCallback = self.onDisconnected
        super().__init__(self, *args, **kwargs, logLevel=logging.DEBUG)


    def send_user_logined(self, userData: User):
        self.send_broadcast(json.dumps({
            "event": "user_logined",
            "data": {
                "id": userData.id,
                "username": userData.username,
                "is_admin": userData.is_admin,
            }
        }))

