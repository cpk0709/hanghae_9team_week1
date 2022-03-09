from bson import ObjectId
from python.database.mongoDB import getConnection

def createInviteLinkProcess(calendarId):
    # get db connection
    client = getConnection()
    db = client.ourschedule


    try:
        if db.calendar.find_one({'_id': ObjectId(calendarId)}) is None:
            return {'msg': 'not exist calendar'}
        else:
            return {'link': 'http://localhost:5000/api/calendar/invite'}


    except Exception as e:
        print(e)
        return {'msg': 'db error'}

def inviteCalendarProcess(calendarId, userId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    try:
        if db.calendar.find_one({'_id': ObjectId(calendarId)}) is None:
            return {'msg': 'not exist calendar'}
        else:
            team = {
                'calendarid': ObjectId(calendarId),
                'userid': ObjectId(userId)
            }
            db.team.insert_one(team)

    except Exception as e:
        print(e)
        return {'msg': 'db error'}

    return {'msg': 'success'}