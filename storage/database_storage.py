import storage.SQL_requests as SQL
from connections import DB
from storage.models import Fragment


def _dictFragmentToClass(fragment: dict):
    if not fragment:
        return None
    return Fragment(
        fragment['user_id'],
        fragment['user_username'],
        fragment['milestone_id'],
        fragment['fragment_id'],
        fragment['fragment_name'],
        fragment['fragment_description'],
        fragment['fragment_default_text'],
        fragment['fragment_hardness'],
        fragment['text'],
    )

def getAllTakenFragmentsInMilestone(milestone_id: int):
    fragments = DB.execute(SQL.selectAllUserFragmentsByMilestoneId, [milestone_id], manyResults=True)
    return list(map(_dictFragmentToClass, fragments))


def getTakenFragmentById(milestone_id: int, fragment_id: int):
    fragment = DB.execute(SQL.selectUserFragmentByMilestoneIdFragmentId, [milestone_id, fragment_id])
    if not fragment:
        return None
    return _dictFragmentToClass(fragment)

def getTakenFragmentByUsername(milestone_id: int, username: str):
    fragment = DB.execute(SQL.selectUserFragmentByMilestoneIdUsername, [milestone_id, username])
    if not fragment:
        return None
    return _dictFragmentToClass(fragment)


def updateTakenFragmentText(milestone_id: int, fragment_id: int, text: str):
    res = DB.execute(SQL.updateUserFragmentTextByMilestoneIdFragmentId, [text, milestone_id, fragment_id])
    if not res:
        return None
    return _dictFragmentToClass(res)


def addTakenFragment(fragment: Fragment):
    res = DB.execute(SQL.insertUserFragment, [fragment.user_id, fragment.user_username, fragment.milestone_id, fragment.fragment_id, fragment.fragment_name, fragment.fragment_description, fragment.fragment_default_text, fragment.fragment_hardness, fragment.text])
    if not fragment:
        print("CAN'T ADD NEW FRAGMENT")
        return None
    return _dictFragmentToClass(res)


def removeTakenFragment(milestone_id: int, fragment_id: int):
    DB.execute(SQL.deleteUserFragmentByMilestoneIdFragmentId, [milestone_id, fragment_id])

