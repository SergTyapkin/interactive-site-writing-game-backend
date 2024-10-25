from connections import WS
import storage.storage as Storage


def register_callbacks():
    def login_user(client, data):
        user = Storage.addUser(data['username'])
        WS.send_user_logined(client, user)
    WS.setCallback("login_user", login_user)

    def logout_user(client, data):
        # Storage.deleteUser(data['username'])
        pass
    WS.setCallback("logout_user", logout_user)
