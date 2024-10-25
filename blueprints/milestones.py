from connections import WS
import storage.storage as Storage


def register_callbacks():
    def get_all_milestones(client, data):
        user_id = data['user_id']
        user_username = data['user_username']
        milestones = Storage.getAllMilestones()
        hasTakenFragmentsDict = {}
        for milestone in milestones:
            existingFragment = Storage.getExistingFragmentUser(user_username, milestone.id)
            hasTakenFragmentsDict[milestone.id] = bool(existingFragment)
        WS.send_all_milestones(client, milestones, hasTakenFragmentsDict)
    WS.setCallback("get_all_milestones", get_all_milestones)

