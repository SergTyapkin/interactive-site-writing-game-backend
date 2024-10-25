from storage.database_storage import getTakenFragmentByUsername, getTakenFragmentById, getAllTakenFragmentsInMilestone, \
    addTakenFragment, updateTakenFragmentText, removeTakenFragment
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
                None,
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
def getExistingFragmentUser(user_username: str, milestone_id: int):
    taken_fragment = getTakenFragmentByUsername(milestone_id, user_username)
    print("By username", taken_fragment, user_username, milestone_id)
    return taken_fragment or None

def getExistingFragmentUserById(milestone_id: int, fragment_id: int):
    taken_fragment = getTakenFragmentById(milestone_id, fragment_id)
    print("By id", taken_fragment, fragment_id, milestone_id)
    return taken_fragment or None


def getAvailableFragments(milestone_id: int):
    # Get available fragments
    availableFragments: list[Fragment] = []
    for milestone in _all_milestones:
        if milestone.id == milestone_id:
            for fragment in milestone.fragments:
                if not fragment.only_for_system:
                    availableFragments.append(fragment)
            break
    takenFragments = getAllTakenFragmentsInMilestone(milestone_id)
    for fragment in takenFragments:
        for availableFragment in availableFragments:
            if availableFragment.fragment_id == fragment.fragment_id:
                availableFragments.remove(availableFragment)
                break
    return availableFragments

def updateFragmentText(fragment: Fragment, text: str):
    return updateTakenFragmentText(fragment.milestone_id, fragment.fragment_id, text)

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
    newFragment = addTakenFragment(Fragment(user_id, user_username, milestone_id, minFragment.fragment_id, minFragment.fragment_name, minFragment.fragment_description, minFragment.fragment_default_text, minFragment.fragment_hardness, None, minFragment.only_for_system))
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
    newFragment = addTakenFragment(Fragment(user_id, user_username, milestone_id, foundFragment.fragment_id, foundFragment.fragment_name, foundFragment.fragment_description, foundFragment.fragment_default_text, foundFragment.fragment_hardness, None, foundFragment.only_for_system))
    return newFragment

def removeUserFragmentByMilestoneIdFragmentId(milestone_id: int, fragment_id: int):
    fragment = getTakenFragmentById(milestone_id, fragment_id)
    if fragment is None:
        return False
    removeTakenFragment(milestone_id, fragment_id)
    return True

def getAllMilestoneFragments(milestone_id: int):
    res = getAllTakenFragmentsInMilestone(milestone_id)

    # Add available fragments
    availableFragments = []
    for milestone in _all_milestones:
        if milestone.id == milestone_id:
            availableFragments = milestone.fragments
            break
    for availableFragment in availableFragments:
        isFound = False
        for fragment in res:
            if fragment.fragment_id == availableFragment.fragment_id:
                isFound = True
        if isFound:
            continue

        user_id = 'NOT TAKEN'
        user_username = 'NOT TAKEN'
        if availableFragment.only_for_system:
            user_id = ''
            user_username = '__SYSTEM__'
        res.append(Fragment(user_id, user_username, milestone_id, availableFragment.fragment_id, availableFragment.fragment_name, availableFragment.fragment_description, availableFragment.fragment_default_text, availableFragment.fragment_hardness, None, availableFragment.only_for_system))
    return res

