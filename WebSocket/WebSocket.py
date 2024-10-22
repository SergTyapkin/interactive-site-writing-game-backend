import json
import logging
from WebSocket.websocket_server.cb_websocket_server import CallbacksWebSocketServer
from storage.storage import User, Fragment


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
    def send_set_fragment(self, fragmentData: Fragment):
        self.send_broadcast(json.dumps({
            "event": "set_fragment",
            "data": {
                "id": fragmentData.fragment_id,
                "milestone_id": fragmentData.milestone_id,
                "name": fragmentData.fragment_name,
                "description": fragmentData.fragment_description,
                "default_text": fragmentData.fragment_default_text,
                "hardness": fragmentData.fragment_hardness,
                "text": fragmentData.text,
            }
        }))
    def send_fragment_updated(self, fragmentData: Fragment):
        self.send_broadcast(json.dumps({
            "event": "fragment_updated",
            "data": {
                "id": fragmentData.fragment_id,
                "user_id": fragmentData.user_id,
                "user_username": fragmentData.user_username,
                "milestone_id": fragmentData.milestone_id,
                "name": fragmentData.fragment_name,
                "description": fragmentData.fragment_description,
                "default_text": fragmentData.fragment_default_text,
                "hardness": fragmentData.fragment_hardness,
                "text": fragmentData.text,
            }
        }))
    def send_all_texts(self, fragmentsData: [Fragment]):
        self.send_broadcast(json.dumps({
            "event": "all_texts",
            "data": {
                "fragments": list(map(lambda fragmentData: {
                    "id": fragmentData.fragment_id,
                    "user_id": fragmentData.user_id,
                    "user_username": fragmentData.user_username,
                    "name": fragmentData.fragment_name,
                    "description": fragmentData.fragment_description,
                    "text": fragmentData.text,
                }, fragmentsData)),
            }
        }))

