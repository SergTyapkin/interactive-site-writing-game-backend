from utils.utils import read_config

config = read_config('config.json')


_last_user_uid = 0
_users = set()


class User:
    id: int
    username: str
    is_admin: bool

    def __init__(self, username):
        global _last_user_uid
        _last_user_uid += 1
        self.id = _last_user_uid
        self.username = username
        self.is_admin = (username == config['admin_username'])


def getUser(username: str):
    for user in _users:
        if user.username == username:
            return user
    return None


def addUser(username: str):
    existingUser = getUser(username)
    if existingUser is not None:
        return existingUser
    newUser = User(username)
    _users.add(newUser)
    return newUser


def deleteUser(username: str):
    for user in _users:
        if user.username == username:
            _users.remove(user)
    return None
