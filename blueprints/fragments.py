from connections import WS
import storage.storage as Storage


def register_callbacks():
    def get_all_available_fragments(client, data):
        milestone_id = int(data['milestone_id'])
        fragments = Storage.getAvailableFragments(milestone_id)
        WS.send_broadcast_available_fragments(milestone_id, fragments)
    WS.setCallback("get_all_available_fragments", get_all_available_fragments)

    def take_fragment(client, data):
        user_id = int(data['user_id'])
        user_username = data['user_username']
        milestone_id = int(data['milestone_id'])
        request_hardness = data.get('request_hardness')
        request_fragment_id = data.get('request_fragment_id')
        if request_hardness is not None:
            fragment = Storage.addFragmentUserByHardness(user_id, user_username, milestone_id, float(request_hardness))
        else:
            fragment = Storage.addFragmentUserByFragmentId(user_id, user_username, milestone_id, int(request_fragment_id))
        if fragment is None:
            return
        WS.send_set_fragment(client, fragment)
        get_all_available_fragments(client, data)
    WS.setCallback("take_fragment", take_fragment)

    def update_fragment_text(client, data):
        milestone_id = int(data['milestone_id'])
        fragment_id = int(data['fragment_id'])
        fragment_text = data['fragment_text']
        fragment = Storage.getExistingFragmentUserById(milestone_id, fragment_id)
        if fragment is None:
            print("CRITICAL ERROR. FRAGMENT NOT EXISTING")
            return
        updatedFragment = Storage.updateFragmentText(fragment, fragment_text)
        WS.send_broadcast_fragment_updated(updatedFragment)
    WS.setCallback("update_fragment_text", update_fragment_text)

    def get_all_texts(client, data):
        milestone_id = int(data['milestone_id'])
        fragments = Storage.getAllMilestoneFragments(milestone_id)
        WS.send_all_texts(client, fragments)
    WS.setCallback("get_all_texts", get_all_texts)

    def clear_fragment_data(client, data):
        milestone_id = int(data['milestone_id'])
        fragment_id = int(data['fragment_id'])
        if Storage.removeUserFragmentByMilestoneIdFragmentId(milestone_id, fragment_id):
            get_all_available_fragments(client, data)
            get_all_texts(client, data)
    WS.setCallback("clear_fragment_data", clear_fragment_data)
