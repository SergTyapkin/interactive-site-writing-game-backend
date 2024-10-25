from storage.models import User, Fragment, Milestone
from utils.utils import read_config

config = read_config('config.json')


# ----------------- USER -----------------

_users: set[User] = set()

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


# ----------------- MILESTONES ----------------
_all_milestones: list[Milestone] = list(map(
    lambda milestone: Milestone(
        milestone['id'],
        milestone['year'],
        milestone['name'],
        milestone['description'],
        milestone['code_language'],
        list(map(
            lambda fragment: Fragment(
                'ONLY FOR STORAGE',
                'ONLY FOR STORAGE',
                milestone['id'],
                fragment['id'],
                fragment['name'],
                fragment['description'],
                fragment['default_text'],
                fragment['hardness'],
                fragment.get('only_for_system') or False,
            ),
            milestone['fragments']
        ))
    ),
    config['milestones']
))


def getAllMilestones():
    return _all_milestones


# ----------------- FRAGMENTS -----------------
_taken_fragments: set[Fragment] = set()


def getExistingFragmentUser(user_username: str, milestone_id: int):
    for fragment in _taken_fragments:
        if fragment.user_username == user_username and fragment.milestone_id == milestone_id:
            return fragment
    return None
def getExistingFragmentUserById(milestone_id: int, fragment_id: int):
    for fragment in _taken_fragments:
        if fragment.milestone_id == milestone_id and fragment.fragment_id == fragment_id:
            return fragment
    return None


def getAvailableFragments(milestone_id: int):
    # Get available fragments
    availableFragments: list[Fragment] = []
    for milestone in _all_milestones:
        if milestone.id == milestone_id:
            availableFragments = milestone.fragments.copy()
            break
    for fragment in _taken_fragments:
        if fragment.milestone_id == milestone_id:
            for availableFragment in availableFragments:
                if availableFragment.fragment_id == fragment.fragment_id:
                    availableFragments.remove(availableFragment)
                    break
    for availableFragment in availableFragments:
        if availableFragment.only_for_system:
            availableFragments.remove(availableFragment)
    return availableFragments

def addFragmentUserByHardness(user_id: int, user_username: str, milestone_id: int, request_hardness: float):
    existingFragment = getExistingFragmentUser(user_username, milestone_id)
    if existingFragment:
        return existingFragment

    availableFragments = getAvailableFragments(milestone_id)
    if len(availableFragments) == 0:
        return None

    # Choose one of available fragments max closer to requested hardness
    minFragment = None
    minHardnessDiff = 999999999
    for availableFragment in availableFragments:
        hardnessDiff = abs(float(availableFragment.fragment_hardness) - request_hardness)
        if hardnessDiff < minHardnessDiff:
            minHardnessDiff = hardnessDiff
            minFragment = availableFragment

    # Create new FragmentUser
    newFragment = Fragment(user_id, user_username, milestone_id, minFragment.fragment_id, minFragment.fragment_name, minFragment.fragment_description, minFragment.fragment_default_text, minFragment.fragment_hardness, minFragment.only_for_system)
    _taken_fragments.add(newFragment)
    return newFragment

def addFragmentUserByFragmentId(user_id: int, user_username: str, milestone_id: int, fragment_id: int):
    existingFragment = getExistingFragmentUser(user_username, milestone_id)
    if existingFragment:
        return existingFragment

    availableFragments = getAvailableFragments(milestone_id)
    if len(availableFragments) == 0:
        return None

    # Check if fragment_id in available fragments
    foundFragment = None
    for availableFragment in availableFragments:
        if availableFragment.fragment_id == fragment_id:
            foundFragment = availableFragment
    if foundFragment is None:
        return None

    # Create new FragmentUser
    newFragment = Fragment(user_id, user_username, milestone_id, foundFragment.fragment_id, foundFragment.fragment_name, foundFragment.fragment_description, foundFragment.fragment_default_text, foundFragment.fragment_hardness, foundFragment.only_for_system)
    _taken_fragments.add(newFragment)
    return newFragment

def removeUserFragmentByMilestoneIdFragmentId(milestone_id: int, fragment_id: int):
    for fragment in _taken_fragments:
        if (fragment.milestone_id == milestone_id) and (fragment.fragment_id == fragment_id):
            _taken_fragments.remove(fragment)
            return True
    return False

def getAllMilestoneFragments(milestone_id: int):
    res = []
    for fragment in _taken_fragments:
        if fragment.milestone_id == milestone_id:
            res.append(fragment)

    # Add available fragments
    availableFragments = []
    for milestone in _all_milestones:
        if milestone.id == milestone_id:
            availableFragments = milestone.fragments
            break
    for availableFragment in availableFragments:
        isFound = False
        for fragment in _taken_fragments:
            if fragment.fragment_id == availableFragment.fragment_id:
                isFound = True
        if not isFound:
            user_id = 'NOT TAKEN'
            user_username = 'NOT TAKEN'
            if availableFragment.only_for_system:
                user_id = ''
                user_username = '__SYSTEM__'
            res.append(Fragment(user_id, user_username, milestone_id, availableFragment.fragment_id, availableFragment.fragment_name, availableFragment.fragment_description, availableFragment.fragment_default_text, availableFragment.fragment_hardness, availableFragment.only_for_system))

    return res
