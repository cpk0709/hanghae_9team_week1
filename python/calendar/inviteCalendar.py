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
            return {'link': 'http://localhost:5000/api/calendar/invite?calendarId=' + calendarId}


    except Exception as e:
        print(e)
        return {'msg': 'db error'}

def inviteCalendarProcess(calendarId, userId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    try:
        user = db.user.find_one({'id': userId})
        calendar = db.calendar.find_one({'_id': ObjectId(calendarId)})
        if calendar is None:
            return {'msg': 'not-exist-calendar'}
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