from connections import WS


def register_callbacks():
    def take_fragment(client, data):
        WS.send_team_answered(data['userName'], data['teamId'], data['teamName'])
    WS.setCallback("take_fragment", take_fragment)

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
