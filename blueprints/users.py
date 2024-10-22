from connections import WS
import database.storage as Storage


def register_callbacks():
    def login_user(client, data):
        user = Storage.addUser(data['username'])
        WS.send_user_logined(user)
    WS.setCallback("login_user", login_user)

    # def answerResult(client, data):
    #     global answeringTeam
    #     if answeringTeam is None:
    #         return
    #
    #     if data['result']:
    #         DB.execute(sql.updateTeamScoreIncrementById, [answeringTeam['teamId']])
    #
    #     team = DB.execute(sql.selectTeamById, [answeringTeam['teamId']])
    #     WS.send_answer_result(data['result'], team['score'])
    #
    #     answeringTeam = None
    # WS.setCallback("answer_result", answerResult)

    # def getAnsweringState(client, data):
    #     return WS.prepare_answering_state(answeringTeam)
    # WS.setCallback("get_answering_state", getAnsweringState)
