from utils.utils import read_config

config = read_config('config.json')


_last_user_uid = 0
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


class Fragment:
    user_id: int
    user_username: str
    milestone_id: int
    fragment_id: int
    fragment_name: str
    fragment_description: str
    fragment_default_text: str
    fragment_hardness: float
    text: str
    only_for_system: bool

    def __init__(self, user_id: int, user_username: str, milestone_id: int, fragment_id: int, fragment_name: str, fragment_description: str, fragment_default_text: str, fragment_hardness: float, only_for_system: bool = False):
        self.user_id = user_id
        self.user_username = user_username
        self.milestone_id = milestone_id
        self.fragment_id = fragment_id
        self.fragment_name = fragment_name
        self.fragment_description = fragment_description
        self.fragment_hardness = fragment_hardness
        self.fragment_default_text = fragment_default_text
        self.text = self.fragment_default_text
        self.only_for_system = only_for_system


class Milestone:
    id: int
    year: int
    name: str
    description: str
    code_language: str
    fragments: list[Fragment]

    def __init__(self, id: int, year: int, name: str, description: str, code_language: str, fragments: list[Fragment]):
        self.id = id
        self.year = year
        self.name = name
        self.description = description
        self.code_language = code_language
        self.fragments = fragments
