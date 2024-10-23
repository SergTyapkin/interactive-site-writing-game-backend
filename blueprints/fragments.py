from connections import WS
import storage.storage as Storage


def register_callbacks():
    def take_fragment(client, data):
        user_id = int(data['user_id'])
        user_username = data['user_username']
        milestone_id = int(data['milestone_id'])
        request_hardness = float(data['request_hardness'])
        fragment = Storage.addFragmentUser(user_id, user_username, milestone_id, request_hardness)
        if fragment is None:
            return
        WS.send_set_fragment(fragment)
    WS.setCallback("take_fragment", take_fragment)

    def update_fragment_text(client, data):
        milestone_id = int(data['milestone_id'])
        fragment_id = int(data['fragment_id'])
        fragment_text = data['fragment_text']
        fragment = Storage.getExistingFragmentUserById(milestone_id, fragment_id)
        if fragment is None:
            print("CRITICAL ERROR. FRAGMENT NOT EXISTING")
            return
        fragment.text = fragment_text
        WS.send_fragment_updated(fragment)
    WS.setCallback("update_fragment_text", update_fragment_text)

    def get_all_texts(client, data):
        milestone_id = int(data['milestone_id'])
        fragments = Storage.getAllMilestoneFragments(milestone_id)
        WS.send_all_texts(fragments)
    WS.setCallback("get_all_texts", get_all_texts)
