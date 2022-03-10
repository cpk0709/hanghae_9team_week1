from bson import ObjectId
from python.database.mongoDB import getConnection
import os

#팀 캘린더 초대링크 생성 서비스
def createInviteLinkProcess(calendarId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    try:
        #calendarId에 해당하는 calendar가 없다면
        if db.calendar.find_one({'_id': ObjectId(calendarId)}) is None:
            return {'msg': 'not exist calendar'}
        else:
            #GET방식 링크 반환
            return {'link': 'http://' + os.getenv('SERVER_IP') + '/api/calendar/invite?calendarId=' + calendarId}


    except Exception as e:
        print(e)
        return {'msg': 'db error'}


#캘린더에 초대하는 서비스
def inviteCalendarProcess(calendarId, userId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    try:
        user = db.user.find_one({'id': userId})
        calendar = db.calendar.find_one({'_id': ObjectId(calendarId)})

        #calnedarId에 해당하는 캘린더가 없으면
        if calendar is None:
            return {'msg': 'not-exist-calendar'}
        #이미 팀에 가입되어 있다면
        if db.team.find_one({'userid': user['_id'], 'calendarid':ObjectId(calendarId)}) is not None:
            return {'msg': 'already-join-team'}
        else:
            team = {
                'calendarid': ObjectId(calendarId),
                'userid': user['_id']
            }
            db.team.insert_one(team)

    except Exception as e:
        print(e)
        return {'msg': 'db-error'}

    return {'msg': 'success', 'calendarId': calendarId, 'calendarTitle': calendar['name']}