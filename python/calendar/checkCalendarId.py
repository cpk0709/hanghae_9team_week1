from python.database.mongoDB import getConnection
from bson import ObjectId

def checkCalendarIdProcess(calendarId):
    client = getConnection()
    db = client.ourschedule

    result = {}

    try:
        calendarExisted = db.calendar.find_one({'_id': ObjectId(calendarId)})
        if calendarExisted is not None:
            # return True
            result = {"msg": "Existed"}
        else:
            result = {"msg": "not existed"}

        return result

    except Exception as e:
        print(e)
        return {"msg": "error"}