from utils.utils import read_config

config = read_config('config.json')


# ----------------- USER -----------------
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
            return user
    return None


# ----------------- FRAGMENTS -----------------
_fragments = set()


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

    def __init__(self, user_id: int, user_username: str, milestone_id: int, fragment_id: int, fragment_name: str, fragment_description: str, fragment_default_text: str, fragment_hardness: float):
        self.user_id = user_id
        self.user_username = user_username
        self.milestone_id = milestone_id
        self.fragment_id = fragment_id
        self.fragment_name = fragment_name
        self.fragment_description = fragment_description
        self.fragment_hardness = fragment_hardness
        self.fragment_default_text = fragment_default_text
        self.text = self.fragment_default_text


def getExistingFragmentUser(user_username: str, milestone_id: int):
    for fragment in _fragments:
        if fragment.user_username == user_username and fragment.milestone_id == milestone_id:
            return fragment
    return None
def getExistingFragmentUserById(milestone_id: int, fragment_id: int):
    for fragment in _fragments:
        if fragment.milestone_id == milestone_id and fragment.fragment_id == fragment_id:
            return fragment
    return None


def addFragmentUser(user_id: int, user_username: str, milestone_id: int, request_hardness: float):
    existingFragment = getExistingFragmentUser(user_username, milestone_id)
    if existingFragment:
        return existingFragment

    # Get available fragments
    availableFragments = []
    allMilestones = config['milestones']
    for milestone in allMilestones:
        if milestone['id'] == milestone_id:
            availableFragments = milestone['fragments']
            break
    for fragment in _fragments:
        if fragment.milestone_id == milestone_id:
            for availableFragment in availableFragments:
                if availableFragment['id'] == fragment.fragment_id or availableFragment.get('only_for_system'):
                    availableFragments.remove(availableFragment)
                    break
    if len(availableFragments) == 0:
        return None

    # Choose one of available fragments max closer to requested hardness
    minFragment = None
    minHardnessDiff = 999999999
    for availableFragment in availableFragments:
        hardnessDiff = abs(float(availableFragment['hardness']) - request_hardness)
        if hardnessDiff < minHardnessDiff:
            minHardnessDiff = hardnessDiff
            minFragment = availableFragment

    # Create new FragmentUser
    newFragment = Fragment(user_id, user_username, milestone_id, int(minFragment['id']), minFragment['name'], minFragment['description'], minFragment['default_text'], float(minFragment['hardness']))
    _fragments.add(newFragment)
    return newFragment


def getAllMilestoneFragments(milestone_id: int):
    res = []
    for fragment in _fragments:
        if fragment.milestone_id == milestone_id:
            res.append(fragment)

    # Add available fragments
    availableFragments = []
    allMilestones = config['milestones']
    for milestone in allMilestones:
        if milestone['id'] == milestone_id:
            availableFragments = milestone['fragments']
            break
    for availableFragment in availableFragments:
        isFound = False
        for fragment in _fragments:
            if fragment.fragment_id == availableFragment['id']:
                isFound = True
        if not isFound:
            if availableFragment.get('only_for_system'):
                res.append(Fragment('', '__SYSTEM__', milestone_id, int(availableFragment['id']), availableFragment['name'], availableFragment['description'], availableFragment['default_text'], float(availableFragment['hardness'])))
            else:
                res.append(Fragment('NOT TAKEN', 'NOT TAKEN', milestone_id, int(availableFragment['id']), availableFragment['name'], availableFragment['description'], availableFragment['default_text'], float(availableFragment['hardness'])))

    return res
