import json
import logging
from WebSocket.websocket_server.cb_websocket_server import CallbacksWebSocketServer
from WebSocket.websocket_server.websocket_server import Client
from storage.models import User, Fragment, Milestone


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


    def send_user_logined(self, client: Client, userData: User):
        self.send(client, json.dumps({
            "event": "user_logined",
            "data": {
                "id": userData.id,
                "username": userData.username,
                "is_admin": userData.is_admin,
            }
        }))
    def send_broadcast_available_fragments(self, milestone_id: int, fragmentsData: list[Fragment]):
        self.send_broadcast(json.dumps({
            "event": "available_fragments",
            "data": {
                "milestone_id": milestone_id,
                "fragments": list(map(
                    lambda fragmentData: {
                        "id": fragmentData.fragment_id,
                        "name": fragmentData.fragment_name,
                        "hardness": fragmentData.fragment_hardness,
                    },
                    fragmentsData
                )),
            }
        }))
    def send_set_fragment(self, client: Client, fragmentData: Fragment):
        self.send(client, json.dumps({
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
    def send_broadcast_fragment_updated(self, fragmentData: Fragment):
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
    def send_all_texts(self, client: Client, fragmentsData: list[Fragment]):
        self.send(client, json.dumps({
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
    def send_all_milestones(self, client: Client, milestonesData: list[Milestone], hasTakenFragmentsDict: dict[int, bool]):
        self.send(client, json.dumps({
            "event": "all_milestones",
            "data": {
                "milestones": list(map(lambda milestoneData: {
                    "id": milestoneData.id,
                    "year": milestoneData.year,
                    "name": milestoneData.name,
                    "description": milestoneData.description,
                    "code_language": milestoneData.code_language,
                    "has_taken_fragment": hasTakenFragmentsDict[milestoneData.id],
                }, milestonesData)),
            }
        }))

