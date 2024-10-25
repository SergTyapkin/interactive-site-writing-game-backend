# ----- INSERTS -----
insertUserFragment = \
    "INSERT INTO users_fragments (user_id, user_username, milestone_id, fragment_id, fragment_name, fragment_description, fragment_default_text, fragment_hardness, text) " \
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) " \
    "RETURNING *"

# ----- SELECTS -----
selectAllUserFragments = \
    "SELECT * FROM users_fragments " \
    "ORDER BY milestone_id, fragment_id"

selectAllUserFragmentsByMilestoneId = \
    "SELECT * FROM users_fragments " \
    "WHERE milestone_id = %s " \
    "ORDER BY fragment_id"

selectUserFragmentByMilestoneIdFragmentId = \
    "SELECT * FROM users_fragments " \
    "WHERE milestone_id = %s AND "\
    "fragment_id = %s"

selectUserFragmentByMilestoneIdUsername = \
    "SELECT * FROM users_fragments " \
    "WHERE milestone_id = %s AND "\
    "user_username = %s"

# ----- UPDATES -----
updateUserFragmentTextByMilestoneIdFragmentId = \
    "UPDATE users_fragments SET " \
    "text = %s " \
    "WHERE milestone_id = %s AND " \
    "fragment_id = %s " \
    "RETURNING *"

# ----- DELETES -----
deleteUserFragmentByMilestoneIdFragmentId = \
    "DELETE FROM users_fragments " \
    "WHERE milestone_id = %s AND " \
    "fragment_id = %s"
