from connections import WS
import storage.storage as Storage


def register_callbacks():
    def get_all_milestones(client, data):
        milestones = Storage.getAllMilestones()
        WS.send_all_milestones(milestones)
    WS.setCallback("get_all_milestones", get_all_milestones)

